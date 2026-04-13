import os

APP_DIR      = os.path.dirname(os.path.dirname(__file__))   # backend/app/
BASE_DIR     = os.path.dirname(APP_DIR)                     # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                    # DraxenAI/

class Settings:
    APP_NAME:      str  = "Draxen AI"
    VERSION:       str  = "1.0.0"
    MONGO_URI:     str  = os.environ.get("MONGO_URI", "mongodb+srv://admin:Atuldandekar%4015@cluster0.hbtkrjz.mongodb.net/?appName=Cluster0")
    DB_NAME:       str  = os.environ.get("DB_NAME", "draxen_db")
    STATIC_DIR:    str  = os.path.join(APP_DIR, "static")
    TEMPLATES_DIR: str  = os.path.join(APP_DIR, "templates")
    CORS_ORIGINS:  list = ["*"]

settings = Settings()
