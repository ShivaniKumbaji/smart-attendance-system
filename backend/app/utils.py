from flask_jwt_extended import create_access_token
from datetime import timedelta
import qrcode
import io
import base64

def generate_token(user_id, role):
    """Generate JWT token for authenticated user"""
    return create_access_token(
        identity=user_id,
        additional_claims={"role": role},
        expires_delta=timedelta(days=1)
    )

def generate_qr_code(data):
    """Generate QR code from data"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str