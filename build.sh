#!/bin/bash
set -o errexit

echo "🚀 Starting NutriAI build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"

# Initialize database and populate data
echo "🗄️ Initializing database..."
python init_admin.py

echo "🍎 Populating food database..."
python populate_foods.py

echo "✅ Build completed successfully!"
