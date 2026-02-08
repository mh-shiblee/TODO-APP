from flask import Flask
from flask_login import LoginManager
from config import Config
from app.models import db, User


login_manager = LoginManager()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
   
    app.config.from_object(Config)
    
   
    db.init_app(app)
    login_manager.init_app(app)
    
    
    login_manager.login_view = 'login'  
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    with app.app_context():
        db.create_all()
        print("✅ Database tables created!")
    
    
    from app.routes import register_routes
    register_routes(app)
    
    return app