from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.database import init_db
from app.routes.auth import auth_bp
from app.routes.attendance import attendance_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    CORS(app)
    JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    
    @app.route('/')
    def home():
        return jsonify({
            "message": "Smart Attendance System API",
            "endpoints": {
                "auth": ["/api/auth/register", "/api/auth/login", "/api/auth/me"],
                "attendance": ["/api/attendance/generate-qr", "/api/attendance/mark-attendance", "/api/attendance/attendance/<student_id>"]
            }
        })
    
    return app