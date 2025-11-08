from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
import os
import logging
import sys

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging for Railway and local development
    # Railway captures stdout/stderr, so we log to console
    if not app.debug:
        # Set logging level
        app.logger.setLevel(logging.INFO)
        
        # Console handler for Railway logs
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Format with emoji for easy identification
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler
        app.logger.addHandler(console_handler)
        
        app.logger.info('=' * 80)
        app.logger.info('🚀 Mahika English Learning App Starting...')
        app.logger.info(f'🔧 Environment: {"Production" if not app.debug else "Development"}')
        app.logger.info(f'📧 Mail Server: {app.config.get("MAIL_SERVER")}:{app.config.get("MAIL_PORT")}')
        app.logger.info(f'📧 Mail Username: {app.config.get("MAIL_USERNAME")}')
        app.logger.info(f'📧 Mail Default Sender: {app.config.get("MAIL_DEFAULT_SENDER")}')
        app.logger.info(f'📧 Mail Use TLS: {app.config.get("MAIL_USE_TLS")}')
        app.logger.info(f'🗄️  Database: {app.config.get("DB_HOST")}:{app.config.get("DB_PORT")}/{app.config.get("DB_NAME")}')
        app.logger.info('=' * 80)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from app.models import User, Payment
      # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.payment import payment_bp
    from app.routes.admin import admin_bp
    from app.routes.test import test_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(test_bp)
    
    # Create database tables (wrapped to avoid crash if DB unreachable)
    skip_db_init = os.environ.get('SKIP_DB_INIT', 'False').lower() in ['1', 'true', 'yes']
    if not skip_db_init:
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                app.logger.error(f"Database initialization skipped due to error: {e}")
    else:
        app.logger.info('SKIP_DB_INIT is set, skipping automatic db.create_all()')
    
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
