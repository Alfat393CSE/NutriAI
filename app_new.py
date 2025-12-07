from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from models import db, User, Food, FoodLog, MealPlan, ChatSession, AdminLog, MLPrediction, SystemSettings, UserHistory
from ml_utils import FoodSimilarityEngine, DietGoalClassifier, MealPlanGenerator, CNNFoodClassifier, ChatbotEngine
from recommendation_engine import NutritionRecommendationEngine
import json
from datetime import datetime, timedelta, date
import uuid
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nutriai.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Global ML engines (will be initialized after DB)
food_similarity_engine = None
diet_classifier = None
meal_plan_generator = None
cnn_classifier = None
chatbot_engine = None
recommendation_engine = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_required(f):
    """Decorator for admin-only routes (page routes)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def admin_api_required(f):
    """Decorator for admin-only API routes (returns JSON)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


def log_admin_action(action, details):
    """Log admin actions"""
    if current_user.is_authenticated and current_user.is_admin:
        log = AdminLog(
            admin_id=current_user.id,
            action=action,
            details=details,
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()


def track_user_activity(action_type, food_id=None, food_name=None, search_query=None, 
                       recommendation_reason=None, quantity_g=None, session_id=None):
    """Track user activity in history"""
    if not current_user.is_authenticated:
        return
    
    try:
        # Get food details if food_id is provided
        food = None
        if food_id:
            food = Food.query.get(food_id)
            if food and not food_name:
                food_name = food.name
        
        history_entry = UserHistory(
            user_id=current_user.id,
            action_type=action_type,
            food_id=food_id,
            food_name=food_name,
            search_query=search_query,
            recommendation_reason=recommendation_reason,
            quantity_g=quantity_g,
            session_id=session_id or request.cookies.get('session_id'),
            source='web'
        )
        
        # Add nutritional data if food exists
        if food:
            history_entry.calories = food.calories
            history_entry.protein_g = food.protein_g
            history_entry.carbs_g = food.carbs_g
            history_entry.fat_g = food.fat_g
            history_entry.fiber_g = food.fiber_g
            history_entry.sugar_g = food.sugar_g
            history_entry.sodium_mg = food.sodium_mg
            history_entry.health_score = food.health_score
            history_entry.health_rating = food.health_rating
        
        db.session.add(history_entry)
        db.session.commit()
    except Exception as e:
        print(f"Error tracking user activity: {str(e)}")
        db.session.rollback()


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/')
def home():
    """Landing page"""
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Set first user as admin
        if User.query.count() == 0:
            user.is_admin = True
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        
        if request.is_json:
            return jsonify({'message': 'Registration successful', 'user': user.to_dict()}), 201
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            
            if request.is_json:
                return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
            
            # Redirect admin users to admin dashboard, regular users to user dashboard
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('dashboard'))
        
        error = 'Invalid username or password'
        if request.is_json:
            return jsonify({'error': error}), 401
        flash(error, 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('home'))


# ============================================
# USER DASHBOARD & PROFILE
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main user dashboard"""
    return render_template('dashboard.html', user=current_user)


@app.route('/profile')
@login_required
def profile_page():
    """User profile page"""
    return render_template('profile.html', user=current_user)


@app.route('/history')
@login_required
def history_page():
    """User history page"""
    return render_template('history.html', user=current_user)


@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard page"""
    return render_template('admin_dashboard.html', user=current_user)


