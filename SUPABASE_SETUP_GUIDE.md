# 🔗 Supabase Database Setup Guide

## Step 1: Create Supabase Project

1. **Go to Supabase**: Visit [https://supabase.com](https://supabase.com)
2. **Sign Up/Login**: Create account or login
3. **Create New Project**: Click "New Project"
4. **Project Details**:
   - Name: `ayurdiet-database`
   - Database Password: Choose a strong password (save this!)
   - Region: Choose closest to your location
5. **Wait for Setup**: Project creation takes 2-3 minutes

## Step 2: Get Database Credentials

Once your project is ready:

1. **Go to Settings** → **Database**
2. **Copy Connection Info**:
   - Host: `db.xxxxxxxxxxxxx.supabase.co`
   - Database name: `postgres`
   - Username: `postgres`
   - Password: [Your chosen password]
   - Port: `5432`

## Step 3: Update Your .env File

Replace the placeholder values in your `.env` file:

```env
# Database Configuration for Supabase PostgreSQL
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432

# Optional: Complete DATABASE_URL (choose one method)
# DATABASE_URL=postgresql://postgres:your_password@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

## Step 4: Update Django Settings

Uncomment the Supabase database configuration in `settings.py`:

```python
# Comment out SQLite
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Uncomment Supabase PostgreSQL
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f"postgresql://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
    )
}
```

## Step 5: Test Connection & Setup Database

```bash
# Test database connection
python manage.py dbshell

# If connection works, create migrations
python manage.py makemigrations

# Apply migrations to create tables
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

## Step 6: Load Food Dataset

```bash
# Preview what will be loaded (dry run)
python manage.py load_food_data --dry-run

# Load the complete food dataset
python manage.py load_food_data

# If you need to clear and reload
python manage.py load_food_data --clear
```

## Step 7: Verify Everything Works

```bash
# Test in Django shell
python manage.py shell
>>> from diet_planner.models import Food
>>> Food.objects.count()  # Should show 100+ foods
>>> Food.objects.filter(virya='Cooling').count()  # Test filtering

# Start server and test
python manage.py runserver
# Visit: http://localhost:8000/admin/ (login with superuser)
# Visit: http://localhost:8000/api/foods/ (test API)
```

## 🎯 Quick Setup Commands

Once you have Supabase credentials, run these commands in order:

```bash
# 1. Navigate to project
cd c:\Users\sneha\ayurdiet_backend

# 2. Update .env file with your Supabase credentials
# (Edit the file manually with your actual values)

# 3. Create and apply migrations
C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe manage.py makemigrations
C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe manage.py migrate

# 4. Create superuser
C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe manage.py createsuperuser

# 5. Load food dataset
C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe manage.py load_food_data

# 6. Start server
C:/Users/sneha/ayurdiet_backend/venv/Scripts/python.exe manage.py runserver
```

## 🔍 Troubleshooting

### Connection Issues
- **Error**: `FATAL: password authentication failed`
  - **Solution**: Double-check password in `.env` file
  
- **Error**: `could not connect to server`
  - **Solution**: Verify host URL is correct
  - **Check**: Supabase project is running (not paused)

### Migration Issues
- **Error**: `relation already exists`
  - **Solution**: Database might have existing tables
  - **Try**: `python manage.py migrate --fake-initial`

### Food Loading Issues
- **Error**: `Food matching query does not exist`
  - **Solution**: Make sure migrations ran successfully
  - **Check**: `python manage.py showmigrations`

## 📊 Expected Results

After successful setup:
- ✅ **Database**: PostgreSQL on Supabase
- ✅ **Tables**: Users, Patients, Foods, Diet Plans
- ✅ **Food Items**: 100+ items with Ayurvedic properties
- ✅ **Admin Panel**: Accessible at localhost:8000/admin
- ✅ **API**: Food search and filtering working
- ✅ **Authentication**: JWT tokens working

## 🚀 Next Steps After Setup

1. **Test Food Search**: Use the API to search foods by Ayurvedic properties
2. **Create Sample Patients**: Add test patients through admin panel
3. **Generate Diet Plans**: Test the diet plan generation
4. **Frontend Integration**: Connect your React frontend to the API
5. **Scale Up**: Add more food items to reach 8000+ target

---

**Need Help?** Check the troubleshooting section or ask specific questions about any setup step!