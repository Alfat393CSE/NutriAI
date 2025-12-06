# NutriAI Deployment Guide for Render.com

## Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

1. **Fork/Push this repository to your GitHub account**
2. **Go to [Render Dashboard](https://dashboard.render.com/)**
3. **Click "New +" and select "Web Service"**
4. **Connect your GitHub repository (NutriAI)**
5. **Configure the service:**
   - **Name:** `nutriai`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `gunicorn app_new:app`
   - **Instance Type:** Free (or paid for better performance)

6. **Add Environment Variables:**
   - `SECRET_KEY` - Auto-generate or set your own secure key
   - `PYTHON_VERSION` - `3.11.0`

7. **Click "Create Web Service"**

### Option 2: Using render.yaml (Infrastructure as Code)

1. Push this repository to GitHub
2. Go to Render Dashboard
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will automatically detect `render.yaml` and set up everything

## What's Included

The following files have been added for deployment:

- **`gunicorn_config.py`** - Gunicorn WSGI server configuration
- **`build.sh`** - Build script for Render (installs dependencies and initializes DB)
- **`Procfile`** - Process file for running the app
- **`runtime.txt`** - Python version specification
- **`render.yaml`** - Render service configuration (optional)
- **`.gitignore`** - Git ignore file for Python projects

## Manual Configuration Steps

If using manual setup on Render:

### 1. Create Web Service

```
Name: nutriai
Environment: Python 3
Region: Choose closest to your users
Branch: main
Build Command: pip install --upgrade pip && pip install -r requirements.txt
Start Command: gunicorn app_new:app
```

### 2. Environment Variables

Add these in Render Dashboard → Environment:

```
SECRET_KEY=your-auto-generated-secret-key
PYTHON_VERSION=3.11.0
```

**Note:** Database initialization will happen automatically on first run when the app starts.

### 3. Database (Optional - Using PostgreSQL)

For production with PostgreSQL:
1. Create a PostgreSQL database in Render
2. Add `DATABASE_URL` environment variable (auto-provided by Render)
3. The app will automatically use PostgreSQL instead of SQLite

## Features

- ✅ Automatic database initialization
- ✅ Pre-populated food database
- ✅ Admin account creation
- ✅ Environment-based configuration
- ✅ PostgreSQL support (production)
- ✅ SQLite support (development)
- ✅ HTTPS/SSL ready
- ✅ CORS enabled

## Default Admin Credentials

After deployment, login with:
- **Username:** `admin`
- **Password:** `admin123`

**⚠️ IMPORTANT:** Change the admin password immediately after first login!

## Post-Deployment

1. **Visit your app:** `https://your-app-name.onrender.com`
2. **Login as admin** and change the password
3. **Test all features:**
   - User registration
   - Food search
   - Meal planner
   - Chatbot
   - Recommendations

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure all dependencies in `requirements.txt` are compatible
- Verify Python version matches `runtime.txt`

### Database Issues
- For PostgreSQL: Ensure `DATABASE_URL` is set
- For SQLite: Check file permissions (SQLite works on Render but data resets on redeploy)

### App Crashes
- Check application logs in Render dashboard
- Verify environment variables are set correctly
- Ensure `SECRET_KEY` is configured

## Scaling

Render Free Tier limitations:
- Sleeps after 15 minutes of inactivity
- 750 hours/month free
- 512 MB RAM

For production:
- Upgrade to paid tier
- Use PostgreSQL database
- Enable auto-scaling
- Set up custom domain

## Support

For issues:
- Check Render logs
- Review this deployment guide
- Contact: alfattasnimhasan@gmail.com

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_admin.py
python populate_foods.py

# Run app
python app_new.py
```

Visit `http://localhost:5000`

---

Created by Alfat Tasnim Hasan | Contact: 01736276082 | alfattasnimhasan@gmail.com
