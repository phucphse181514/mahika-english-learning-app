from app import create_app
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Create application instance
application = create_app()
app = application

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['1', 'true', 'yes']
    app.run(debug=debug, host='0.0.0.0', port=port)
