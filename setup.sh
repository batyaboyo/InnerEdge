#!/bin/bash

# InnerEdge Setup Script

set -e

echo "🚀 InnerEdge CFD SaaS - Setup Script"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python $(python3 --version) found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Python dependencies installed"

# Create environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Edit .env file with your settings"
else
    echo "✅ .env file already exists"
fi

# Run migrations
echo "🔧 Running Django migrations..."
python manage.py migrate --noinput

# Create superuser (optional)
read -p "Create superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Seed test data
echo "🌱 Seeding test data..."
python manage.py seed_assets > /dev/null 2>&1 || true
python manage.py seed_plans > /dev/null 2>&1 || true
python manage.py seed_tags > /dev/null 2>&1 || true
echo "✅ Test data seeded"

# Install frontend dependencies
if [ -d "frontend" ]; then
    echo "📥 Installing frontend dependencies..."
    cd frontend
    npm install > /dev/null 2>&1
    echo "✅ Frontend dependencies installed"
    cd ..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env with your settings"
echo "2. Start backend: python manage.py runserver"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Visit http://localhost:3000"
echo ""
echo "🧪 Run tests: pytest"
echo "🐳 Docker: docker-compose up -d"
echo ""
