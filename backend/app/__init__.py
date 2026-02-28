# This file makes 'app' a Python package
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.database import init_db
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-in-production'  # Change this!
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    @app.route('/')
    def home():
        return jsonify({"message": "Smart Attendance System API"})
    
    return app