# config.py
import os

class Config:
    # Use environment variable DATABASE_URI if set, otherwise default to local MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'mysql+pymysql://root:password@localhost:3306/hospital_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
