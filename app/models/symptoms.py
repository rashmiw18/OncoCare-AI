from datetime import datetime

from app import db


class Symptom(db.Model):

    __tablename__ = "symptoms"


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


    symptom_name = db.Column(

        db.String(100),

        nullable=False

    )


    severity = db.Column(

        db.Integer,

        nullable=False

    )


    description = db.Column(

        db.Text,

        nullable=True

    )


    recorded_at = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )


    def __repr__(self):

        return (

            f"<Symptom "

            f"{self.symptom_name}>"

        )