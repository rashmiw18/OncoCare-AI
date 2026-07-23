import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


class Config:

    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "oncocare-ai-development-secret-key"
    )

    # MySQL Database
    MYSQL_USER = os.getenv(
        "MYSQL_USER",
        "root"
    )

    MYSQL_PASSWORD = os.getenv(
        "MYSQL_PASSWORD",
        ""
    )

    MYSQL_HOST = os.getenv(
        "MYSQL_HOST",
        "localhost"
    )

    MYSQL_PORT = os.getenv(
        "MYSQL_PORT",
        "3306"
    )

    MYSQL_DATABASE = os.getenv(
        "MYSQL_DATABASE",
        "oncocare_ai"
    )


    # SQLAlchemy Database URL
    SQLALCHEMY_DATABASE_URI = (

        f"mysql+pymysql://"

        f"{MYSQL_USER}:"

        f"{MYSQL_PASSWORD}@"

        f"{MYSQL_HOST}:"

        f"{MYSQL_PORT}/"

        f"{MYSQL_DATABASE}"

    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Gemini API
    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
        ""
    )


    # Application settings
    APP_NAME = "OncoCare AI"