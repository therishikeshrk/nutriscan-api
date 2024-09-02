from flask import Blueprint

# Create Blueprints
api_bp = Blueprint('api', __name__)
health_check_bp = Blueprint('health_check', __name__)

def register_routes(app):
    from .food_controller import api_bp
    from .health_check import health_check_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(health_check_bp)
