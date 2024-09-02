from flask import Flask
from ..config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    from app.routes.food_controller import api_bp
    from routes.health_check import health_check_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(health_check_bp)
    
    return app
