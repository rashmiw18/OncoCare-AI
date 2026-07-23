from app import db

from app.models.alerts import Alert


class AlertService:


    @staticmethod

    def create_alert(

        user_id,

        risk_level,

        message

    ):


        if risk_level == "High":

            alert_type = "HIGH_RISK"


        elif risk_level == "Medium":

            alert_type = "MEDIUM_RISK"


        else:

            alert_type = "INFO"


        alert = Alert(

            user_id=user_id,

            alert_type=alert_type,

            message=message,

            severity=risk_level,

            is_read=False

        )


        db.session.add(

            alert

        )


        db.session.commit()


        return alert


    @staticmethod

    def create_anomaly_alert(

        user_id,

        message

    ):


        alert = Alert(

            user_id=user_id,

            alert_type="ANOMALY",

            message=message,

            severity="Medium",

            is_read=False

        )


        db.session.add(

            alert

        )


        db.session.commit()


        return alert