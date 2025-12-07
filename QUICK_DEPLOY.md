# 🚀 NutriAI - Quick Deploy to Render

## Prerequisites ✓
- GitHub repository with NutriAI code
- Render account (free tier works!)

## 3-Step Deployment

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy NutriAI to Render"
git push origin main
```

### Step 2: Create Service on Render
1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect your **NutriAI** repository
4. Click **"Apply"**

### Step 3: Done! 🎉
Your app will be live at: `https://[your-service-name].onrender.com`

## Default Login
- Username: `admin`
- Password: `admin123`
⚠️ Change immediately after login!

## What's Included?
✅ 300+ food database
✅ Admin panel
✅ ML-powered recommendations
✅ Meal planner
✅ AI chatbot
✅ User management
✅ Food logging & tracking

## Files Ready for Deployment
✅ render.yaml - Auto-configuration
✅ build.sh - Database setup
✅ gunicorn_config.py - Server config
✅ requirements.txt - Dependencies
✅ Procfile - Process definition
✅ runtime.txt - Python 3.11.9

## Need Help?
📖 See `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions
📖 See `DEPLOYMENT_SUMMARY.md` for what was fixed

## Troubleshooting
- **Build fails?** Check logs in Render dashboard
- **App won't start?** Verify all files committed to git
- **Database empty?** Check if build.sh ran successfully

---
**Ready? Start with Step 1 above! 🚀**
