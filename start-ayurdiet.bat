@echo off
echo 🚀 Starting AyurDiet Application (Frontend + Backend)
echo.

echo 📱 Starting Django Backend Server...
echo Backend will be available at: http://localhost:8000
echo.

start cmd /k "cd /d c:\Users\sneha\ayurdiet_backend && python manage.py runserver"

echo.
echo ⏳ Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo 🌐 Instructions for React Frontend:
echo 1. Open a new terminal in your React app directory
echo 2. Run: npm run dev (or yarn dev)
echo 3. Your React app will be available at: http://localhost:5173
echo.

echo 🔍 Available Services:
echo - Django Backend: http://localhost:8000
echo - Django Admin: http://localhost:8000/admin/
echo - API Documentation: http://localhost:8000/swagger/
echo - React Frontend: http://localhost:5173 (after starting)
echo.

echo 🧪 Testing Integration:
echo - Visit the Backend Integration Test page in your React app
echo - Test login with: admin / admin123
echo.

echo ✅ Backend server started! Now start your React frontend.
pause