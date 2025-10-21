import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("mysql://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("mysql://", "mysql+pymysql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_timeout": 20,
        "pool_recycle": -1,
        "pool_pre_ping": True
    }

    # Email
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False").lower() in ["true", "1", "yes"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # PayOS
    PAYOS_CLIENT_ID = os.environ.get("PAYOS_CLIENT_ID")
    PAYOS_API_KEY = os.environ.get("PAYOS_API_KEY")
    PAYOS_CHECKSUM_KEY = os.environ.get("PAYOS_CHECKSUM_KEY")
    PAYOS_RETURN_URL = os.environ.get("PAYOS_RETURN_URL")
    PAYOS_CANCEL_URL = os.environ.get("PAYOS_CANCEL_URL")

    # Downloads
    DOWNLOAD_FILE_URL = os.environ.get("DOWNLOAD_FILE_URL")
    DOWNLOAD_FILE_NAME = os.environ.get("DOWNLOAD_FILE_NAME", "App.exe")

    # Payment
    PAYMENT_AMOUNT = int(os.environ.get("PAYMENT_AMOUNT", "50000"))
    PAYMENT_CURRENCY = "VND"
