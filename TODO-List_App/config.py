import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-super-secret-key-change-this'
    

    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False