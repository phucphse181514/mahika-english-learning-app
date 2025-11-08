from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from app import db, mail
from app.models import User
from datetime import datetime, timezone, timedelta
from threading import Thread
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ================================================================
# FIX: Prevent Gunicorn worker timeouts when sending emails on Railway
# ================================================================
# Reason:
#   Railway kills Flask workers if a request runs longer than ~30s.
#   The mail.send() function blocks while connecting to SMTP server,
#   which makes the worker hang and causes "WORKER TIMEOUT" errors.
# Solution:
#   Send emails asynchronously in a background thread so Flask can
#   return a response immediately while the email is sent in parallel.
# ================================================================

def send_async_email(app, msg):
    """Send email in a background thread to avoid blocking requests."""
    with app.app_context():
        try:
            app.logger.info(f"📧 [EMAIL START] Attempting to send email to {msg.recipients}")
            app.logger.info(f"📧 [EMAIL CONFIG] MAIL_SERVER={app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}")
            app.logger.info(f"📧 [EMAIL CONFIG] MAIL_USE_TLS={app.config.get('MAIL_USE_TLS')}, MAIL_USE_SSL={app.config.get('MAIL_USE_SSL')}")
            app.logger.info(f"📧 [EMAIL CONFIG] MAIL_USERNAME={app.config.get('MAIL_USERNAME')}")
            app.logger.info(f"📧 [EMAIL CONFIG] MAIL_DEFAULT_SENDER={app.config.get('MAIL_DEFAULT_SENDER')}")
            app.logger.info(f"📧 [EMAIL DETAILS] Subject: {msg.subject}")
            app.logger.info(f"📧 [EMAIL DETAILS] From: {msg.sender}")
            app.logger.info(f"📧 [EMAIL DETAILS] To: {msg.recipients}")
            
            mail.send(msg)
            
            app.logger.info(f"✅ [EMAIL SUCCESS] Email sent successfully to {msg.recipients}")
            app.logger.info(f"✅ [EMAIL SUCCESS] Subject: {msg.subject}")
        except Exception as e:
            app.logger.error(f"❌ [EMAIL ERROR] Failed to send email to {msg.recipients}")
            app.logger.error(f"❌ [EMAIL ERROR] Subject: {msg.subject}")
            app.logger.error(f"❌ [EMAIL ERROR] Error type: {type(e).__name__}")
            app.logger.error(f"❌ [EMAIL ERROR] Error message: {str(e)}")
            app.logger.error(f"❌ [EMAIL ERROR] Full traceback:", exc_info=True)

def get_vietnam_time():
    """Get current time in Vietnam timezone (UTC+7)"""
    vietnam_tz = timezone(timedelta(hours=7))
    vietnam_time = datetime.now(vietnam_tz)
    return vietnam_time.strftime('%d/%m/%Y lúc %H:%M:%S (UTC+7)')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Mật khẩu phải có ít nhất 8 ký tự"
    if not re.search(r'[A-Z]', password):
        return False, "Mật khẩu phải có ít nhất 1 chữ hoa"
    if not re.search(r'[a-z]', password):
        return False, "Mật khẩu phải có ít nhất 1 chữ thường"
    if not re.search(r'[0-9]', password):
        return False, "Mật khẩu phải có ít nhất 1 số"
    return True, "Mật khẩu hợp lệ"

def send_verification_email(user):
    """Send email verification asynchronously"""
    try:
        current_app.logger.info(f"🔵 [VERIFICATION EMAIL] Starting verification email process for user: {user.email}")
        
        token = user.generate_verification_token()
        current_app.logger.info(f"🔵 [VERIFICATION EMAIL] Token generated successfully for {user.email}")
        
        verification_url = url_for('auth.verify_email', token=token, _external=True)
        current_app.logger.info(f"🔵 [VERIFICATION EMAIL] Verification URL: {verification_url}")
        
        current_time_vn = get_vietnam_time()
        
        msg = Message(
            subject='Xác thực tài khoản Mahika của bạn',
            recipients=[user.email],
            html=render_template('emails/verification.html', 
                               user=user, 
                               verification_url=verification_url,
                               current_time_vn=current_time_vn),
            body=f'Vui lòng truy cập liên kết sau để xác thực tài khoản: {verification_url}'
        )
        
        current_app.logger.info(f"🔵 [VERIFICATION EMAIL] Email message prepared for {user.email}")
        current_app.logger.info(f"🔵 [VERIFICATION EMAIL] Starting background thread to send email...")
        
        # Send email asynchronously to prevent blocking
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
        
        current_app.logger.info(f"✅ [VERIFICATION EMAIL] Background thread started successfully for {user.email}")
        return True
    except Exception as e:
        current_app.logger.error(f'❌ [VERIFICATION EMAIL] Error preparing verification email for {user.email}')
        current_app.logger.error(f'❌ [VERIFICATION EMAIL] Error: {str(e)}', exc_info=True)
        return False

