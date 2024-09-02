from flask import Flask
from .config import Config
from .routes import food_controller
from .routes import health_check_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
   
    
    app.register_blueprint(food_controller.api_bp, url_prefix='/api')
    app.register_blueprint(health_check_bp)
    
    return app
