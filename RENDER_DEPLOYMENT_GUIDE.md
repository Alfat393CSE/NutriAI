# 🚀 NutriAI - Render Deployment Guide

## ✅ Pre-Deployment Checklist

All configuration files are ready for Render deployment:

- ✅ `render.yaml` - Render service configuration
- ✅ `build.sh` - Build script with database initialization
- ✅ `requirements.txt` - All dependencies properly specified
- ✅ `gunicorn_config.py` - Production-ready Gunicorn configuration
- ✅ `Procfile` - Process file for web service
- ✅ `runtime.txt` - Python version (3.11.9)
- ✅ `.gitignore` - Prevents sensitive files from being committed
- ✅ Database initialization in `init_admin.py` and `populate_foods.py`
- ✅ Environment variable handling in `app_new.py`

## 📋 Deployment Steps

### Step 1: Prepare Your Repository

1. **Commit all changes** to your Git repository:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

2. **Ensure your repository is on GitHub** (or GitLab/Bitbucket)

### Step 2: Deploy to Render

#### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select your **NutriAI** repository
5. Render will automatically detect `render.yaml`
6. Click **"Apply"**
7. Render will create your service with all configured settings

#### Option B: Manual Web Service Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `nutriai` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty (unless repo is in subfolder)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app_new:app --config gunicorn_config.py`
   - **Instance Type**: `Free` (or paid for better performance)

5. **Add Environment Variables** (under "Environment" tab):
   - `SECRET_KEY`: Click "Generate" for auto-generated secure key
   - `PYTHON_VERSION`: `3.11.9`
   - `FLASK_ENV`: `production`

6. Click **"Create Web Service"**

### Step 3: Monitor Deployment

1. Watch the **deployment logs** in real-time
2. The build process will:
   - Install Python dependencies
   - Create database tables
   - Initialize admin user
   - Populate food database
   - Start the Gunicorn server

3. Wait for the message: **"Your service is live 🎉"**

### Step 4: Access Your Application

1. Your app will be available at: `https://nutriai.onrender.com` (or your custom URL)
2. **Test the login** with default admin credentials:
   - **Username**: `admin`
   - **Password**: `admin123`

### Step 5: Post-Deployment Security

⚠️ **IMPORTANT**: Change the admin password immediately!

1. Login as admin
2. Go to Profile or Admin Settings
3. Change the password to something secure

## 🔧 Configuration Details

### Environment Variables

Your app uses these environment variables:

| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `SECRET_KEY` | Flask session encryption | Generated | Yes |
| `DATABASE_URL` | Database connection string | SQLite (auto) | No* |
| `PYTHON_VERSION` | Python runtime version | 3.11.9 | Yes |
| `FLASK_ENV` | Flask environment | production | Yes |

*Render can optionally provide PostgreSQL database. For free tier, SQLite works fine.

### Build Process

The `build.sh` script runs automatically and:
1. Upgrades pip, setuptools, and wheel
2. Installs all requirements from `requirements.txt`
3. Creates database tables
4. Initializes admin user (username: admin, password: admin123)
5. Populates database with 300+ food items

### Production Features

✅ **Automatic HTTPS/SSL** - Render provides free SSL certificates
✅ **Auto-deploy on push** - Push to main branch triggers redeployment
✅ **Health checks** - Render monitors your app's availability
✅ **Persistent storage** - Database persists across deployments
✅ **Environment isolation** - Secure environment variable storage
✅ **Zero-downtime deploys** - Render uses rolling deploys

## 🎯 Testing Your Deployment

### 1. Basic Functionality
- [ ] Homepage loads
- [ ] User registration works
- [ ] User login works
- [ ] Admin login works (admin/admin123)

### 2. Core Features
- [ ] Food search returns results
- [ ] Food logging works
- [ ] Dashboard displays correctly
- [ ] Meal planner functional
- [ ] Chatbot responds
- [ ] Nutrition recommendations load

### 3. Admin Features
- [ ] Admin dashboard accessible
- [ ] User management works
- [ ] Food management works
- [ ] System settings accessible

## 🐛 Troubleshooting

### Build Fails

**Problem**: Build fails during dependency installation
**Solution**: Check `requirements.txt` for version conflicts. View logs for specific errors.

### Database Not Initializing

**Problem**: Database tables not created
**Solution**: Ensure `build.sh` has execute permissions. Check if `init_admin.py` and `populate_foods.py` run successfully in logs.

### App Won't Start

**Problem**: Service starts but app crashes immediately
**Solution**: 
1. Check logs for Python errors
2. Verify `app_new:app` is the correct entry point
3. Ensure all imports work correctly

### Port Binding Issues

**Problem**: "Failed to bind to port"
**Solution**: Render automatically provides PORT environment variable. Make sure gunicorn config uses it correctly (already configured).

### Static Files Not Loading

**Problem**: CSS/JS files return 404
**Solution**: Ensure `static/` folder is committed to git and not in `.gitignore`

## 📊 Monitoring & Logs

### View Logs
1. Go to your service in Render Dashboard
2. Click "Logs" tab
3. View real-time application logs

### Metrics
Render provides:
- Request count
- Response times
- Memory usage
- CPU usage

## 🔄 Updating Your App

### Deploy Updates
```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically:
1. Detect the push
2. Start a new build
3. Run build.sh
4. Deploy the new version
5. Switch traffic to new version

### Manual Deploy
In Render Dashboard:
1. Go to your service
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

## 🆙 Upgrading to Paid Tier

Free tier limitations:
- Service spins down after inactivity
- Limited resources
- Cold start delays

Paid tier benefits:
- Always-on service
- More RAM & CPU
- Faster response times
- Custom domains
- No cold starts

To upgrade:
1. Go to service settings
2. Change Instance Type
3. Confirm billing

## 🔐 Security Best Practices

1. ✅ Change default admin password immediately
2. ✅ Use strong, unique SECRET_KEY (auto-generated)
3. ✅ Enable 2FA on your Render account
4. ✅ Regularly update dependencies
5. ✅ Monitor logs for suspicious activity
6. ✅ Use environment variables for all secrets
7. ✅ Never commit .env files or secrets to git

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 🎉 Success!

Your NutriAI app should now be live on Render! 

**Live URL**: https://[your-service-name].onrender.com

**Admin Credentials**:
- Username: `admin`
- Password: `admin123` (⚠️ **CHANGE THIS IMMEDIATELY**)

---

**Need Help?**
- Check Render logs for errors
- Review this guide's troubleshooting section
- Contact Render support for platform issues

**Happy Deploying! 🚀**
