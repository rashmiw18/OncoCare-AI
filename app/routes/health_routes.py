from flask import (

    Blueprint,

    render_template,

    request,

    redirect,

    url_for,

    flash

)

from flask_login import (

    login_required,

    current_user

)

from app import db

from app.models.health_data import HealthData


health_bp = Blueprint(

    "health",

    __name__,

    url_prefix="/health"

)


@health_bp.route(

    "/add",

    methods=["GET", "POST"]

)

@login_required

def add_health_data():


    if request.method == "POST":


        try:


            temperature = float(

                request.form.get(

                    "temperature"

                )

            )


            heart_rate = int(

                request.form.get(

                    "heart_rate"

                )


            )


            spo2 = float(

                request.form.get(

                    "spo2"

                )


            )


            sleep_hours = float(

                request.form.get(

                    "sleep_hours"

                )


            )


            pain_level = int(

                request.form.get(

                    "pain_level"

                )


            )


            fatigue_level = int(

                request.form.get(

                    "fatigue_level"

                )


            )


            nausea_level = int(

                request.form.get(

                    "nausea_level"

                )


            )


            dizziness = (

                request.form.get(

                    "dizziness"

                ) == "yes"

            )


            notes = request.form.get(

                "notes"

            )


            # Basic validation

            if not 0 <= pain_level <= 10:

                raise ValueError(

                    "Pain level must be between 0 and 10."

                )


            if not 0 <= fatigue_level <= 10:

                raise ValueError(

                    "Fatigue level must be between 0 and 10."

                )


            if not 0 <= nausea_level <= 10:

                raise ValueError(

                    "Nausea level must be between 0 and 10."

                )


            health_record = HealthData(

                user_id=current_user.id,

                temperature=temperature,

                heart_rate=heart_rate,

                spo2=spo2,

                sleep_hours=sleep_hours,

                pain_level=pain_level,

                fatigue_level=fatigue_level,

                nausea_level=nausea_level,

                dizziness=dizziness,

                notes=notes

            )


            db.session.add(

                health_record

            )


            db.session.commit()


            flash(

                "Health data saved successfully.",

                "success"

            )


            return redirect(

                url_for(

                    "dashboard.dashboard"

                )

            )


        except (

            ValueError,

            TypeError

        ) as error:


            db.session.rollback()


            flash(

                f"Invalid health data: {error}",

                "error"

            )


            return redirect(

                url_for(

                    "health.add_health_data"

                )

            )


    return render_template(

        "health_form.html"

    )