from flask import Blueprint, jsonify, current_app
from flask_mail import Message
from threading import Thread
from app import mail

test_bp = Blueprint('test', __name__, url_prefix='/test')

# ================================================================
# FIX: Test route for Brevo SMTP verification
# ================================================================
# Purpose:
#   Verify Brevo SMTP connection is working on Railway production
#   Send a test email asynchronously to confirm configuration
# ================================================================

def send_async_email(app, msg):
    """Send email in background thread."""
    with app.app_context():
        try:
            mail.send(msg)
            app.logger.info(f"✅ Test email sent successfully to {msg.recipients}")
        except Exception as e:
            app.logger.error(f"❌ Test email failed: {str(e)}")
            raise

@test_bp.route('/brevo')
def test_brevo():
    """
    Test Brevo SMTP connection.
    Usage: GET /test/brevo
    """
    try:
        # Test recipient email
        test_recipient = 'buinguyenkhoi6868@gmail.com'
        
        # Get default sender for FROM field
        sender = current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME')
        
        if not sender:
            return jsonify({
                'status': 'error',
                'message': 'MAIL_DEFAULT_SENDER or MAIL_USERNAME not configured'
            }), 500
        
        # Create test message - send to test recipient
        msg = Message(
            subject='✅ Brevo SMTP Test from Railway - Mahika App',
            recipients=[test_recipient],  # Send to test email
            body='Xin chào! Đây là email test từ hệ thống Mahika English Learning App.\n\nNếu bạn nhận được email này, nghĩa là cấu hình Brevo SMTP đã hoạt động chính xác!\n\nCảm ơn đã test.',
            html='''
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #4CAF50;">✅ Brevo SMTP Test Thành Công!</h2>
                <p>Xin chào <strong>buinguyenkhoi6868@gmail.com</strong>,</p>
                <p>Đây là email test từ hệ thống <strong>Mahika English Learning App</strong>.</p>
                <p>Nếu bạn nhận được email này, nghĩa là cấu hình Brevo SMTP đã hoạt động chính xác!</p>
                
                <h3>📋 Thông tin cấu hình:</h3>
                <ul>
                    <li><strong>SMTP Server:</strong> smtp-relay.brevo.com</li>
                    <li><strong>Port:</strong> 587</li>
                    <li><strong>Sender:</strong> ''' + sender + '''</li>
                    <li><strong>Method:</strong> Async (Background Threading)</li>
                </ul>
                
                <p style="color: #666; font-size: 12px; margin-top: 30px;">
                    Email này được gửi tự động từ Railway production environment.
                </p>
            </div>
            '''
        )
        
        # Send asynchronously
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
        
        current_app.logger.info(f"📧 Test email triggered for {test_recipient} (from: {sender})")
        
        return jsonify({
            'status': 'success',
            'message': f'Test email triggered! Check inbox at: {test_recipient}',
            'from': sender,
            'note': 'Email is being sent in background. Check Railway logs for status.'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"❌ Test route error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@test_bp.route('/email-config')
def test_email_config():
    """
    Display current email configuration (without sensitive data).
    Usage: GET /test/email-config
    """
    config = current_app.config
    
    return jsonify({
        'MAIL_SERVER': config.get('MAIL_SERVER'),
        'MAIL_PORT': config.get('MAIL_PORT'),
        'MAIL_USE_TLS': config.get('MAIL_USE_TLS'),
        'MAIL_USE_SSL': config.get('MAIL_USE_SSL'),
        'MAIL_USERNAME': config.get('MAIL_USERNAME')[:5] + '***' if config.get('MAIL_USERNAME') else 'NOT SET',
        'MAIL_PASSWORD': '***SET***' if config.get('MAIL_PASSWORD') else 'NOT SET',
        'MAIL_DEFAULT_SENDER': config.get('MAIL_DEFAULT_SENDER'),
        'MAIL_DEBUG': config.get('MAIL_DEBUG'),
        'MAIL_TIMEOUT': config.get('MAIL_TIMEOUT')
    }), 200

@test_bp.route('/health')
def health_check():
    """
    Simple health check endpoint.
    Usage: GET /test/health
    """
    return jsonify({
        'status': 'healthy',
        'app': 'Mahika English Learning',
        'email_configured': bool(current_app.config.get('MAIL_USERNAME'))
    }), 200