def send_reset_email(user):
    """Send password reset email asynchronously"""
    try:
        current_app.logger.info(f"🔵 [RESET EMAIL] Starting password reset email process for user: {user.email}")
        
        token = user.generate_reset_token()
        current_app.logger.info(f"🔵 [RESET EMAIL] Token generated successfully for {user.email}")
        
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        current_app.logger.info(f"🔵 [RESET EMAIL] Reset URL: {reset_url}")
        
        current_time_vn = get_vietnam_time()
        
        msg = Message(
            subject='Đặt lại mật khẩu Mahika',
            recipients=[user.email],
            html=render_template('emails/reset_password.html', 
                               user=user, 
                               reset_url=reset_url,
                               current_time_vn=current_time_vn),
            body=f'Vui lòng truy cập liên kết sau để đặt lại mật khẩu: {reset_url}'
        )
        
        current_app.logger.info(f"🔵 [RESET EMAIL] Email message prepared for {user.email}")
        current_app.logger.info(f"🔵 [RESET EMAIL] Starting background thread to send email...")
        
        # Send email asynchronously to prevent blocking
        Thread(
            target=send_async_email,
            args=(current_app._get_current_object(), msg)
        ).start()
        
        current_app.logger.info(f"✅ [RESET EMAIL] Background thread started successfully for {user.email}")
        return True
    except Exception as e:
        current_app.logger.error(f'❌ [RESET EMAIL] Error preparing reset email for {user.email}')
        current_app.logger.error(f'❌ [RESET EMAIL] Error: {str(e)}', exc_info=True)
        return False

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not email or not password:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template('auth/register.html')
        
        if not validate_email(email):
            flash('Email không hợp lệ', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'error')
            return render_template('auth/register.html')
        
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('auth/register.html')
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email này đã được đăng ký', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        try:
            current_app.logger.info(f"🔵 [REGISTER] Creating new user with email: {email}")
            
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            current_app.logger.info(f"✅ [REGISTER] User created successfully: {email}")
            current_app.logger.info(f"🔵 [REGISTER] Attempting to send verification email to: {email}")
            
            # Send verification email asynchronously
            email_sent = send_verification_email(user)
            
            if email_sent:
                current_app.logger.info(f"✅ [REGISTER] Verification email process initiated for: {email}")
                flash('Đăng ký thành công! Email xác thực đang được gửi, vui lòng kiểm tra hộp thư.', 'success')
            else:
                current_app.logger.error(f"❌ [REGISTER] Failed to initiate verification email for: {email}")
                flash('Đăng ký thành công! Tuy nhiên không thể gửi email xác thực. Vui lòng liên hệ admin.', 'warning')
            
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'❌ [REGISTER] Registration error for {email}: {str(e)}', exc_info=True)
            flash('Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.', 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not email or not password:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email hoặc mật khẩu không đúng', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Đã đăng xuất thành công', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify email address"""
    user = User.verify_verification_token(token)
    if not user:
        flash('Link xác thực không hợp lệ hoặc đã hết hạn', 'error')
        return redirect(url_for('auth.login'))
    
    if user.is_verified:
        flash('Tài khoản đã được xác thực trước đó', 'info')
        return redirect(url_for('auth.login'))
    
    user.is_verified = True
    user.verified_at = datetime.utcnow()
    db.session.commit()
    
    flash('Xác thực email thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        if not email:
            flash('Vui lòng nhập email', 'error')
            return render_template('auth/forgot_password.html')
        
        current_app.logger.info(f"🔵 [FORGOT PASSWORD] Password reset requested for: {email}")
        
        user = User.query.filter_by(email=email).first()
        if user:
            current_app.logger.info(f"🔵 [FORGOT PASSWORD] User found, sending reset email to: {email}")
            email_sent = send_reset_email(user)
            if not email_sent:
                current_app.logger.error(f'❌ [FORGOT PASSWORD] Failed to send reset email to {email}')
        else:
            current_app.logger.info(f"⚠️ [FORGOT PASSWORD] User not found for email: {email} (security: still showing success message)")
        
        # Always show success message for security
        flash('Nếu email tồn tại, chúng tôi đã gửi hướng dẫn đặt lại mật khẩu.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_reset_token(token)
    if not user:
        flash('Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        user.set_password(password)
        db.session.commit()
        
        flash('Đặt lại mật khẩu thành công! Bạn có thể đăng nhập với mật khẩu mới.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)

@auth_bp.route('/resend-verification')
@login_required
def resend_verification():
    """Resend verification email"""
    if current_user.is_verified:
        flash('Tài khoản đã được xác thực', 'info')
        return redirect(url_for('main.dashboard'))
    
    current_app.logger.info(f"🔵 [RESEND VERIFICATION] User {current_user.email} requested resend verification email")
    
    email_sent = send_verification_email(current_user)
    
    if email_sent:
        current_app.logger.info(f"✅ [RESEND VERIFICATION] Verification email process initiated for: {current_user.email}")
        flash('Email xác thực đang được gửi. Vui lòng kiểm tra hộp thư trong vài phút.', 'success')
    else:
        current_app.logger.error(f"❌ [RESEND VERIFICATION] Failed to initiate verification email for: {current_user.email}")
        flash('Không thể gửi email xác thực. Vui lòng thử lại sau hoặc liên hệ admin.', 'error')
    
    return redirect(url_for('main.dashboard'))
