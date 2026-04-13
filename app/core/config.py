import os

APP_DIR      = os.path.dirname(os.path.dirname(__file__))   # backend/app/
BASE_DIR     = os.path.dirname(APP_DIR)                     # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                    # DraxenAI/

class Settings:
    APP_NAME:      str  = "Draxen AI API"
    VERSION:       str  = "1.0.0"
    DB_PATH:       str  = os.path.join(BASE_DIR, "database.db")
    STATIC_DIR:    str  = os.path.join(APP_DIR, "static")
    TEMPLATES_DIR: str  = os.path.join(APP_DIR, "templates")
    CORS_ORIGINS:  list = ["*"]

settings = Settings()
