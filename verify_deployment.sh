#!/bin/bash
# Pre-deployment verification script for NutriAI on Render

echo "🔍 NutriAI - Pre-Deployment Verification"
echo "=========================================="
echo ""

# Check if critical files exist
echo "📋 Checking critical files..."
files=(
    "render.yaml"
    "build.sh"
    "requirements.txt"
    "gunicorn_config.py"
    "Procfile"
    "runtime.txt"
    "app_new.py"
    "models.py"
    "ml_utils.py"
    "recommendation_engine.py"
    "init_admin.py"
    "populate_foods.py"
    ".gitignore"
)

missing_files=()
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING!)"
        missing_files+=("$file")
    fi
done

echo ""

# Check if static folder exists
echo "📁 Checking directories..."
if [ -d "static" ]; then
    echo "  ✅ static/"
else
    echo "  ❌ static/ (MISSING!)"
fi

if [ -d "templates" ]; then
    echo "  ✅ templates/"
else
    echo "  ❌ templates/ (MISSING!)"
fi

echo ""

# Check Python version in runtime.txt
echo "🐍 Checking Python version..."
if [ -f "runtime.txt" ]; then
    python_version=$(cat runtime.txt)
    echo "  ✅ Python version: $python_version"
else
    echo "  ❌ runtime.txt missing"
fi

echo ""

# Check if build.sh is executable
echo "🔧 Checking build.sh permissions..."
if [ -x "build.sh" ]; then
    echo "  ✅ build.sh is executable"
else
    echo "  ⚠️  build.sh is not executable (will be fixed during deployment)"
fi

echo ""

# Summary
echo "=========================================="
if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All critical files present!"
    echo "✅ Ready for Render deployment!"
    echo ""
    echo "Next steps:"
    echo "1. Commit all changes: git add . && git commit -m 'Ready for deployment'"
    echo "2. Push to GitHub: git push origin main"
    echo "3. Deploy on Render: https://dashboard.render.com/"
else
    echo "❌ Missing ${#missing_files[@]} critical file(s):"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please ensure all files are present before deploying."
fi
echo "=========================================="
