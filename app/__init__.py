from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
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
