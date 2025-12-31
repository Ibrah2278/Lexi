import os
from dotenv import load_dotenv

load_dotenv()  # charge le fichier .env

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "une_clef_secrete")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "mysql://user:password@localhost/lexi")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
