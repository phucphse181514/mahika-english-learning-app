#!/usr/bin/env python3
"""Create or update an admin user.

Usage (from Railway):
  python scripts/create_admin.py --email admin@example.com --password Secret123

Usage (from local with Railway CLI):
  railway run -- python scripts/create_admin.py --email admin@example.com --password Secret123
"""
import os
import sys
import argparse

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import User


def create_or_update_admin(email: str, password: str):
    app = create_app()
    with app.app_context():
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                print(f'Updating existing user {email}')
                user.set_password(password)
                user.is_admin = True
                user.is_verified = True
                user.has_paid = True
            else:
                print(f'Creating new admin user {email}')
                user = User(email=email, is_verified=True, has_paid=True, is_admin=True)
                user.set_password(password)
                db.session.add(user)

            db.session.commit()
            print('✓ Admin user is ready.')
        except Exception as e:
            print('✗ ERROR: Failed to create admin:')
            print(e)
            sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--email', required=True, help='Admin email')
    p.add_argument('--password', required=True, help='Admin password')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    create_or_update_admin(args.email, args.password)
