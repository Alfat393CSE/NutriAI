# 🍏 NutriAI - Intelligent Nutrition Management System

**Status**: ✅ **FULLY OPERATIONAL** | **Version**: 2.0.0 | **Last Updated**: December 6, 2025

An AI-powered nutrition and diet management platform with machine learning models, personalized meal planning, intelligent chatbot, food comparison tools, and comprehensive admin panel.

## ✅ System Status

**All Features Tested and Working**
- ✅ Database initialized with user authentication
- ✅ ML models loaded (Food Similarity, Diet Classifier, Meal Planner, Chatbot)
- ✅ 8+ user templates and features
- ✅ 40+ REST API endpoints
- ✅ Admin panel with access control
- ✅ Professional responsive UI/UX

## 🌟 Features

### 1. ML Models
- **Food Similarity Engine**: TF-IDF based similarity search for finding alternative foods
- **Diet Goal Classifier**: Predicts optimal diet based on comprehensive user profile
- **Meal Plan Generator**: Creates personalized 7-day meal plans with macro calculations
- **Chatbot Engine**: NLP-powered assistant for nutrition questions and recommendations
- **CNN Food Classifier**: Placeholder for future food image recognition

### 2. Backend (Flask)
- User registration and authentication with Flask-Login
- Comprehensive user profiles with health metrics and dietary preferences
- SQLite database with SQLAlchemy ORM (8 models)
- 40+ REST APIs for all features
- Session-based authentication
- Admin panel with role-based access control
- ML prediction tracking and logging

### 3. Frontend Features
- **Landing Page**: Modern hero section with feature showcase
- **Dashboard**: Calorie tracking, macro visualization, food logs, meal plan overview
- **Food Search**: Browse 25+ foods with nutritional information and filtering
- **Food Comparison**: Side-by-side comparison of two foods with health analysis
- **Meal Planner**: Daily meal sections (Breakfast/Lunch/Dinner/Snack) with 7-day plan generation
- **Chatbot**: Interactive AI assistant with natural language understanding
- **Profile Management**: Complete health data and dietary preference management
- **Admin Dashboard**: System monitoring, user management, analytics

### 4. User Capabilities 🎯
- **Food Database**: Search and browse 25+ foods with complete nutritional data
- **Food Alternatives**: ML-powered similar food recommendations
- **Food Comparison**: Compare two foods side-by-side with health verdict
- **Meal Planning**: Generate personalized 7-day meal plans
- **Daily Meal Tracking**: Log foods for Breakfast, Lunch, Dinner, and Snacks
- **AI Chatbot**: Ask nutrition questions, get food recommendations, dietary advice
- **Profile Management**: Update health metrics, dietary restrictions, and goals
- **Calorie & Macro Tracking**: Real-time dashboard with visual charts

### 5. Admin Panel 🛡️
- **Dashboard**: System stats, user metrics, ML performance tracking
- **User Management**: View/activate/deactivate users, grant admin privileges
- **Food Database**: Add/edit/delete foods, manage nutritional data
- **ML Monitor**: Track predictions, model accuracy, usage patterns
- **Analytics**: Diet goal trends, user growth, popular foods
- **Settings**: Configure system parameters, API limits, feature flags
- **Activity Logs**: Complete audit trail of all admin actions

## 🚀 Quick Start

### Installation
```powershell
# Install dependencies
pip install flask flask-login flask-cors flask-sqlalchemy scikit-learn pandas numpy
```

### First Run
```powershell
# Navigate to project directory
cd "C:\Users\Alfat\OneDrive\Documents\Desktop\NutriAI"

# Start the server
python app_new.py
```

Visit: **http://127.0.0.1:5000**

### For First Time Users:
```
1. Register → Create your account with email and password
2. Login → Access the dashboard
3. Complete Profile → Add age, weight, height, dietary goals
4. Explore Dashboard → View your nutrition overview
5. Food Search → Browse and discover foods
6. Compare Foods → Analyze nutritional differences
7. Meal Planner → Generate personalized 7-day meal plans
8. AI Chatbot → Ask nutrition questions and get recommendations
```

### For Admins:
```
1. Login at /login → Use admin credentials (username: admin, password: admin123)
2. Access Admin Panel → Click "Admin Panel" in sidebar or visit /admin
3. Dashboard → Monitor system health and user statistics
4. User Management → Manage users and grant permissions
5. Food Database → Add/edit/delete foods
6. ML Monitor → Track model performance and predictions
7. Analytics → View trends and insights
8. Settings → Configure system parameters
```

**Admin Credentials:**
- **URL**: http://127.0.0.1:5000/login
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Admin users login at the regular `/login` page, NOT at `/admin`. After logging in with admin credentials, you'll see the "Admin Panel" link in the sidebar.

## 📊 Key APIs

### User APIs
- `POST /register`, `/login` - Authentication
- `GET /api/foods` - Get all foods with filters
- `GET /api/foods/<id>` - Get single food details
- `GET /api/foods/alternatives/<id>` - Find similar foods (ML-powered)
- `GET /api/foods/compare/<id1>/<id2>` - Compare two foods
- `POST /api/foods/compare` - Compare multiple foods
- `GET /api/food-logs` - Get user's food logs
- `POST /api/food-logs` - Log food intake
- `GET /api/meal-plans` - Get user's meal plans
- `POST /api/meal-plans` - Generate new meal plan
- `POST /api/chatbot/message` - Chat with AI assistant
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Admin APIs (12 endpoints)
- `GET /api/admin/stats` - Dashboard statistics
- `GET /api/admin/users` - List all users
- `POST /api/admin/users/<id>/toggle-active` - Activate/deactivate user
- `POST /api/admin/users/<id>/make-admin` - Grant admin privileges
- `GET /api/admin/foods` - Manage food database
- `PUT /api/admin/foods/<id>` - Update food
- `DELETE /api/admin/foods/<id>` - Delete food
- `GET /api/admin/ml/predictions` - ML prediction history
- `GET /api/admin/ml/accuracy` - Model accuracy metrics
- `GET /api/admin/analytics/diet-goals` - Diet goal distribution
- `GET /api/admin/analytics/user-growth` - User growth trends
- `GET /api/admin/logs` - Admin activity logs

