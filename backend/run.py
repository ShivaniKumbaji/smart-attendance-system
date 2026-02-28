from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Smart Attendance System API Starting...")
    print("📍 Server will run on: http://localhost:5000")
    print("📝 Available endpoints:")
    print("   POST /api/auth/register - Register new user")
    print("   POST /api/auth/login - Login user")
    print("   GET /api/auth/me - Get current user (protected)")
    app.run(debug=True, port=5000)