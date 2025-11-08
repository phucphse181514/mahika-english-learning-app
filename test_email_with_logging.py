"""
Test email sending with detailed logging
Usage: python test_email_with_logging.py <recipient_email>
Example: python test_email_with_logging.py test@example.com
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, mail
from flask_mail import Message
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def test_email(recipient_email):
    """Test email sending with detailed logging"""
    
    logger.info("=" * 80)
    logger.info("🧪 EMAIL TESTING SCRIPT")
    logger.info("=" * 80)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Log configuration
        logger.info("📧 Email Configuration:")
        logger.info(f"   MAIL_SERVER: {app.config.get('MAIL_SERVER')}")
        logger.info(f"   MAIL_PORT: {app.config.get('MAIL_PORT')}")
        logger.info(f"   MAIL_USE_TLS: {app.config.get('MAIL_USE_TLS')}")
        logger.info(f"   MAIL_USE_SSL: {app.config.get('MAIL_USE_SSL')}")
        logger.info(f"   MAIL_USERNAME: {app.config.get('MAIL_USERNAME')}")
        logger.info(f"   MAIL_PASSWORD: {'***' if app.config.get('MAIL_PASSWORD') else 'NOT SET'}")
        logger.info(f"   MAIL_DEFAULT_SENDER: {app.config.get('MAIL_DEFAULT_SENDER')}")
        logger.info(f"   MAIL_DEBUG: {app.config.get('MAIL_DEBUG')}")
        logger.info("")
        
        # Check configuration
        if not app.config.get('MAIL_USERNAME'):
            logger.error("❌ MAIL_USERNAME is not configured!")
            return False
        
        if not app.config.get('MAIL_PASSWORD'):
            logger.error("❌ MAIL_PASSWORD is not configured!")
            return False
        
        # Prepare test email
        logger.info(f"📝 Preparing test email to: {recipient_email}")
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        msg = Message(
            subject=f'🧪 Test Email from Mahika - {current_time}',
            recipients=[recipient_email],
            html=f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2>✅ Email Test Successful!</h2>
                    <p>This is a test email from Mahika English Learning App.</p>
                    <p><strong>Sent at:</strong> {current_time}</p>
                    <hr>
                    <h3>Email Configuration:</h3>
                    <ul>
                        <li>Server: {app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}</li>
                        <li>TLS: {app.config.get('MAIL_USE_TLS')}</li>
                        <li>From: {app.config.get('MAIL_DEFAULT_SENDER')}</li>
                    </ul>
                    <p style="color: green;">If you can read this, email sending is working correctly! ✅</p>
                </body>
            </html>
            """,
            body=f"""
            Email Test Successful!
            
            This is a test email from Mahika English Learning App.
            Sent at: {current_time}
            
            Email Configuration:
            - Server: {app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}
            - TLS: {app.config.get('MAIL_USE_TLS')}
            - From: {app.config.get('MAIL_DEFAULT_SENDER')}
            
            If you can read this, email sending is working correctly!
            """
        )
        
        logger.info(f"   Subject: {msg.subject}")
        logger.info(f"   From: {msg.sender}")
        logger.info(f"   To: {msg.recipients}")
        logger.info("")
        
        # Send email
        try:
            logger.info("📧 Attempting to send email...")
            logger.info("   Connecting to SMTP server...")
            
            mail.send(msg)
            
            logger.info("✅ Email sent successfully!")
            logger.info("")
            logger.info("=" * 80)
            logger.info("✅ TEST PASSED - Email was sent successfully")
            logger.info(f"📬 Check inbox at: {recipient_email}")
            logger.info("=" * 80)
            return True
            
        except Exception as e:
            logger.error("")
            logger.error("❌ Failed to send email!")
            logger.error(f"   Error Type: {type(e).__name__}")
            logger.error(f"   Error Message: {str(e)}")
            logger.error("")
            logger.error("=" * 80)
            logger.error("❌ TEST FAILED")
            logger.error("=" * 80)
            logger.exception("Full traceback:")
            return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ Usage: python test_email_with_logging.py <recipient_email>")
        print("📧 Example: python test_email_with_logging.py test@example.com")
        sys.exit(1)
    
    recipient = sys.argv[1]
    success = test_email(recipient)
    
    sys.exit(0 if success else 1)
