from datetime import datetime

from app import db


class HealthData(db.Model):

    __tablename__ = "health_data"


    id = db.Column(

        db.Integer,

        primary_key=True

    )


    user_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "users.id",

            ondelete="CASCADE"

        ),

        nullable=False

    )


    temperature = db.Column(

        db.Float,

        nullable=True

    )


    heart_rate = db.Column(

        db.Integer,

        nullable=True

    )


    spo2 = db.Column(

        db.Float,

        nullable=True

    )


    sleep_hours = db.Column(

        db.Float,

        nullable=True

    )


    pain_level = db.Column(

        db.Integer,

        nullable=True

    )


    fatigue_level = db.Column(

        db.Integer,

        nullable=True

    )


    nausea_level = db.Column(

        db.Integer,

        nullable=True

    )


    dizziness = db.Column(

        db.Boolean,

        default=False

    )


    notes = db.Column(

        db.Text,

        nullable=True

    )


    recorded_at = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )


    def __repr__(self):

        return (

            f"<HealthData "

            f"{self.id}>"

        )