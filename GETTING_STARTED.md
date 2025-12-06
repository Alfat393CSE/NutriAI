# NutriAI - Getting Started Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app_new.py
```

The app will:
- Initialize the SQLite database
- Seed 25+ sample foods automatically
- Start the Flask server on `http://localhost:5000`

### 3. Access the Application
Open your browser and go to: **http://localhost:5000**

---

## 📝 First Time Setup

### Register an Account
1. Click **"Get Started"** on the home page
2. Fill in the registration form
3. After registration, you'll be redirected to the dashboard

### Create an Admin User (Optional)
1. Register a normal account first
2. Open the database or use the Python shell:
```python
from app_new import app, db, User
with app.app_context():
    user = User.query.filter_by(username='your_username').first()
    user.is_admin = True
    db.session.commit()
```

---

## 🎯 Features Available

### For All Users:
- **Dashboard**: View daily nutrition stats with interactive charts
- **Food Search**: Browse 25+ foods, view nutrition details, find alternatives
- **Meal Planner**: Generate AI-powered weekly meal plans
- **AI Chatbot**: Ask nutrition questions (20+ intent categories)
- **Profile**: Update health metrics, dietary preferences, goals

### For Admin Users:
- **User Management**: View all users, toggle status, grant admin rights
- **Food Database**: Manage food items, view nutrition data
- **Analytics**: View diet goal distribution charts
- **Activity Logs**: Track all admin actions

---

## 🧪 Testing the Features

### 1. Log Your First Meal
- Go to Dashboard → Click **"Log Food"**
- Search for "Grilled Chicken Breast"
- Enter portion (e.g., 150g)
- See your stats update in real-time!

### 2. Generate a Meal Plan
- Navigate to **Meal Planner**
- Click **"Generate New Plan"**
- Select diet type (Weight Loss, Muscle Gain, etc.)
- Enter your budget
- View your 7-day meal plan!

### 3. Chat with AI
- Go to **AI Assistant**
- Try questions like:
  - "What foods are high in protein?"
  - "Give me a breakfast recipe"
  - "How can I lose weight?"

### 4. Find Food Alternatives
- Go to **Food Search**
- Click on any food (e.g., "White Rice")
- Click **"Find Alternatives"**
- See healthier alternatives with similar taste!

---

## 🗂️ Project Structure

```
NutriAI/
├── app_new.py              # Main Flask application (26+ API endpoints)
├── models.py               # Database models (8 tables)
├── ml_utils.py            # ML engines (similarity, classifier, chatbot)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── home.html          # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── food_search.html   # Food database browser
│   ├── meal_planner.html  # Meal planning interface
│   ├── chatbot.html       # AI chat interface
│   ├── profile.html       # User profile editor
│   ├── admin_dashboard.html # Admin panel
│   └── includes/
│       └── sidebar.html   # Reusable navigation
└── static/
    ├── css/
    │   └── main.css       # Professional styling (900+ lines)
    └── js/
        ├── main.js        # Core utilities
        ├── auth.js        # Authentication logic
        ├── dashboard.js   # Dashboard interactivity
        ├── food-search.js # Food browsing
        ├── chatbot.js     # Chat functionality
        ├── meal-planner.js # Meal plan management
        ├── profile.js     # Profile editing
        └── admin.js       # Admin panel logic
```

---

## 🔧 Configuration

### Database
- **Type**: SQLite (file-based)
- **Location**: `nutriai.db` (created automatically)
- **Tables**: Users, Foods, FoodLogs, MealPlans, ChatSessions, AdminLogs, MLPredictions, SystemSettings

### Security
⚠️ **Important for Production:**
- Change `SECRET_KEY` in `app_new.py` (line 13)
- Use environment variables for sensitive data
- Enable HTTPS
- Use a production database (PostgreSQL, MySQL)

---

## 📊 Sample Data

The app automatically seeds 25+ foods on first run:
- Proteins: Chicken, Salmon, Tofu, Eggs, etc.
- Grains: Rice, Quinoa, Oats, etc.
- Vegetables: Broccoli, Spinach, etc.
- Fruits: Banana, Apple, Berries, etc.
- Dairy: Greek Yogurt, Milk, etc.

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Database errors
Delete `nutriai.db` and restart the app to recreate the database.

### Port 5000 already in use
Change the port in `app_new.py` (last line):
```python
app.run(debug=True, port=5001)
```

---

## 🎨 Design Inspiration

The frontend design is inspired by [Flowmo](https://flowmoapp.com/) featuring:
- Modern gradient backgrounds
- Smooth animations
- Professional card layouts
- Responsive design
- Clean typography

---

## 📦 Dependencies

- **Flask 3.0.0**: Web framework
- **Flask-Login**: Authentication
- **Flask-SQLAlchemy**: Database ORM
- **Flask-CORS**: API access
- **scikit-learn**: ML models
- **pandas**: Data processing
- **numpy**: Numerical operations

---

## 🚀 Next Steps

1. **Customize**: Add your own foods to the database
2. **Extend**: Implement the CNN food image classifier
3. **Deploy**: Host on Heroku, AWS, or DigitalOcean
4. **Mobile**: Build a mobile app using the REST API

---

## 📄 License

This project is for educational purposes. Feel free to modify and use as needed!

---

**Enjoy using NutriAI! 🌱**
