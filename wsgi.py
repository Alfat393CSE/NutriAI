"""
WSGI Configuration for PythonAnywhere Deployment
"""
import os
import sys

# Add your project directory to the sys.path
# Replace 'YOUR_USERNAME' with your actual PythonAnywhere username
project_home = '/home/YOUR_USERNAME/NutriAI'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables for production
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-to-a-secure-random-key')
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:////home/YOUR_USERNAME/NutriAI/instance/nutriai.db')

# Import Flask app
from app_new import app as application

# This is required for PythonAnywhere
if __name__ == '__main__':
    application.run()
