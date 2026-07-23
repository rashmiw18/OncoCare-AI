from datetime import datetime

from app import db


class AIInsight(db.Model):

    __tablename__ = "ai_insights"


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


    health_data_id = db.Column(

        db.Integer,

        db.ForeignKey(

            "health_data.id",

            ondelete="SET NULL"

        ),

        nullable=True

    )


    insight_text = db.Column(

        db.Text,

        nullable=False

    )


    risk_level = db.Column(

        db.String(20),

        default="Low",

        nullable=False

    )


    risk_score = db.Column(

        db.Integer,

        default=0,

        nullable=False

    )


    confidence_score = db.Column(

        db.Float,

        nullable=True

    )


    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow,

        nullable=False

    )


    health_record = db.relationship(

        "HealthData",

        backref="ai_insights",

        foreign_keys=[health_data_id]

    )


    def __repr__(self):

        return (

            f"<AIInsight "

            f"{self.id} "

            f"- "

            f"{self.risk_level}>"

        )