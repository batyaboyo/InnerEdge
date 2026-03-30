@echo off
REM InnerEdge Setup Script for Windows

echo.
echo 🚀 InnerEdge CFD SaaS - Setup Script (Windows)
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Install dependencies
echo 📥 Installing Python dependencies...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo ✅ Python dependencies installed

REM Create environment file
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Edit .env file with your settings
) else (
    echo ✅ .env file already exists
)

REM Run migrations
echo 🔧 Running Django migrations...
python manage.py migrate --noinput

REM Seed test data
echo 🌱 Seeding test data...
python manage.py seed_assets >nul 2>&1
python manage.py seed_plans >nul 2>&1
python manage.py seed_tags >nul 2>&1
echo ✅ Test data seeded

REM Install frontend dependencies
if exist "frontend" (
    echo 📥 Installing frontend dependencies...
    cd frontend
    call npm install >nul 2>&1
    echo ✅ Frontend dependencies installed
    cd ..
)

echo.
echo ✅ Setup complete!
echo.
echo 📚 Next steps:
echo 1. Edit .env with your settings
echo 2. Start backend: python manage.py runserver
echo 3. Start frontend: cd frontend ^&^& npm run dev
echo 4. Visit http://localhost:3000
echo.
echo 🧪 Run tests: pytest
echo 🐳 Docker: docker-compose up -d
echo.
