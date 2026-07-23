from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from app.models.health_data import HealthData


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
@login_required
def dashboard():

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


    latest_record = (

        HealthData.query

        .filter_by(

            user_id=current_user.id

        )

        .order_by(

            HealthData.recorded_at.desc()

        )

        .first()

    )


    chart_labels = [

        record.recorded_at.strftime(

            "%d %b"

        )

        for record in health_records

    ]


    temperature_data = [

        record.temperature

        for record in health_records

    ]


    heart_rate_data = [

        record.heart_rate

        for record in health_records

    ]


    spo2_data = [

        record.spo2

        for record in health_records

    ]


    sleep_data = [

        record.sleep_hours

        for record in health_records

    ]


    fatigue_data = [

        record.fatigue_level

        for record in health_records

    ]


    pain_data = [

        record.pain_level

        for record in health_records

    ]


    return render_template(

        "dashboard.html",

        latest_record=latest_record,

        health_records=health_records,

        chart_labels=chart_labels,

        temperature_data=temperature_data,

        heart_rate_data=heart_rate_data,

        spo2_data=spo2_data,

        sleep_data=sleep_data,

        fatigue_data=fatigue_data,

        pain_data=pain_data

    )