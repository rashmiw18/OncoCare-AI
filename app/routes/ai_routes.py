import json

from flask import (

    Blueprint,

    render_template,

    redirect,

    url_for,

    flash

)

from flask_login import (

    login_required,

    current_user

)

from app import db

from app.models.health_data import (

    HealthData

)

from app.models.ai_insight import (

    AIInsight

)

from app.services.health_service import (

    HealthService

)

from app.services.alert_service import (

    AlertService

)


ai_bp = Blueprint(

    "ai",

    __name__,

    url_prefix="/ai"

)
def parse_ai_insight(text):

    if not text:
        return {
            "summary": "",
            "observations": [],
            "risk_factors": [],
            "recommendations": [],
            "confidence": "Unknown"
        }


    # ---------------------------------
    # TRY JSON FIRST
    # ---------------------------------

    try:

        data = json.loads(text)

        return {

            "summary": data.get(
                "summary",
                ""
            ),

            "observations": data.get(
                "observations",
                data.get(
                    "key_observations",
                    []
                )
            ),

            "risk_factors": data.get(
                "risk_factors",
                []
            ),

            "recommendations": data.get(
                "recommendations",
                []
            ),

            "confidence": data.get(
                "confidence",
                "Unknown"
            )

        }

    except Exception:

        pass


    # ---------------------------------
    # FALLBACK FOR OLD TEXT RESPONSES
    # ---------------------------------

    sections = {

        "summary": "",

        "observations": [],

        "risk_factors": [],

        "recommendations": [],

        "confidence": "Unknown"

    }


    current_section = None


    for line in text.splitlines():

        line = line.strip()


        if not line:

            continue


        upper_line = line.upper()


        if upper_line.startswith("SUMMARY"):

            current_section = "summary"

            continue


        elif (

            upper_line.startswith(

                "KEY OBSERVATIONS"

            )

            or upper_line.startswith(

                "OBSERVATIONS"

            )

        ):

            current_section = "observations"

            continue


        elif (

            upper_line.startswith(

                "RISK FACTORS"

            )

            or upper_line.startswith(

                "POSSIBLE RISKS"

            )

        ):

            current_section = "risk_factors"

            continue


        elif (

            upper_line.startswith(

                "RECOMMENDATIONS"

            )

            or upper_line.startswith(

                "RECOMMENDATION"

            )

        ):

            current_section = "recommendations"

            continue


        elif upper_line.startswith("CONFIDENCE"):

            current_section = "confidence"

            continue


        # Remove bullet symbols

        clean_line = line.lstrip(

            "-•*0123456789. "

        ).strip()


        if not clean_line:

            continue


        if current_section == "summary":

            if sections["summary"]:

                sections["summary"] += " " + clean_line

            else:

                sections["summary"] = clean_line


        elif current_section == "observations":

            sections["observations"].append(

                clean_line

            )


        elif current_section == "risk_factors":

            sections["risk_factors"].append(

                clean_line

            )


        elif current_section == "recommendations":

            sections["recommendations"].append(

                clean_line

            )


        elif current_section == "confidence":

            sections["confidence"] = clean_line


    return sections


@ai_bp.route("/insights")

@login_required

def insights():


    insights_data = (

        AIInsight.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            AIInsight.created_at.desc()

        )

        .all()

    )


    parsed_insights = []

    for insight in insights_data:

        parsed_data = parse_ai_insight(

            insight.insight_text

        )


        parsed_insights.append({

            "id": insight.id,

            "risk_level": insight.risk_level,

            "risk_score": insight.risk_score,

            "created_at": insight.created_at,

            "data": parsed_data

        })


    return render_template(

        "ai_insights.html",

        insights=parsed_insights

    )


@ai_bp.route("/analyze")

@login_required

def analyze_health():


    # =====================================
    # STEP 1: FETCH HEALTH RECORDS
    # =====================================

    health_records = (

        HealthData.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            HealthData.recorded_at.asc()

        )

        .all()

    )


    if not health_records:


        flash(

            "Please add health data before "
            "running AI analysis.",

            "warning"

        )


        return redirect(

            url_for(

                "dashboard.dashboard"

            )

        )


    try:


        # =====================================
        # STEP 2: COMPLETE ANALYSIS
        # =====================================

        health_service = (

            HealthService()

        )


        result = (

            health_service

            .analyze_patient_health(

                health_records

            )

        )


        if (

            result.get(

                "status"

            )

            != "success"

        ):


            flash(

                result.get(

                    "message",

                    "Unable to analyze health data."

                ),

                "warning"

            )


            return redirect(

                url_for(

                    "dashboard.dashboard"

                )

            )


        # =====================================
        # STEP 3: STORE STRUCTURED AI INSIGHT
        # =====================================

        ai_insight_data = (

            result.get(

                "ai_insight",

                {}

            )

        )


        # Convert dictionary to JSON string
        if isinstance(

            ai_insight_data,

            dict

        ):


            insight_text = json.dumps(

                ai_insight_data

            )


        else:


            insight_text = str(

                ai_insight_data

            )


        insight = AIInsight(

            user_id=current_user.id,

            insight_text=insight_text,

            risk_level=result.get(

                "risk_level",

                "Unknown"

            ),

            risk_score=result.get(

                "risk_score",

                0

            )

        )


        db.session.add(

            insight

        )


        db.session.commit()


        # =====================================
        # STEP 4: RISK ALERT
        # =====================================

        if result.get(

            "risk_level"

        ) in [

            "High",

            "Medium"

        ]:


            alert_message = (

                "The AI monitoring system detected "

                f"a {result['risk_level'].lower()}-risk "

                "health pattern. Please review your "

                "AI health insight."

            )


            AlertService.create_alert(

                user_id=current_user.id,

                risk_level=result["risk_level"],

                message=alert_message

            )


        # =====================================
        # STEP 5: ANOMALY ALERT
        # =====================================

        anomaly_result = (

            result.get(

                "anomaly_result",

                {}

            )

        )


        if (

            anomaly_result.get(

                "anomaly_count",

                0

            )

            > 0

        ):


            AlertService.create_anomaly_alert(

                user_id=current_user.id,

                message=(

                    "An unusual health pattern was "

                    "detected by the machine learning "

                    "monitoring system."

                )

            )


        flash(

            "AI health analysis completed successfully.",

            "success"

        )


        return redirect(

            url_for(

                "ai.insights"

            )

        )


    except Exception as error:


        db.session.rollback()


        print(

            "AI ANALYSIS ERROR:",

            error

        )


        flash(

            "An error occurred while analyzing "
            "your health data.",

            "danger"

        )


        return redirect(

            url_for(

                "dashboard.dashboard"

            )

        )