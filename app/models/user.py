from datetime import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="patient"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # Relationships

    health_records = db.relationship(

        "HealthData",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"

    )


    symptoms = db.relationship(

        "Symptom",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"

    )


    ai_insights = db.relationship(

        "AIInsight",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"

    )


    alerts = db.relationship(

        "Alert",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"

    )


    def __repr__(self):

        return (

            f"<User "

            f"{self.email}>"

        )