from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from app.models.health_data import HealthData
from app.models.ai_insight import AIInsight

from app.services.chatbot_service import ChatbotService


chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


# =========================================
# CHATBOT PAGE
# =========================================

@chatbot_bp.route("/")
@login_required
def chatbot():

    return render_template(
        "chatbot.html"
    )


# =========================================
# SEND MESSAGE TO CHATBOT
# =========================================

@chatbot_bp.route(
    "/message",
    methods=["POST"]
)
@login_required
def send_message():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        user_message = data.get(
            "message",
            ""
        ).strip()


        if not user_message:

            return jsonify({

                "success": False,

                "message":
                    "Please enter a message."

            }), 400


        # =================================
        # FETCH USER HEALTH RECORDS
        # =================================

        health_records = (

            HealthData.query

            .filter_by(

                user_id=current_user.id

            )

            .order_by(

                HealthData.recorded_at.desc()

            )

            .limit(10)

            .all()

        )


        health_context = ""


        if health_records:

            health_context += (

                "RECENT HEALTH RECORDS:\n\n"

            )


            for record in health_records:

                health_context += (

                    f"Date: "
                    f"{record.recorded_at}\n"

                    f"Heart Rate: "
                    f"{record.heart_rate} BPM\n"

                    f"SpO2: "
                    f"{record.spo2}%\n"

                    f"Temperature: "
                    f"{record.temperature} °F\n"

                    f"Sleep: "
                    f"{record.sleep_hours} hours\n"

                    f"Fatigue: "
                    f"{record.fatigue_level}/10\n"

                    f"Pain: "
                    f"{record.pain_level}/10\n\n"

                )


        else:

            health_context = (

                "No health records are available "

                "for this user yet.\n"

            )


        # =================================
        # FETCH LATEST AI INSIGHT
        # =================================

        latest_insight = (

            AIInsight.query

            .filter_by(

                user_id=current_user.id

            )

            .order_by(

                AIInsight.created_at.desc()

            )

            .first()

        )


        if latest_insight:

            health_context += (

                "\nLATEST AI HEALTH INSIGHT:\n\n"

                f"Risk Level: "
                f"{latest_insight.risk_level}\n"

                f"Risk Score: "
                f"{latest_insight.risk_score}\n"

                f"Insight: "
                f"{latest_insight.insight_text}\n"

            )


        # =================================
        # CHATBOT SERVICE
        # =================================

        chatbot_service = ChatbotService()


        response = (

            chatbot_service.generate_response(

                user_message=user_message,

                health_context=health_context

            )

        )


        return jsonify({

            "success": True,

            "response": response

        })


    except Exception as error:

        print(

            "CHATBOT ERROR:",

            error

        )


        error_text = str(error).lower()


        # =================================
        # QUOTA ERROR
        # =================================

        if (

            "429" in error_text

            or "resource_exhausted"

            in error_text

            or "quota" in error_text

        ):

            return jsonify({

                "success": False,

                "message": (

                    "The chatbot API has "

                    "temporarily reached its "

                    "request limit. Please try "

                    "again later or use a "

                    "different chatbot API key."

                )

            }), 429


        # =================================
        # MODEL UNAVAILABLE
        # =================================

        if (

            "503" in error_text

            or "unavailable"

            in error_text

        ):

            return jsonify({

                "success": False,

                "message": (

                    "The AI model is temporarily "

                    "unavailable. Please try "

                    "again shortly."

                )

            }), 503


        # =================================
        # GENERAL ERROR
        # =================================

        return jsonify({

            "success": False,

            "message": (

                "Unable to connect to the AI "

                "assistant right now. Please "

                "try again later."

            )

        }), 500