from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, User, Attendance
from app.utils import generate_qr_code
from datetime import datetime, date

attendance_bp = Blueprint('attendance', __name__)

# API 3: Generate QR Code for attendance
@attendance_bp.route('/generate-qr', methods=['POST'])
@jwt_required()
def generate_qr():
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        # Create session data
        session_data = f"class:{data.get('class_id', 'default')}:date:{date.today()}"
        
        # Generate QR code
        qr_code = generate_qr_code(session_data)
        
        return jsonify({
            "qr_code": qr_code,
            "session": session_data,
            "message": "QR Code generated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 4: Mark Attendance (via QR scan)
@attendance_bp.route('/mark-attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get student ID from request
        student_id = data.get('student_id')
        
        if not student_id:
            return jsonify({"error": "Student ID required"}), 400
        
        # Check if user is a student
        student = User.query.get(student_id)
        if not student or student.role != 'student':
            return jsonify({"error": "Invalid student ID"}), 400
        
        # Check if attendance already marked today
        today = date.today()
        existing = Attendance.query.filter_by(
            student_id=student_id,
            date=today
        ).first()
        
        if existing:
            return jsonify({"error": "Attendance already marked for today"}), 400
        
        # Mark attendance
        attendance = Attendance(
            student_id=student_id,
            date=today,
            status='present',
            marked_by=current_user_id
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            "message": "Attendance marked successfully",
            "attendance": {
                "student_id": student_id,
                "student_name": student.name,
                "date": str(today),
                "status": "present"
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API 5: Get student attendance history
@attendance_bp.route('/attendance/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_attendance(student_id):
    try:
        records = Attendance.query.filter_by(student_id=student_id).all()
        
        result = []
        for record in records:
            result.append({
                'id': record.id,
                'date': str(record.date),
                'status': record.status,
                'marked_by': record.marked_by,
                'marked_at': str(record.marked_at)
            })
        
        return jsonify({
            'student_id': student_id,
            'total_records': len(result),
            'attendance': result
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500