@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    """Get or update user profile"""
    try:
        if request.method == 'GET':
            return jsonify(current_user.to_dict()), 200
        
        # Update profile
        data = request.get_json()
        
        # Update fields
        fields = ['age', 'gender', 'weight_kg', 'height_cm', 'daily_caloric_intake',
                  'protein_goal', 'carbs_goal', 'fat_goal',
                  'cholesterol', 'blood_pressure', 'glucose', 'physical_activity_level',
                  'weekly_exercise_hours', 'dietary_restrictions', 'allergies',
                  'preferred_cuisine', 'diet_goal', 'disease_type', 'severity']
        
        for field in fields:
            if field in data:
                value = data[field]
                # Convert lists to comma-separated strings for text fields
                if isinstance(value, list) and field in ['dietary_restrictions', 'allergies']:
                    value = ', '.join(str(v) for v in value)
                setattr(current_user, field, value)
        
        # Calculate BMI
        current_user.calculate_bmi()
        
        db.session.commit()
        
        return jsonify({'message': 'Profile updated', 'user': current_user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/stats')
@login_required
def dashboard_stats():
    """Get dashboard statistics"""
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    # Today's food logs
    today_logs = FoodLog.query.filter(
        FoodLog.user_id == current_user.id,
        FoodLog.date == today
    ).all()
    
    today_calories = sum(log.calories_consumed or 0 for log in today_logs)
    today_protein = sum(log.protein_consumed or 0 for log in today_logs)
    today_carbs = sum(log.carbs_consumed or 0 for log in today_logs)
    today_fat = sum(log.fat_consumed or 0 for log in today_logs)
    
    # Weekly logs
    week_logs = FoodLog.query.filter(
        FoodLog.user_id == current_user.id,
        FoodLog.date >= week_ago
    ).all()
    
    # Active meal plan
    active_meal_plan = MealPlan.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).first()
    
    # Diet recommendation
    diet_rec = None
    if diet_classifier:
        profile = current_user.to_dict()
        diet_rec = diet_classifier.predict(profile)
    
    return jsonify({
        'today': {
            'calories': round(today_calories, 1),
            'protein': round(today_protein, 1),
            'carbs': round(today_carbs, 1),
            'fat': round(today_fat, 1),
            'target_calories': current_user.daily_caloric_intake or 2000,
            'target_protein': current_user.protein_goal or 150,
            'target_carbs': current_user.carbs_goal or 200,
            'target_fat': current_user.fat_goal or 65,
            'meals_logged': len(today_logs)
        },
        'weekly': {
            'total_meals': len(week_logs),
            'avg_daily_calories': round(sum(l.calories_consumed or 0 for l in week_logs) / 7, 1)
        },
        'active_meal_plan': active_meal_plan.to_dict() if active_meal_plan else None,
        'recommended_diet': diet_rec
    }), 200


# ============================================
# FOOD DATABASE & SEARCH
# ============================================

@app.route('/food-search')
@login_required
def food_search_page():
    """Food search page"""
    return render_template('food_search.html')


@app.route('/food-comparison')
@login_required
def food_comparison_page():
    """Food comparison page"""
    return render_template('food_comparison.html')


@app.route('/api/foods', methods=['GET'])
@login_required
def get_foods():
    """Get all foods with optional filters"""
    category = request.args.get('category')
    search = request.args.get('search')
    health_rating = request.args.get('health_rating')
    min_protein = request.args.get('min_protein', type=float)
    max_calories = request.args.get('max_calories', type=float)
    
    query = Food.query.filter_by(approved=True)
    
    if category:
        query = query.filter_by(category=category)
    if health_rating:
        query = query.filter_by(health_rating=health_rating)
    if search:
        query = query.filter(Food.name.ilike(f'%{search}%'))
        # Track search in history
        track_user_activity('search', search_query=search)
    if min_protein:
        query = query.filter(Food.protein_g >= min_protein)
    if max_calories:
        query = query.filter(Food.calories <= max_calories)
    
    foods = query.all()
    
    return jsonify({'foods': [food.to_dict() for food in foods]}), 200


@app.route('/api/foods/<int:food_id>')
@login_required
def get_food(food_id):
    """Get single food details"""
    food = Food.query.get_or_404(food_id)
    
    # Track view in history
    track_user_activity('view', food_id=food_id, food_name=food.name)
    
    return jsonify(food.to_dict()), 200


@app.route('/api/foods/<int:food_id>/check-risks')
@login_required
def check_food_risks(food_id):
    """Check if food has allergy or health risks for current user"""
    food = Food.query.get_or_404(food_id)
    
    risks = []
    warnings = []
    
    # Check allergies
    user_allergies = (current_user.allergies or '').lower()
    food_allergens = (food.common_allergens or '').lower()
    
    if user_allergies:
        for allergy in user_allergies.split(','):
            allergy = allergy.strip()
            if allergy and allergy in food_allergens:
                risks.append({
                    'type': 'allergy',
                    'severity': 'danger',
                    'message': f'⚠️ ALLERGEN ALERT: Contains {allergy.title()}',
                    'icon': 'exclamation-triangle'
                })
    
    # Check dietary restrictions
    restrictions = (current_user.dietary_restrictions or '').lower()
    if restrictions:
        if 'vegetarian' in restrictions and food.category and 'meat' in food.category.lower():
            warnings.append({
                'type': 'dietary',
                'severity': 'warning',
                'message': '🌱 Not suitable for vegetarian diet',
                'icon': 'leaf'
            })
        if 'vegan' in restrictions and food.category and any(x in food.category.lower() for x in ['dairy', 'meat', 'egg']):
            warnings.append({
                'type': 'dietary',
                'severity': 'warning',
                'message': '🌱 Not suitable for vegan diet',
                'icon': 'leaf'
            })
    
    # Check health conditions
    disease = (current_user.disease_type or '').lower()
    
    if 'diabetes' in disease:
        if food.sugar_g and food.sugar_g > 10:
            warnings.append({
                'type': 'health',
                'severity': 'warning',
                'message': f'⚕️ High sugar content ({food.sugar_g}g) - monitor blood glucose',
                'icon': 'heartbeat'
            })
        if food.carbs_g and food.carbs_g > 30:
            warnings.append({
                'type': 'health',
                'severity': 'info',
                'message': f'Moderate-high carbs ({food.carbs_g}g) - consider portion size',
                'icon': 'info-circle'
            })
    
    if 'hypertension' in disease or 'high blood pressure' in disease:
        if food.sodium_mg and food.sodium_mg > 400:
            warnings.append({
                'type': 'health',
                'severity': 'warning',
                'message': f'⚕️ High sodium content ({food.sodium_mg}mg) - may affect blood pressure',
                'icon': 'heartbeat'
            })
    
    if 'heart' in disease or 'cardiovascular' in disease:
        if food.cholesterol_mg and food.cholesterol_mg > 50:
            warnings.append({
                'type': 'health',
                'severity': 'warning',
                'message': f'❤️ High cholesterol ({food.cholesterol_mg}mg) - consider alternatives',
                'icon': 'heart'
            })
        if food.fat_g and food.fat_g > 15:
            warnings.append({
                'type': 'health',
                'severity': 'info',
                'message': f'High fat content ({food.fat_g}g) - consume in moderation',
                'icon': 'info-circle'
            })
    
    if 'kidney' in disease or 'renal' in disease:
        if food.sodium_mg and food.sodium_mg > 300:
            warnings.append({
                'type': 'health',
                'severity': 'warning',
                'message': f'⚕️ High sodium - may strain kidneys',
                'icon': 'heartbeat'
            })
        if food.protein_g and food.protein_g > 20:
            warnings.append({
                'type': 'health',
                'severity': 'info',
                'message': f'High protein ({food.protein_g}g) - consult healthcare provider',
                'icon': 'info-circle'
            })
    
    # Check diet goals
    if current_user.diet_goal:
        goal = current_user.diet_goal.lower()
        if 'weight_loss' in goal or 'lose weight' in goal:
            if food.calories and food.calories > 300:
                warnings.append({
                    'type': 'diet_goal',
                    'severity': 'info',
                    'message': f'High calorie food ({food.calories} cal) - adjust portions for weight loss',
                    'icon': 'chart-line'
                })
    
    return jsonify({
        'food_id': food_id,
        'food_name': food.name,
        'has_risks': len(risks) > 0,
        'has_warnings': len(warnings) > 0,
        'risks': risks,
        'warnings': warnings,
        'safe': len(risks) == 0 and len(warnings) == 0
    }), 200


@app.route('/api/foods/compare/<int:food_id1>/<int:food_id2>')
@login_required
def compare_two_foods(food_id1, food_id2):
    """Compare two foods with detailed analysis"""
    food1 = Food.query.get_or_404(food_id1)
    food2 = Food.query.get_or_404(food_id2)
    
    # Calculate differences
    differences = {
        'calories': (food2.calories or 0) - (food1.calories or 0),
        'protein_g': (food2.protein_g or 0) - (food1.protein_g or 0),
        'carbs_g': (food2.carbs_g or 0) - (food1.carbs_g or 0),
        'fat_g': (food2.fat_g or 0) - (food1.fat_g or 0),
        'fiber_g': (food2.fiber_g or 0) - (food1.fiber_g or 0),
        'sugar_g': (food2.sugar_g or 0) - (food1.sugar_g or 0),
        'sodium_mg': (food2.sodium_mg or 0) - (food1.sodium_mg or 0),
        'health_score': (food2.health_score or 0) - (food1.health_score or 0)
    }
    
    # Determine which is healthier
    health_analysis = {
        'winner': None,
        'reasons': []
    }
    
    score1 = food1.health_score or 0
    score2 = food2.health_score or 0
    
    if score2 > score1:
        health_analysis['winner'] = food2.name
        health_analysis['reasons'].append(f"Higher health score ({score2} vs {score1})")
    elif score1 > score2:
        health_analysis['winner'] = food1.name
        health_analysis['reasons'].append(f"Higher health score ({score1} vs {score2})")
    else:
        health_analysis['winner'] = 'tie'
    
    # Add specific nutritional advantages
    if differences['protein_g'] > 5:
        health_analysis['reasons'].append(f"{food2.name} has {abs(differences['protein_g']):.1f}g more protein")
    elif differences['protein_g'] < -5:
        health_analysis['reasons'].append(f"{food1.name} has {abs(differences['protein_g']):.1f}g more protein")
    
    if differences['fiber_g'] > 2:
        health_analysis['reasons'].append(f"{food2.name} has {abs(differences['fiber_g']):.1f}g more fiber")
    elif differences['fiber_g'] < -2:
        health_analysis['reasons'].append(f"{food1.name} has {abs(differences['fiber_g']):.1f}g more fiber")
    
    if differences['calories'] < -50:
        health_analysis['reasons'].append(f"{food1.name} has {abs(differences['calories']):.0f} fewer calories")
    elif differences['calories'] > 50:
        health_analysis['reasons'].append(f"{food2.name} has {abs(differences['calories']):.0f} more calories")
    
    if differences['sugar_g'] < -5:
        health_analysis['reasons'].append(f"{food1.name} has {abs(differences['sugar_g']):.1f}g less sugar")
    elif differences['sugar_g'] > 5:
        health_analysis['reasons'].append(f"{food2.name} has {abs(differences['sugar_g']):.1f}g more sugar")
    
    return jsonify({
        'food1': food1.to_dict(),
        'food2': food2.to_dict(),
        'differences': differences,
        'health_analysis': health_analysis
    }), 200


@app.route('/api/foods/compare', methods=['POST'])
@login_required
def compare_foods():
    """Compare multiple foods side-by-side"""
    data = request.get_json()
    food_ids = data.get('food_ids', [])
    
    foods = Food.query.filter(Food.id.in_(food_ids)).all()
    
    return jsonify({
        'foods': [food.to_dict() for food in foods],
        'comparison': {
            'highest_protein': max(foods, key=lambda f: f.protein_g or 0).name if foods else None,
            'lowest_calories': min(foods, key=lambda f: f.calories or 1000).name if foods else None,
            'best_health_score': max(foods, key=lambda f: f.health_score or 0).name if foods else None
        }
    }), 200


@app.route('/api/foods/alternatives/<int:food_id>')
@login_required
def get_food_alternatives(food_id):
    """Get similar/healthier food alternatives"""
    try:
        food = Food.query.get_or_404(food_id)
        
        if food_similarity_engine:
            similar = food_similarity_engine.find_similar(food.name, n=5)
            
            # Track recommendations in history
            for alt in similar:
                if alt.get('id'):
                    track_user_activity(
                        'recommend', 
                        food_id=alt['id'], 
                        food_name=alt.get('name'),
                        recommendation_reason=f"Alternative to {food.name}"
                    )
            
            return jsonify(similar), 200
        
        # Fallback: find by category
        alternatives = Food.query.filter(
            Food.category == food.category,
            Food.id != food_id,
            Food.health_score > food.health_score
        ).limit(5).all()
        
        # Track recommendations
        for alt in alternatives:
            track_user_activity(
                'recommend',
                food_id=alt.id,
                food_name=alt.name,
                recommendation_reason=f"Healthier alternative to {food.name}"
            )
        
        return jsonify([alt.to_dict() for alt in alternatives]), 200
    
    except Exception as e:
        print(f"Error in get_food_alternatives: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# ============================================
# FOOD LOGGING
# ============================================

@app.route('/api/food-logs', methods=['GET', 'POST'])
@login_required
def food_logs():
    """Get or create food logs"""
    if request.method == 'GET':
        log_date = request.args.get('date')
        
        query = FoodLog.query.filter_by(user_id=current_user.id)
        
        if log_date:
            try:
                log_date = datetime.strptime(log_date, '%Y-%m-%d').date()
                query = query.filter_by(date=log_date)
            except:
                pass
        else:
            # Default to today
            query = query.filter_by(date=date.today())
        
        logs = query.all()
        return jsonify([log.to_dict() for log in logs]), 200
    
    # Create new log
    data = request.get_json()
    
    food = Food.query.get_or_404(data['food_id'])
    quantity = data.get('quantity_g', 100)
    
    # Calculate nutrition based on quantity
    multiplier = quantity / 100
    
    log = FoodLog(
        user_id=current_user.id,
        food_id=food.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date() if 'date' in data else date.today(),
        meal_type=data.get('meal_type', 'Snack'),
        quantity_g=quantity,
        calories_consumed=food.calories * multiplier,
        protein_consumed=food.protein_g * multiplier,
        carbs_consumed=food.carbs_g * multiplier,
        fat_consumed=food.fat_g * multiplier
    )
    
    db.session.add(log)
    db.session.commit()
    
    # Track in history
    track_user_activity(
        'log',
        food_id=food.id,
        food_name=food.name,
        quantity_g=quantity
    )
    
    return jsonify(log.to_dict()), 201


@app.route('/api/food-logs/<int:log_id>', methods=['DELETE'])
@login_required
def delete_food_log(log_id):
    """Delete a food log"""
    log = FoodLog.query.get_or_404(log_id)
    
    if log.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(log)
    db.session.commit()
    
    return jsonify({'message': 'Log deleted'}), 200


# ============================================
# MEAL PLANNING
# ============================================

@app.route('/meal-planner')
@login_required
def meal_planner_page():
    """Meal planner page"""
    return render_template('meal_planner.html')


@app.route('/api/meal-plans', methods=['GET', 'POST'])
@login_required
def meal_plans():
    """Get or generate meal plans"""
    try:
        if request.method == 'GET':
            plans = MealPlan.query.filter_by(user_id=current_user.id).order_by(MealPlan.created_at.desc()).all()
            return jsonify([plan.to_dict() for plan in plans]), 200
        
        # Generate new meal plan
        data = request.get_json()
        
        user_profile = current_user.to_dict()
        user_profile['budget_per_day'] = data.get('budget_per_day', 20)
        
        diet_type = data.get('diet_type', 'Balanced')
        
        # Get all foods for meal planning
        foods = Food.query.filter_by(approved=True).all()
        foods_dict = [food.to_dict() for food in foods]
        
        if not foods_dict:
            return jsonify({'error': 'No foods available for meal planning'}), 400
        
        if meal_plan_generator:
            meal_plan_generator.foods = foods_dict
            plan_data = meal_plan_generator.generate_plan(user_profile, diet_type)
        else:
            return jsonify({'error': 'Meal plan generator not initialized'}), 500
        
        # Create meal plan
        week_start = datetime.strptime(data.get('start_date', date.today().isoformat()), '%Y-%m-%d').date()
        
        plan = MealPlan(
            user_id=current_user.id,
            name=data.get('name', f"Meal Plan {week_start}"),
            week_start_date=week_start,
            monday=json.dumps(plan_data['meal_plan'].get('monday', {})),
            tuesday=json.dumps(plan_data['meal_plan'].get('tuesday', {})),
            wednesday=json.dumps(plan_data['meal_plan'].get('wednesday', {})),
            thursday=json.dumps(plan_data['meal_plan'].get('thursday', {})),
            friday=json.dumps(plan_data['meal_plan'].get('friday', {})),
            saturday=json.dumps(plan_data['meal_plan'].get('saturday', {})),
            sunday=json.dumps(plan_data['meal_plan'].get('sunday', {})),
            total_calories=plan_data['totals']['total_calories'],
            total_protein=plan_data['totals']['total_protein'],
            total_carbs=plan_data['totals']['total_carbs'],
            total_fat=plan_data['totals']['total_fat'],
            estimated_budget=data.get('budget_per_day', 20) * 7
        )
        
        db.session.add(plan)
        db.session.commit()
        
        return jsonify({'message': 'Meal plan created', 'plan_id': plan.id}), 201
    
    except Exception as e:
        print(f"Error in meal_plans endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/meal-plans/<int:plan_id>')
@login_required
def get_meal_plan(plan_id):
    """Get detailed meal plan"""
    plan = MealPlan.query.get_or_404(plan_id)
    
    if plan.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    plan_dict = plan.to_dict()
    plan_dict['meals'] = {
        'Monday': json.loads(plan.monday) if plan.monday else {},
        'Tuesday': json.loads(plan.tuesday) if plan.tuesday else {},
        'Wednesday': json.loads(plan.wednesday) if plan.wednesday else {},
        'Thursday': json.loads(plan.thursday) if plan.thursday else {},
        'Friday': json.loads(plan.friday) if plan.friday else {},
        'Saturday': json.loads(plan.saturday) if plan.saturday else {},
        'Sunday': json.loads(plan.sunday) if plan.sunday else {}
    }
    
    return jsonify(plan_dict), 200


@app.route('/api/meal-plans/<int:plan_id>/activate', methods=['POST'])
@login_required
def activate_meal_plan(plan_id):
    """Set meal plan as active"""
    plan = MealPlan.query.get_or_404(plan_id)
    
    if plan.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Deactivate all other plans
    MealPlan.query.filter_by(user_id=current_user.id).update({'is_active': False})
    
    plan.is_active = True
    db.session.commit()
    
    return jsonify({'message': 'Meal plan activated'}), 200


# ============================================
# CHATBOT
# ============================================

@app.route('/chatbot')
@login_required
def chatbot_page():
    """Chatbot interface page"""
    return render_template('chatbot.html')


@app.route('/api/chatbot/message', methods=['POST'])
@login_required
def chatbot_message():
    """Process chatbot message"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        # Get or create session
        chat_session = None
        if session_id:
            chat_session = ChatSession.query.filter_by(session_id=session_id, user_id=current_user.id).first()
        
        if not chat_session:
            session_id = str(uuid.uuid4())
            chat_session = ChatSession(
                user_id=current_user.id,
                session_id=session_id,
                messages=json.dumps([])
            )
            db.session.add(chat_session)
        
        # Get message history
        messages = json.loads(chat_session.messages) if chat_session and chat_session.messages else []
        
        # Process message
        user_profile = current_user.to_dict()
        
        if chatbot_engine:
            response = chatbot_engine.process_message(message, user_profile)
        else:
            response = {'response': "Chatbot engine not initialized. Please contact support."}
        
        # Add to history
        messages.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.utcnow().isoformat()
        })
        messages.append({
            'role': 'assistant',
            'content': response['response'],
            'timestamp': datetime.utcnow().isoformat()
        })
        
        chat_session.messages = json.dumps(messages)
        chat_session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'session_id': session_id,
            'response': response['response'],
            'data': response
        }), 200
    
    except Exception as e:
        print(f"Error in chatbot_message endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/chatbot/sessions')
@login_required
def get_chat_sessions():
    """Get user's chat sessions"""
    sessions = ChatSession.query.filter_by(user_id=current_user.id).order_by(ChatSession.updated_at.desc()).all()
    
    return jsonify([{
        'session_id': s.session_id,
        'updated_at': s.updated_at.isoformat(),
        'message_count': len(json.loads(s.messages)) if s.messages else 0
    } for s in sessions]), 200


# ============================================
# ADVANCED FEATURES
# ============================================

@app.route('/api/features/mood-food', methods=['POST'])
@login_required
def mood_food():
    """Get food recommendations based on mood"""
    data = request.get_json()
    mood = data.get('mood', 'happy').lower()
    
    mood_mapping = {
        'stressed': {'category': 'Fruits', 'keywords': ['banana', 'avocado', 'dark chocolate']},
        'tired': {'category': 'Proteins', 'keywords': ['chicken', 'fish', 'eggs', 'nuts']},
        'happy': {'category': 'Vegetables', 'keywords': ['berries', 'salad', 'yogurt']},
        'sad': {'category': 'Proteins', 'keywords': ['salmon', 'turkey', 'walnuts']}
    }
    
    mapping = mood_mapping.get(mood, mood_mapping['happy'])
    
    foods = Food.query.filter(
        (Food.category == mapping['category']) |
        (Food.name.ilike(f"%{mapping['keywords'][0]}%"))
    ).limit(5).all()
    
    return jsonify({
        'mood': mood,
        'recommendations': [food.to_dict() for food in foods]
    }), 200


@app.route('/api/features/weekly-report')
@login_required
def weekly_report():
    """Generate weekly nutrition report"""
    week_ago = date.today() - timedelta(days=7)
    
    logs = FoodLog.query.filter(
        FoodLog.user_id == current_user.id,
        FoodLog.date >= week_ago
    ).all()
    
    total_calories = sum(log.calories_consumed or 0 for log in logs)
    total_protein = sum(log.protein_consumed or 0 for log in logs)
    total_carbs = sum(log.carbs_consumed or 0 for log in logs)
    total_fat = sum(log.fat_consumed or 0 for log in logs)
    
    target_calories = (current_user.daily_caloric_intake or 2000) * 7
    
    # Calculate grade
    calorie_adherence = min(100, (total_calories / target_calories) * 100) if target_calories > 0 else 0
    
    if calorie_adherence >= 90:
        grade = 'A'
    elif calorie_adherence >= 75:
        grade = 'B'
    elif calorie_adherence >= 60:
        grade = 'C'
    else:
        grade = 'D'
    
    return jsonify({
        'week_start': week_ago.isoformat(),
        'week_end': date.today().isoformat(),
        'totals': {
            'calories': round(total_calories, 1),
            'protein': round(total_protein, 1),
            'carbs': round(total_carbs, 1),
            'fat': round(total_fat, 1)
        },
        'averages': {
            'daily_calories': round(total_calories / 7, 1),
            'daily_protein': round(total_protein / 7, 1)
        },
        'grade': grade,
        'adherence_percentage': round(calorie_adherence, 1),
        'meals_logged': len(logs),
        'insights': [
            f"You logged {len(logs)} meals this week.",
            f"Your average daily intake was {round(total_calories/7, 0)} calories.",
            f"Keep it up!" if grade in ['A', 'B'] else "Try to stay consistent with your meal logging."
        ]
    }), 200


@app.route('/api/features/future-prediction')
@login_required
def future_prediction():
    """Predict future weight and energy trends"""
    current_weight = current_user.weight_kg or 70
    target_calories = current_user.daily_caloric_intake or 2000
    
    # Simple prediction model
    weeks = 8
    predictions = []
    
    for week in range(weeks):
        # Assume 0.5kg loss per week with calorie deficit
        predicted_weight = current_weight - (week * 0.3)
        energy_level = min(100, 70 + (week * 3))  # Energy improves over time
        
        predictions.append({
            'week': week + 1,
            'predicted_weight': round(predicted_weight, 1),
            'energy_level': round(energy_level, 0)
        })
    
    return jsonify({
        'current_weight': current_weight,
        'predictions': predictions,
        'message': 'Predictions based on consistent adherence to your diet plan.'
    }), 200


@app.route('/api/features/allergy-check', methods=['POST'])
@login_required
def allergy_check():
    """Check if food contains user's allergens"""
    data = request.get_json()
    food_id = data.get('food_id')
    
    food = Food.query.get_or_404(food_id)
    user_allergies = current_user.allergies.lower().split(',') if current_user.allergies else []
    
    food_allergens = food.common_allergens.lower().split(',') if food.common_allergens else []
    
    detected_allergens = [a.strip() for a in user_allergies if any(a.strip() in fa for fa in food_allergens)]
    
    return jsonify({
        'food': food.name,
        'safe': len(detected_allergens) == 0,
        'detected_allergens': detected_allergens,
        'warning': f"⚠️ Contains: {', '.join(detected_allergens)}" if detected_allergens else "✓ Safe to eat"
    }), 200


# ============================================
# ADMIN PANEL - User Management
# ============================================

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin dashboard"""
    return render_template('admin_dashboard.html')


@app.route('/api/admin/stats')
@admin_api_required
def admin_stats():
    """Get admin dashboard statistics"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_foods = Food.query.count()
    total_meal_plans = MealPlan.query.count()
    total_logs = FoodLog.query.count()
    
    # Recent registrations
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = User.query.filter(User.created_at >= week_ago).count()
    
    # Popular foods
    popular_foods = db.session.query(
        Food.name, db.func.count(FoodLog.id).label('count')
    ).join(FoodLog).group_by(Food.name).order_by(db.text('count DESC')).limit(5).all()
    
    return jsonify({
        'users': {
            'total': total_users,
            'active': active_users,
            'new_this_week': new_users_week
        },
        'content': {
            'total_foods': total_foods,
            'total_meal_plans': total_meal_plans,
            'total_food_logs': total_logs
        },
        'popular_foods': [{'name': f[0], 'count': f[1]} for f in popular_foods]
    }), 200


@app.route('/api/admin/users')
@admin_api_required
def admin_get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'is_admin': u.is_admin,
        'is_active': u.is_active,
        'created_at': u.created_at.isoformat() if u.created_at else None
    } for u in users]), 200


