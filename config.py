import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB file upload limit
    SAMPLE_RATE = 44000 # added sample rate. Originally from file_analysis.py


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Default config
config = DevelopmentConfig
