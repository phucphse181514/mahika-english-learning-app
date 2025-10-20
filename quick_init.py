#!/usr/bin/env python3
"""
Quick DB init - no dependencies needed
Run with: railway run python quick_init.py
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Don't load .env - Railway provides env vars
from app import create_app, db


def main():
    print('Creating Flask app...')
    app = create_app()
    
    with app.app_context():
        try:
            print('Creating database tables...')
            db.create_all()
            print('✓ Tables created successfully!')
            
            # Show tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f'\nCreated tables: {tables}')
            
        except Exception as e:
            print(f'✗ Error: {e}')
            sys.exit(1)


if __name__ == '__main__':
    main()