## 🍎 Food Database

25+ foods with complete nutritional data:
- **Proteins**: Chicken Breast, Salmon, Greek Yogurt, Eggs, Tofu
- **Grains**: Brown Rice, Quinoa, Oatmeal, Whole Wheat Bread
- **Vegetables**: Broccoli, Spinach, Sweet Potato, Carrots, Kale
- **Fruits**: Apple, Banana, Blueberries, Orange, Avocado
- **Nuts**: Almonds, Walnuts, Peanuts
- **Legumes**: Lentils, Black Beans, Chickpeas

Each food includes:
- Calories, Protein, Carbs, Fat, Fiber, Sugar
- Vitamins and minerals
- Health score (0-100)
- Category and tags
- Allergen information

## 🔐 Security

- **Password Hashing**: Werkzeug security for password encryption
- **Flask-Login**: Session-based authentication
- **Admin Access Control**: Two-tier decorator system
  - `@admin_required` - Redirects non-admin users (for pages)
  - `@admin_api_required` - Returns 403 JSON (for APIs)
- **SQLAlchemy ORM**: SQL injection prevention
- **CORS Support**: Secure cross-origin requests
- **Active Status**: User deactivation capability
- **Admin Logging**: Complete audit trail

## 📁 Project Structure

```
NutriAI/
├── app_new.py                  # Main Flask application (1195 lines)
├── models.py                   # Database models (8 models, 262 lines)
├── ml_utils.py                 # ML engines (5 classes, 494 lines)
├── templates/                  # HTML templates
│   ├── home.html               # Landing page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # User dashboard
│   ├── food_search.html        # Food browser
│   ├── food_comparison.html    # Food comparison tool
│   ├── meal_planner.html       # Meal planning interface
│   ├── chatbot.html            # AI chatbot
│   ├── profile.html            # Profile management
│   ├── admin_dashboard.html    # Admin panel
│   └── includes/
│       └── sidebar.html        # Reusable sidebar component
├── static/                     # Static assets
│   ├── css/
│   │   └── main.css            # Styles (2000+ lines, Flowmo-inspired)
│   └── js/
│       ├── main.js             # Core utilities
│       ├── auth.js             # Authentication logic
│       ├── dashboard.js        # Dashboard interactions
│       ├── food-search.js      # Food search functionality
│       ├── food-comparison.js  # Comparison logic
│       ├── meal-planner.js     # Meal planning logic
│       ├── chatbot.js          # Chatbot interactions
│       ├── profile.js          # Profile management
│       └── admin.js            # Admin panel logic
└── instance/                   # Database files
    └── nutriai.db              # SQLite database
```

## 🔧 Technical Stack

- **Backend**: Flask 3.0.0, Flask-Login, Flask-CORS, Flask-SQLAlchemy
- **Database**: SQLite with 8 models (User, Food, FoodLog, MealPlan, ChatSession, AdminLog, MLPrediction, SystemSettings)
- **ML/AI**: scikit-learn (TF-IDF, cosine similarity), pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript ES6+, Chart.js 4.0
- **Icons**: Font Awesome 6.4.0
- **Design**: Flowmo-inspired gradients, animations, responsive layouts

## 📚 Key Routes

### User Routes
- `/` - Landing page
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/dashboard` - User dashboard
- `/profile` - Profile management
- `/food-search` - Food database browser
- `/food-comparison` - Compare foods side-by-side
- `/meal-planner` - Meal planning interface
- `/chatbot` - AI nutrition assistant

### Admin Routes
- `/admin` - Admin dashboard (protected)
- All API routes under `/api/admin/*` (protected)

## 🎨 UI/UX Features

- **Flowmo-Inspired Design**: Modern gradients, smooth animations
- **CSS Variables**: Easy theming with color system
- **Responsive Layout**: Mobile-first design, works on all devices
- **Interactive Charts**: Chart.js visualizations for data
- **Toast Notifications**: User feedback for all actions
- **Loading States**: Skeleton loaders and spinners
- **Form Validation**: Client-side and server-side validation
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation

## 🚨 Error Handling

- **API Errors**: Proper HTTP status codes (200, 400, 401, 403, 404, 500)
- **Try-Catch Blocks**: Comprehensive error catching
- **Traceback Logging**: Server-side error logging for debugging
- **User Feedback**: Toast messages for success/error states
- **Graceful Degradation**: Fallback options when ML models unavailable

## 📈 Future Enhancements

- [ ] CNN-based food image recognition
- [ ] Mobile app (React Native)
- [ ] Barcode scanner integration
- [ ] Social features (share meal plans)
- [ ] Recipe recommendations
- [ ] Grocery list generator
- [ ] Integration with fitness trackers
- [ ] Multi-language support
- [ ] Dark mode theme

---

**Built with ❤️ for better health and nutrition**

**Version**: 2.0.0 | **License**: MIT | **Last Updated**: December 6, 2025
