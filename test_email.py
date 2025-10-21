#!/usr/bin/env python3
"""
Test email configuration
"""
import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

load_dotenv()

def test_email():
    """Test email sending"""
    print("=" * 60)
    print("🧪 TESTING EMAIL CONFIGURATION")
    print("=" * 60)
    
    # Check environment variables
    print("\n📋 Checking environment variables...")
    mail_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    mail_port = os.environ.get('MAIL_PORT', '587')
    mail_username = os.environ.get('MAIL_USERNAME')
    mail_password = os.environ.get('MAIL_PASSWORD')
    
    print(f"   MAIL_SERVER: {mail_server}")
    print(f"   MAIL_PORT: {mail_port}")
    print(f"   MAIL_USERNAME: {mail_username if mail_username else '❌ NOT SET'}")
    print(f"   MAIL_PASSWORD: {'✅ SET' if mail_password else '❌ NOT SET'}")
    
    if not mail_username or not mail_password:
        print("\n❌ ERROR: MAIL_USERNAME or MAIL_PASSWORD not set!")
        print("\n📝 To fix this:")
        print("   1. Create .env file in project root")
        print("   2. Add these lines:")
        print("      MAIL_USERNAME=your-email@gmail.com")
        print("      MAIL_PASSWORD=your-app-password")
        print("\n📖 See RAILWAY_PRODUCTION_SETUP.md for instructions")
        return False
    
    # Create Flask app
    print("\n🔧 Creating Flask app...")
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = mail_server
    app.config['MAIL_PORT'] = int(mail_port)
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = mail_password
    app.config['MAIL_DEFAULT_SENDER'] = mail_username
    app.config['MAIL_TIMEOUT'] = 10
    
    mail = Mail(app)
    
    # Send test email
    print(f"\n📧 Sending test email to {mail_username}...")
    
    try:
        with app.app_context():
            msg = Message(
                subject='✅ Mahika Email Test - Success!',
                recipients=[mail_username],
                body='🎉 Congratulations! Your email configuration is working correctly.\n\n'
                     'You can now deploy your app to Railway.\n\n'
                     'If you received this email, your SMTP settings are correct.',
                html='<h2>✅ Email Test Successful!</h2>'
                     '<p>🎉 Congratulations! Your email configuration is working correctly.</p>'
                     '<p>You can now deploy your app to Railway.</p>'
                     '<p>If you received this email, your SMTP settings are correct.</p>'
            )
            
            mail.send(msg)
            
        print("✅ SUCCESS! Email sent successfully!")
        print(f"📬 Check your inbox at: {mail_username}")
        print("\n🚀 Your email configuration is working!")
        print("   You can now deploy to Railway with these settings.")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED to send email!")
        print(f"   Error: {str(e)}")
        print("\n🔍 Common issues:")
        print("   1. MAIL_PASSWORD is not an App Password (must be 16 characters)")
        print("   2. 2-Step Verification not enabled on Gmail")
        print("   3. Wrong email/password")
        print("   4. Firewall blocking SMTP port 587")
        print("\n📖 See RAILWAY_PRODUCTION_SETUP.md for detailed instructions")
        return False

if __name__ == '__main__':
    success = test_email()
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TESTS FAILED - Please fix the issues above")
    print("=" * 60)
    exit(0 if success else 1)

