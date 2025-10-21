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
        # Get default sender or use MAIL_USERNAME
        sender = current_app.config.get('MAIL_DEFAULT_SENDER') or current_app.config.get('MAIL_USERNAME')
        
        if not sender:
            return jsonify({
                'status': 'error',
                'message': 'MAIL_DEFAULT_SENDER or MAIL_USERNAME not configured'
            }), 500
        
        # Create test message - send to same email as sender for testing
        msg = Message(
            subject='✅ Brevo SMTP Test from Railway',
            recipients=[sender],  # Send to self for testing
            body='If you received this email, your Brevo SMTP configuration is working correctly!',
            html='''
            <h2>✅ Brevo SMTP Test Successful!</h2>
            <p>Your Brevo SMTP configuration on Railway is working correctly.</p>
            <p><strong>Configuration:</strong></p>
            <ul>
                <li>Server: smtp-relay.brevo.com</li>
                <li>Port: 587</li>
                <li>Sender: ''' + sender + '''</li>
            </ul>
            <p>This email was sent asynchronously using background threading.</p>
            '''
        )
        
        # Send asynchronously
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
        
        current_app.logger.info(f"📧 Test email triggered for {sender}")
        
        return jsonify({
            'status': 'success',
            'message': f'Test email triggered! Check inbox at: {sender}',
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