@app.route('/api/admin/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_api_required
def admin_toggle_user(user_id):
    """Activate/deactivate user"""
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    log_admin_action('toggle_user_status', f"User {user.username} {'activated' if user.is_active else 'deactivated'}")
    
    return jsonify({'message': 'User status updated', 'is_active': user.is_active}), 200


@app.route('/api/admin/users/<int:user_id>/make-admin', methods=['POST'])
@admin_api_required
def admin_make_admin(user_id):
    """Grant admin privileges"""
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    
    log_admin_action('grant_admin', f"Admin privileges granted to {user.username}")
    
    return jsonify({'message': 'Admin privileges granted'}), 200


# ============================================
# ADMIN PANEL - Food Management
# ============================================

@app.route('/api/admin/foods', methods=['GET', 'POST'])
@admin_api_required
def admin_foods():
    """Manage foods"""
    if request.method == 'GET':
        foods = Food.query.all()
        return jsonify([food.to_dict() for food in foods]), 200
    
    # Add new food
    data = request.get_json()
    
    food = Food(
        name=data['name'],
        category=data.get('category'),
        calories=data.get('calories'),
        protein_g=data.get('protein_g'),
        carbs_g=data.get('carbs_g'),
        fat_g=data.get('fat_g'),
        fiber_g=data.get('fiber_g'),
        sugar_g=data.get('sugar_g'),
        sodium_mg=data.get('sodium_mg'),
        cholesterol_mg=data.get('cholesterol_mg'),
        health_score=data.get('health_score', 50),
        health_rating=data.get('health_rating', 'Good'),
        common_allergens=data.get('common_allergens'),
        price_per_serving=data.get('price_per_serving'),
        approved=True
    )
    
    db.session.add(food)
    db.session.commit()
    
    log_admin_action('add_food', f"Added food: {food.name}")
    
    return jsonify({'message': 'Food added', 'food': food.to_dict()}), 201


@app.route('/api/admin/foods/<int:food_id>', methods=['PUT', 'DELETE'])
@admin_api_required
def admin_manage_food(food_id):
    """Update or delete food"""
    food = Food.query.get_or_404(food_id)
    
    if request.method == 'DELETE':
        db.session.delete(food)
        db.session.commit()
        
        log_admin_action('delete_food', f"Deleted food: {food.name}")
        
        return jsonify({'message': 'Food deleted'}), 200
    
    # Update food
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(food, key):
            setattr(food, key, value)
    
    db.session.commit()
    
    log_admin_action('update_food', f"Updated food: {food.name}")
    
    return jsonify({'message': 'Food updated', 'food': food.to_dict()}), 200


# ============================================
# ADMIN PANEL - ML Monitoring
# ============================================

@app.route('/api/admin/ml/predictions')
@admin_api_required
def admin_ml_predictions():
    """Get ML prediction history"""
    predictions = MLPrediction.query.order_by(MLPrediction.timestamp.desc()).limit(100).all()
    
    return jsonify([{
        'id': p.id,
        'model_type': p.model_type,
        'prediction': p.prediction,
        'confidence': p.confidence,
        'timestamp': p.timestamp.isoformat(),
        'is_correct': p.is_correct
    } for p in predictions]), 200


@app.route('/api/admin/ml/accuracy')
@admin_api_required
def admin_ml_accuracy():
    """Get ML model accuracy statistics"""
    predictions = MLPrediction.query.filter(MLPrediction.is_correct.isnot(None)).all()
    
    if not predictions:
        return jsonify({'message': 'No accuracy data available'}), 200
    
    correct = sum(1 for p in predictions if p.is_correct)
    accuracy = (correct / len(predictions)) * 100
    
    # Group by model
    by_model = {}
    for p in predictions:
        if p.model_type not in by_model:
            by_model[p.model_type] = {'correct': 0, 'total': 0}
        by_model[p.model_type]['total'] += 1
        if p.is_correct:
            by_model[p.model_type]['correct'] += 1
    
    model_accuracy = {
        model: (stats['correct'] / stats['total']) * 100
        for model, stats in by_model.items()
    }
    
    return jsonify({
        'overall_accuracy': round(accuracy, 2),
        'total_predictions': len(predictions),
        'by_model': model_accuracy
    }), 200


# ============================================
# ADMIN PANEL - Analytics
# ============================================

@app.route('/api/admin/analytics/diet-goals')
@admin_api_required
def admin_analytics_diet_goals():
    """Get diet goal distribution"""
    users = User.query.filter(User.diet_goal.isnot(None)).all()
    
    goals = {}
    for user in users:
        goal = user.diet_goal or 'Not Set'
        goals[goal] = goals.get(goal, 0) + 1
    
    return jsonify(goals), 200


@app.route('/api/admin/analytics/user-growth')
@admin_api_required
def admin_analytics_growth():
    """Get user growth over time"""
    users = User.query.order_by(User.created_at).all()
    
    growth = {}
    for user in users:
        if user.created_at:
            month = user.created_at.strftime('%Y-%m')
            growth[month] = growth.get(month, 0) + 1
    
    return jsonify(growth), 200


# ============================================
# ADMIN PANEL - Settings
# ============================================

@app.route('/api/admin/settings', methods=['GET', 'POST'])
@admin_api_required
def admin_settings():
    """Get or update system settings"""
    if request.method == 'GET':
        settings = SystemSettings.query.all()
        return jsonify({s.key: s.value for s in settings}), 200
    
    # Update settings
    data = request.get_json()
    
    for key, value in data.items():
        setting = SystemSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
        else:
            setting = SystemSettings(key=key, value=str(value))
            db.session.add(setting)
    
    db.session.commit()
    
    log_admin_action('update_settings', f"Updated {len(data)} settings")
    
    return jsonify({'message': 'Settings updated'}), 200


@app.route('/api/admin/logs')
@admin_api_required
def admin_logs():
    """Get admin activity logs"""
    logs = AdminLog.query.order_by(AdminLog.timestamp.desc()).limit(100).all()
    
    return jsonify([{
        'id': log.id,
        'admin': log.admin.username if log.admin else 'Unknown',
        'action': log.action,
        'details': log.details,
        'timestamp': log.timestamp.isoformat(),
        'ip_address': log.ip_address
    } for log in logs]), 200


# ============================================
# INITIALIZATION
# ============================================

def initialize_database():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if foods exist
        if Food.query.count() == 0:
            # Add sample foods
            sample_foods = [
                {'name': 'Chicken Breast', 'category': 'Proteins', 'calories': 165, 'protein_g': 31, 'carbs_g': 0, 'fat_g': 3.6, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
                {'name': 'Brown Rice', 'category': 'Grains', 'calories': 112, 'protein_g': 2.6, 'carbs_g': 24, 'fat_g': 0.9, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 0.5},
                {'name': 'Broccoli', 'category': 'Vegetables', 'calories': 34, 'protein_g': 2.8, 'carbs_g': 7, 'fat_g': 0.4, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
                {'name': 'Salmon', 'category': 'Proteins', 'calories': 208, 'protein_g': 20, 'carbs_g': 0, 'fat_g': 13, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 4.0},
                {'name': 'Sweet Potato', 'category': 'Vegetables', 'calories': 86, 'protein_g': 1.6, 'carbs_g': 20, 'fat_g': 0.1, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.8},
                {'name': 'Oatmeal', 'category': 'Grains', 'calories': 68, 'protein_g': 2.4, 'carbs_g': 12, 'fat_g': 1.4, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 0.3},
                {'name': 'Greek Yogurt', 'category': 'Dairy', 'calories': 59, 'protein_g': 10, 'carbs_g': 3.6, 'fat_g': 0.4, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 1.5},
                {'name': 'Almonds', 'category': 'Nuts', 'calories': 579, 'protein_g': 21, 'carbs_g': 22, 'fat_g': 49, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 2.0, 'common_allergens': 'Nuts'},
                {'name': 'Banana', 'category': 'Fruits', 'calories': 89, 'protein_g': 1.1, 'carbs_g': 23, 'fat_g': 0.3, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 0.4},
                {'name': 'Spinach', 'category': 'Vegetables', 'calories': 23, 'protein_g': 2.9, 'carbs_g': 3.6, 'fat_g': 0.4, 'health_score': 98, 'health_rating': 'Excellent', 'price_per_serving': 1.2},
                {'name': 'Eggs', 'category': 'Proteins', 'calories': 155, 'protein_g': 13, 'carbs_g': 1.1, 'fat_g': 11, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.3, 'common_allergens': 'Eggs'},
                {'name': 'Quinoa', 'category': 'Grains', 'calories': 120, 'protein_g': 4.4, 'carbs_g': 21, 'fat_g': 1.9, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 1.5},
                {'name': 'Avocado', 'category': 'Fruits', 'calories': 160, 'protein_g': 2, 'carbs_g': 9, 'fat_g': 15, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 2.0},
                {'name': 'Tuna', 'category': 'Proteins', 'calories': 130, 'protein_g': 28, 'carbs_g': 0, 'fat_g': 1, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
                {'name': 'Blueberries', 'category': 'Fruits', 'calories': 57, 'protein_g': 0.7, 'carbs_g': 14, 'fat_g': 0.3, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
                {'name': 'Kale', 'category': 'Vegetables', 'calories': 49, 'protein_g': 4.3, 'carbs_g': 9, 'fat_g': 0.9, 'health_score': 96, 'health_rating': 'Excellent', 'price_per_serving': 1.8},
                {'name': 'Whole Wheat Bread', 'category': 'Grains', 'calories': 247, 'protein_g': 13, 'carbs_g': 41, 'fat_g': 3.4, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 0.4, 'common_allergens': 'Gluten'},
                {'name': 'Cottage Cheese', 'category': 'Dairy', 'calories': 98, 'protein_g': 11, 'carbs_g': 3.4, 'fat_g': 4.3, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 1.2},
                {'name': 'Turkey Breast', 'category': 'Proteins', 'calories': 135, 'protein_g': 30, 'carbs_g': 0, 'fat_g': 0.7, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 3.0},
                {'name': 'Lentils', 'category': 'Legumes', 'calories': 116, 'protein_g': 9, 'carbs_g': 20, 'fat_g': 0.4, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 0.6},
                {'name': 'Carrots', 'category': 'Vegetables', 'calories': 41, 'protein_g': 0.9, 'carbs_g': 10, 'fat_g': 0.2, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.5},
                {'name': 'Apple', 'category': 'Fruits', 'calories': 52, 'protein_g': 0.3, 'carbs_g': 14, 'fat_g': 0.2, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 0.6},
                {'name': 'Walnuts', 'category': 'Nuts', 'calories': 654, 'protein_g': 15, 'carbs_g': 14, 'fat_g': 65, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 2.5, 'common_allergens': 'Nuts'},
                {'name': 'Bell Peppers', 'category': 'Vegetables', 'calories': 31, 'protein_g': 1, 'carbs_g': 6, 'fat_g': 0.3, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
                {'name': 'Tofu', 'category': 'Proteins', 'calories': 76, 'protein_g': 8, 'carbs_g': 1.9, 'fat_g': 4.8, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 1.5},
                {'name': 'Dark Chocolate', 'category': 'Snacks', 'calories': 546, 'protein_g': 5, 'carbs_g': 61, 'fat_g': 31, 'health_score': 60, 'health_rating': 'Fair', 'price_per_serving': 2.0},
                {'name': 'Green Tea', 'category': 'Beverages', 'calories': 1, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.2},
            ]
            
            for food_data in sample_foods:
                food = Food(**food_data)
                db.session.add(food)
            
            db.session.commit()
            print("✅ Sample foods added!")
        
        # Initialize ML engines
        global food_similarity_engine, diet_classifier, meal_plan_generator, cnn_classifier, chatbot_engine, recommendation_engine
        
        foods = Food.query.all()
        foods_dict = [food.to_dict() for food in foods]
        
        food_similarity_engine = FoodSimilarityEngine()
        food_similarity_engine.fit(foods_dict)
        
        diet_classifier = DietGoalClassifier()
        meal_plan_generator = MealPlanGenerator(foods_dict)
        cnn_classifier = CNNFoodClassifier()
        chatbot_engine = ChatbotEngine(foods_dict)
        recommendation_engine = NutritionRecommendationEngine()
        
        print("✅ ML engines initialized!")


# ============================================
# USER HISTORY ROUTES
# ============================================

@app.route('/api/history')
@login_required
def get_user_history():
    """Get user's activity history"""
    try:
        # Get query parameters
        days = request.args.get('days', type=int, default=30)
        action_type = request.args.get('action_type')
        limit = request.args.get('limit', type=int, default=100)
        
        # Build query
        query = UserHistory.query.filter_by(user_id=current_user.id)
        
        # Filter by date range
        if days:
            start_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(UserHistory.timestamp >= start_date)
        
        # Filter by action type
        if action_type:
            query = query.filter_by(action_type=action_type)
        
        # Order and limit
        history = query.order_by(UserHistory.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'history': [entry.to_dict() for entry in history],
            'total': query.count()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/stats')
@login_required
def get_history_stats():
    """Get user history statistics"""
    try:
        days = request.args.get('days', type=int, default=7)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all history for time period
        history = UserHistory.query.filter(
            UserHistory.user_id == current_user.id,
            UserHistory.timestamp >= start_date
        ).all()
        
        # Calculate statistics
        total_activities = len(history)
        
        # Count by action type
        action_counts = {}
        for entry in history:
            action_counts[entry.action_type] = action_counts.get(entry.action_type, 0) + 1
        
        # Get unique foods
        unique_foods = set()
        for entry in history:
            if entry.food_id:
                unique_foods.add(entry.food_id)
        
        # Calculate nutritional totals (for logged foods only)
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        logged_foods = [e for e in history if e.action_type == 'log' and e.quantity_g]
        for entry in logged_foods:
            if entry.calories:
                total_calories += entry.calories * (entry.quantity_g / 100)
            if entry.protein_g:
                total_protein += entry.protein_g * (entry.quantity_g / 100)
            if entry.carbs_g:
                total_carbs += entry.carbs_g * (entry.quantity_g / 100)
            if entry.fat_g:
                total_fat += entry.fat_g * (entry.quantity_g / 100)
        
        # Most viewed foods
        food_views = {}
        for entry in history:
            if entry.action_type == 'view' and entry.food_name:
                food_views[entry.food_name] = food_views.get(entry.food_name, 0) + 1
        
        top_viewed = sorted(food_views.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Search queries
        searches = [e.search_query for e in history if e.action_type == 'search' and e.search_query]
        
        return jsonify({
            'period_days': days,
            'total_activities': total_activities,
            'action_counts': action_counts,
            'unique_foods_explored': len(unique_foods),
            'nutritional_totals': {
                'calories': round(total_calories, 2),
                'protein_g': round(total_protein, 2),
                'carbs_g': round(total_carbs, 2),
                'fat_g': round(total_fat, 2)
            },
            'top_viewed_foods': [{'name': name, 'views': count} for name, count in top_viewed],
            'recent_searches': searches[:10],
            'logged_meals_count': len(logged_foods)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history/weekly-report')
@login_required
def get_weekly_report():
    """Get weekly activity report"""
    try:
        # Get last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        history = UserHistory.query.filter(
            UserHistory.user_id == current_user.id,
            UserHistory.timestamp >= start_date
        ).all()
        
        # Group by day
        daily_data = {}
        for i in range(7):
            day = start_date + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            daily_data[day_str] = {
                'date': day_str,
                'day_name': day.strftime('%A'),
                'calories': 0,
                'protein_g': 0,
                'carbs_g': 0,
                'fat_g': 0,
                'activities': 0,
                'foods_logged': 0
            }
        
        # Aggregate data
        for entry in history:
            day_str = entry.timestamp.strftime('%Y-%m-%d')
            if day_str in daily_data:
                daily_data[day_str]['activities'] += 1
                
                if entry.action_type == 'log' and entry.quantity_g:
                    daily_data[day_str]['foods_logged'] += 1
                    multiplier = entry.quantity_g / 100
                    
                    if entry.calories:
                        daily_data[day_str]['calories'] += entry.calories * multiplier
                    if entry.protein_g:
                        daily_data[day_str]['protein_g'] += entry.protein_g * multiplier
                    if entry.carbs_g:
                        daily_data[day_str]['carbs_g'] += entry.carbs_g * multiplier
                    if entry.fat_g:
                        daily_data[day_str]['fat_g'] += entry.fat_g * multiplier
        
        # Round values
        for day_data in daily_data.values():
            day_data['calories'] = round(day_data['calories'], 2)
            day_data['protein_g'] = round(day_data['protein_g'], 2)
            day_data['carbs_g'] = round(day_data['carbs_g'], 2)
            day_data['fat_g'] = round(day_data['fat_g'], 2)
        
        # Calculate weekly totals and averages
        weekly_totals = {
            'total_calories': sum(d['calories'] for d in daily_data.values()),
            'total_protein_g': sum(d['protein_g'] for d in daily_data.values()),
            'total_carbs_g': sum(d['carbs_g'] for d in daily_data.values()),
            'total_fat_g': sum(d['fat_g'] for d in daily_data.values()),
            'total_activities': sum(d['activities'] for d in daily_data.values()),
            'total_foods_logged': sum(d['foods_logged'] for d in daily_data.values())
        }
        
        weekly_averages = {
            'avg_calories': round(weekly_totals['total_calories'] / 7, 2),
            'avg_protein_g': round(weekly_totals['total_protein_g'] / 7, 2),
            'avg_carbs_g': round(weekly_totals['total_carbs_g'] / 7, 2),
            'avg_fat_g': round(weekly_totals['total_fat_g'] / 7, 2)
        }
        
        return jsonify({
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'daily_breakdown': list(daily_data.values()),
            'weekly_totals': weekly_totals,
            'weekly_averages': weekly_averages
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# NUTRITION RECOMMENDATION ENGINE ROUTES
# ============================================

@app.route('/nutrition-recommendations')
@login_required
def nutrition_recommendations_page():
    """Nutrition recommendations page"""
    return render_template('nutrition_recommendations.html', user=current_user)


@app.route('/api/nutrition-recommendations', methods=['GET'])
@login_required
def get_nutrition_recommendations():
    """
    Generate personalized nutrition recommendations based on user profile
    """
    try:
        print(f"\n🔍 DEBUG: Generating recommendations for user: {current_user.username}")
        
        if not recommendation_engine:
            print("❌ DEBUG: Recommendation engine not initialized")
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        # Get user profile data
        user_profile = {
            'age': current_user.age or 30,
            'gender': current_user.gender or 'male',
            'weight_kg': current_user.weight_kg or 70,
            'height_cm': current_user.height_cm or 170,
            'physical_activity_level': current_user.physical_activity_level or 'moderate',
            'diet_goal': current_user.diet_goal or 'maintenance',
            'dietary_restrictions': current_user.dietary_restrictions or '',
            'allergies': current_user.allergies or '',
            'disease_type': current_user.disease_type or ''
        }
        
        print(f"📊 DEBUG: User profile: {user_profile}")
        
        # Get all foods
        foods = Food.query.all()
        print(f"🍎 DEBUG: Found {len(foods)} foods in database")
        
        if len(foods) == 0:
            print("❌ DEBUG: No foods in database!")
            return jsonify({
                'error': 'No foods in database',
                'message': 'Please add foods to the database first using populate_foods.py'
            }), 404
        
        foods_dict = [food.to_dict() for food in foods]
        print(f"✅ DEBUG: Converted {len(foods_dict)} foods to dict")
        
        # Generate recommendations
        print(f"🤖 DEBUG: Calling recommendation_engine.generate_recommendations...")
        recommendations = recommendation_engine.generate_recommendations(user_profile, foods_dict)
        print(f"✅ DEBUG: Recommendations generated successfully!")
        
        # Track activity
        try:
            track_user_activity(
                action_type='recommendation_generated',
                recommendation_reason=f"Goal: {user_profile['diet_goal']}"
            )
        except Exception as track_err:
            print(f"⚠️ DEBUG: Failed to track activity: {track_err}")
        
        return jsonify(recommendations), 200
        
    except Exception as e:
        print(f"❌ Error in nutrition recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-nutrition-targets', methods=['POST'])
@login_required
def calculate_nutrition_targets():
    """
    Calculate nutrition targets based on custom input
    Allows users to get recommendations without updating their profile
    """
    try:
        if not recommendation_engine:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'gender', 'weight_kg', 'height_cm', 'activity_level', 'goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Build user profile from input
        user_profile = {
            'age': int(data['age']),
            'gender': data['gender'],
            'weight_kg': float(data['weight_kg']),
            'height_cm': float(data['height_cm']),
            'physical_activity_level': data['activity_level'],
            'diet_goal': data['goal'],
            'dietary_restrictions': data.get('dietary_restrictions', ''),
            'allergies': data.get('allergies', ''),
            'disease_type': data.get('disease_type', '')
        }
        
        # Get all foods
        foods = Food.query.all()
        foods_dict = [food.to_dict() for food in foods]
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(user_profile, foods_dict)
        
        return jsonify(recommendations), 200
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/rank-foods', methods=['POST'])
@login_required
def rank_foods_endpoint():
    """
    Rank all foods based on user profile/goals
    """
    try:
        if not recommendation_engine:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        data = request.get_json()
        
        # Get user profile (use current user or custom)
        if data and 'custom_profile' in data:
            user_profile = data['custom_profile']
        else:
            user_profile = {
                'age': current_user.age or 30,
                'gender': current_user.gender or 'male',
                'weight_kg': current_user.weight_kg or 70,
                'height_cm': current_user.height_cm or 170,
                'physical_activity_level': current_user.physical_activity_level or 'moderate',
                'diet_goal': current_user.diet_goal or 'maintenance',
                'dietary_restrictions': current_user.dietary_restrictions or '',
                'allergies': current_user.allergies or ''
            }
        
        # Get all foods
        foods = Food.query.all()
        foods_dict = [food.to_dict() for food in foods]
        
        # Rank foods
        ranked_foods = recommendation_engine.rank_foods(foods_dict, user_profile)
        
        return jsonify({
            'ranked_foods': ranked_foods[:20],  # Return top 20
            'total_foods': len(ranked_foods)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/foods-to-avoid', methods=['GET'])
@login_required
def get_foods_to_avoid():
    """
    Get list of foods to avoid based on user profile
    """
    try:
        if not recommendation_engine:
            return jsonify({'error': 'Recommendation engine not initialized'}), 500
        
        user_profile = {
            'diet_goal': current_user.diet_goal or 'maintenance',
            'dietary_restrictions': current_user.dietary_restrictions or '',
            'allergies': current_user.allergies or '',
            'disease_type': current_user.disease_type or ''
        }
        
        foods_to_avoid = recommendation_engine.get_foods_to_avoid(user_profile)
        
        return jsonify({
            'foods_to_avoid': foods_to_avoid,
            'count': len(foods_to_avoid)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    initialize_database()
    print("🚀 NutriAI Backend Starting...")
    print("📊 Database: SQLite (nutriai.db)")
    print("🤖 ML Models: Loaded")
    print("🌐 Server: http://localhost:5000")
    app.run(debug=True, port=5000)


