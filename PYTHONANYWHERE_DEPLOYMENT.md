# NutriAI Deployment Guide for PythonAnywhere

## Prerequisites
- PythonAnywhere account (free or paid)
- Your code pushed to GitHub: `https://github.com/Alfat393CSE/NutriAI.git`

## Step-by-Step Deployment

### 1. Create PythonAnywhere Account
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account (or login if you have one)

### 2. Open Bash Console
1. From PythonAnywhere Dashboard, click **"Consoles"**
2. Click **"Bash"** to open a new bash console

### 3. Clone Your Repository

```bash
# Clone your repository
git clone https://github.com/Alfat393CSE/NutriAI.git
cd NutriAI
```

### 4. Create Virtual Environment

```bash
# Create virtual environment with Python 3.11
mkvirtualenv --python=/usr/bin/python3.11 nutriai-env

# If you get errors, the virtualenv might be corrupted. Recreate it:
# deactivate
# rmvirtualenv nutriai-env
# mkvirtualenv --python=/usr/bin/python3.11 nutriai-env

# Activate it (if not already activated)
workon nutriai-env
```

### 5. Install Dependencies

```bash
# Install requirements (use python -m pip if regular pip fails)
python -m pip install -r requirements.txt

# If above fails with _posixsubprocess error, recreate virtual environment:
# deactivate
# rmvirtualenv nutriai-env  
# mkvirtualenv --python=/usr/bin/python3.11 nutriai-env
# pip install -r requirements.txt
```

### 6. Initialize Database

```bash
# Run initialization scripts
python init_admin.py
python populate_foods.py
```

### 7. Create WSGI Configuration File

1. Go to **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (not Flask)
4. Select **Python 3.11**
5. Click through to create the app

### 8. Configure WSGI File

1. In the **Web** tab, scroll to **"Code"** section
2. Click on the **WSGI configuration file** link
3. **Delete all content** and replace with:

```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/NutriAI'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here-change-this'
os.environ['DATABASE_URL'] = 'sqlite:////home/YOUR_USERNAME/NutriAI/instance/nutriai.db'

# Import flask app
from app_new import app as application
```

**Important:** Replace `YOUR_USERNAME` with your PythonAnywhere username!

### 9. Configure Virtual Environment

1. In the **Web** tab, scroll to **"Virtualenv"** section
2. Enter the path: `/home/YOUR_USERNAME/.virtualenvs/nutriai-env`
3. Replace `YOUR_USERNAME` with your actual username

### 10. Set Static Files

In the **Web** tab, scroll to **"Static files"** section and add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/NutriAI/static` |

Replace `YOUR_USERNAME` with your actual username.

### 11. Reload Web App

1. Scroll to top of **Web** tab
2. Click the big green **"Reload"** button
3. Wait for reload to complete

### 12. Test Your App

1. Click on your app URL (e.g., `YOUR_USERNAME.pythonanywhere.com`)
2. You should see the NutriAI home page
3. Login with default admin credentials:
   - Username: `admin`
   - Password: `admin123`

## Important Notes

### Free Account Limitations
- One web app only
- Limited CPU time per day
- App sleeps after 3 months of inactivity
- HTTPS available, custom domains not available

### Database Location
- Database will be at: `/home/YOUR_USERNAME/NutriAI/instance/nutriai.db`
- Make sure the `instance` folder has write permissions

### Updating Your App

When you make changes to your code:

```bash
# Open bash console
cd ~/NutriAI

# Pull latest changes
git pull origin main

# Reinstall dependencies if requirements changed
workon nutriai-env
pip install -r requirements.txt

# Run any new migrations/updates
python init_admin.py
python populate_foods.py
```

Then reload your web app from the Web tab.

## Troubleshooting

### Error: "ModuleNotFoundError: No module named '_posixsubprocess'"
This is a pip corruption issue on PythonAnywhere. Fix it:
```bash
# Reinstall pip in the virtual environment
python -m pip install --force-reinstall pip

# Or use curl method
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm get-pip.py
```

### Error: "No module named 'flask'"
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### Error: "Could not find application"
- Check WSGI file has correct paths
- Verify username is correct in all paths
- Make sure `app_new.py` is in the NutriAI folder

### Error: "Database is locked"
- SQLite doesn't handle concurrent writes well
- Consider upgrading to paid plan for MySQL
- Or use a different database service

### Error: "Permission denied"
- Check file permissions: `chmod -R 755 ~/NutriAI`
- Ensure instance folder is writable: `chmod -R 777 ~/NutriAI/instance`

### Static Files Not Loading
- Verify static files path in Web tab
- Check URL path starts with `/static/`
- Reload web app after changes

## Environment Variables

For security, set these in WSGI file:

```python
os.environ['SECRET_KEY'] = 'generate-a-secure-random-key'
```

Generate a secure key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Performance Tips

### Free Account
- Optimize database queries
- Use caching where possible
- Minimize external API calls

### Paid Account
- Upgrade for more CPU time
- Use MySQL instead of SQLite
- Enable always-on workers

## Security Recommendations

1. **Change Admin Password** immediately after first login
2. **Update SECRET_KEY** in WSGI file with a secure random key
3. **Don't commit** `.env` or sensitive files to git
4. **Review** user permissions and access controls

## Support

For issues:
- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Contact: alfattasnimhasan@gmail.com

## Quick Reference

**Your App URL:** `https://YOUR_USERNAME.pythonanywhere.com`

**Bash Console:**
```bash
cd ~/NutriAI
workon nutriai-env
python app_new.py  # Test locally
```

**View Logs:**
- Go to Web tab
- Click on error log link
- Click on server log link

---

Created by Alfat Tasnim Hasan | Contact: 01736276082 | alfattasnimhasan@gmail.com
