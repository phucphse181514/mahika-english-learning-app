#!/usr/bin/env python3
"""Initialize the database (create tables).

Usage (from Railway):
  python scripts/init_db.py

Usage (from local with Railway CLI):
  railway run -- python scripts/init_db.py
"""
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db


def main():
    app = create_app()
    with app.app_context():
        try:
            print('Creating database tables...')
            db.create_all()
            print('✓ Database tables created successfully.')
        except Exception as e:
            print('✗ ERROR: Failed to create database tables:')
            print(e)
            sys.exit(1)


if __name__ == '__main__':
    main()
