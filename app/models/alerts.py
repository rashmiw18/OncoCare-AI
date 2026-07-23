from datetime import datetime

from app import db


class Alert(db.Model):

    __tablename__ = "alerts"


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


    alert_type = db.Column(

        db.String(50),

        nullable=False

    )


    message = db.Column(

        db.Text,

        nullable=False

    )


    severity = db.Column(

        db.String(20),

        nullable=False

    )


    is_read = db.Column(

        db.Boolean,

        default=False,

        nullable=False

    )


    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow,

        nullable=False

    )


    def __repr__(self):

        return (

            f"<Alert "

            f"{self.id} "

            f"- "

            f"{self.alert_type} "

            f"- "

            f"{self.severity}>"

        )