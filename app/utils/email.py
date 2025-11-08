"""
Email utility using Brevo API with detailed logging
Fallback to SMTP if Brevo API fails
"""

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import current_app
from flask_mail import Message
from threading import Thread


def send_email_via_brevo_api(to_email, subject, html_content, sender_name="Mahika English Learning"):
    """
    Send email using Brevo (Sendinblue) API with detailed logging
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        sender_name: Name to display as sender
    
    Returns:
        dict: {'success': bool, 'message': str, 'message_id': str or None}
    """
    try:
        # Check if API key is configured
        api_key = current_app.config.get('BREVO_API_KEY')
        if not api_key:
            current_app.logger.error("❌ [BREVO API] BREVO_API_KEY is not configured")
            return {
                'success': False,
                'message': 'Brevo API Key is not configured',
                'message_id': None
            }
        
        current_app.logger.info(f"📧 [BREVO API] Starting email send to: {to_email}")
        current_app.logger.info(f"📧 [BREVO API] Subject: {subject}")
        current_app.logger.info(f"📧 [BREVO API] Sender: {sender_name} <{current_app.config.get('MAIL_DEFAULT_SENDER')}>")
        
        # Configure Brevo API
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        
        # Prepare email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={
                "name": sender_name, 
                "email": current_app.config.get('MAIL_DEFAULT_SENDER')
            },
            subject=subject,
            html_content=html_content
        )
        
        current_app.logger.info(f"📧 [BREVO API] Sending email via Brevo API...")
        
        # Send email
        api_response = api_instance.send_transac_email(send_smtp_email)
        
        current_app.logger.info(f"✅ [BREVO API] Email sent successfully to {to_email}")
        current_app.logger.info(f"✅ [BREVO API] Message ID: {api_response.message_id}")
        
        return {
            'success': True,
            'message': 'Email sent successfully via Brevo API',
            'message_id': api_response.message_id
        }
        
    except ApiException as e:
        error_body = e.body if hasattr(e, 'body') else str(e)
        current_app.logger.error(f"❌ [BREVO API] API Exception when sending email to {to_email}")
        current_app.logger.error(f"❌ [BREVO API] Status: {e.status if hasattr(e, 'status') else 'Unknown'}")
        current_app.logger.error(f"❌ [BREVO API] Reason: {e.reason if hasattr(e, 'reason') else 'Unknown'}")
        current_app.logger.error(f"❌ [BREVO API] Body: {error_body}")
        
        return {
            'success': False,
            'message': f'Brevo API error: {error_body}',
            'message_id': None
        }
        
    except Exception as e:
        current_app.logger.error(f"❌ [BREVO API] Unexpected error sending email to {to_email}: {str(e)}")
        current_app.logger.exception(e)
        
        return {
            'success': False,
            'message': f'Unexpected error: {str(e)}',
            'message_id': None
        }


def send_async_email_smtp(app, msg):
    """Send email via SMTP in background thread (fallback method)"""
    with app.app_context():
        try:
            from app import mail
            
            app.logger.info(f"📧 [SMTP FALLBACK] Attempting to send email to {msg.recipients}")
            app.logger.info(f"📧 [SMTP FALLBACK] MAIL_SERVER={app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}")
            
            mail.send(msg)
            
            app.logger.info(f"✅ [SMTP FALLBACK] Email sent successfully to {msg.recipients}")
            
        except Exception as e:
            app.logger.error(f"❌ [SMTP FALLBACK] Failed to send email to {msg.recipients}")
            app.logger.error(f"❌ [SMTP FALLBACK] Error: {str(e)}", exc_info=True)


def send_email_via_smtp(to_email, subject, html_content, text_content=None):
    """
    Send email using Flask-Mail (SMTP) as fallback
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (optional)
    
    Returns:
        dict: {'success': bool, 'message': str, 'message_id': str or None}
    """
    try:
        from app import mail
        
        current_app.logger.info(f"📧 [SMTP] Preparing email to {to_email}")
        
        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=html_content,
            body=text_content or html_content
        )
        
        # Send asynchronously to prevent blocking
        Thread(
            target=send_async_email_smtp,
            args=(current_app._get_current_object(), msg)
        ).start()
        
        current_app.logger.info(f"✅ [SMTP] Background thread started for {to_email}")
        
        return {
            'success': True,
            'message': 'Email queued for sending via SMTP',
            'message_id': None
        }
        
    except Exception as e:
        current_app.logger.error(f"❌ [SMTP] Error preparing email to {to_email}: {str(e)}", exc_info=True)
        
        return {
            'success': False,
            'message': f'SMTP error: {str(e)}',
            'message_id': None
        }


def send_email(to_email, subject, html_content, text_content=None, sender_name="Mahika English Learning"):
    """
    Smart email sender - tries Brevo API first, falls back to SMTP if needed
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        text_content: Plain text content (optional)
        sender_name: Name to display as sender
    
    Returns:
        dict: {'success': bool, 'message': str, 'message_id': str or None}
    """
    current_app.logger.info(f"📧 [EMAIL SENDER] Starting email process to: {to_email}")
    current_app.logger.info(f"📧 [EMAIL SENDER] Subject: {subject}")
    
    # Try Brevo API first if configured
    if current_app.config.get('BREVO_API_KEY'):
        current_app.logger.info("📧 [EMAIL SENDER] Using Brevo API (primary method)")
        result = send_email_via_brevo_api(to_email, subject, html_content, sender_name)
        
        if result['success']:
            current_app.logger.info(f"✅ [EMAIL SENDER] Email sent successfully via Brevo API")
            return result
        else:
            current_app.logger.warning(f"⚠️ [EMAIL SENDER] Brevo API failed: {result['message']}")
            current_app.logger.info("⚠️ [EMAIL SENDER] Attempting SMTP fallback...")
    else:
        current_app.logger.info("📧 [EMAIL SENDER] Brevo API Key not configured, using SMTP")
    
    # Fallback to SMTP
    result = send_email_via_smtp(to_email, subject, html_content, text_content)
    
    if result['success']:
        current_app.logger.info(f"✅ [EMAIL SENDER] Email sent successfully via SMTP fallback")
    else:
        current_app.logger.error(f"❌ [EMAIL SENDER] All email methods failed")
    
    return result
