#!/bin/bash
set -e

echo "🚀 Installing Django Project Dependencies"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Deactivate any active venv
if command -v deactivate &> /dev/null; then
    echo "Deactivating current virtual environment..."
    deactivate 2>/dev/null || true
fi

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

# Create new venv
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate venv
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To activate the virtual environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "To run the development server:"
echo "  python manage.py runserver"
echo ""
echo "To run tests:"
echo "  python manage.py test"
echo ""
