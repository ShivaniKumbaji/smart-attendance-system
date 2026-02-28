from flask_sqlalchemy import SQLAlchemy
from app.models import db

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'  # Using SQLite for simplicity
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database initialized!")