from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User
from app.utils import generate_token
from werkzeug.security import generate_password_hash, check_password_hash

# Create blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# API 1: Register User
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Get data from request
        data = request.get_json()
        
        # Check if all required fields are present
        if not all(k in data for k in ('name', 'email', 'password', 'role')):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=data['role']  # 'admin', 'faculty', or 'student'
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "role": new_user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 2: Login User
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Get data from request
        data = request.get_json()
        
        # Check if email and password are provided
        if not all(k in data for k in ('email', 'password')):
            return jsonify({"error": "Email and password required"}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, data['password']):
            # Generate JWT token
            token = generate_token(user.id, user.role)
            
            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 3: Get Current User (Protected route example)
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        # Get user ID from JWT token
        current_user_id = get_jwt_identity()
        
        # Find user in database
        user = User.query.get(current_user_id)
        
        if user:
            return jsonify({
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500