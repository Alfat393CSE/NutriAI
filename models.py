from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile Information
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight_kg = db.Column(db.Float)
    height_cm = db.Column(db.Float)
    bmi = db.Column(db.Float)
    
    # Health Metrics
    daily_caloric_intake = db.Column(db.Integer)
    cholesterol = db.Column(db.Float)
    blood_pressure = db.Column(db.String(20))
    glucose = db.Column(db.Float)
    
    # Lifestyle
    physical_activity_level = db.Column(db.String(50))
    weekly_exercise_hours = db.Column(db.Float)
    
    # Dietary Preferences
    dietary_restrictions = db.Column(db.String(200))
    allergies = db.Column(db.String(200))
    preferred_cuisine = db.Column(db.String(100))
    diet_goal = db.Column(db.String(100))  # Weight Loss, Muscle Gain, etc.
    
    # Disease Information
    disease_type = db.Column(db.String(100))
    severity = db.Column(db.String(50))
    
    # Relationships
    food_logs = db.relationship('FoodLog', backref='user', lazy=True, cascade='all, delete-orphan')
    meal_plans = db.relationship('MealPlan', backref='user', lazy=True, cascade='all, delete-orphan')
    chat_sessions = db.relationship('ChatSession', backref='user', lazy=True, cascade='all, delete-orphan')
    user_history = db.relationship('UserHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def calculate_bmi(self):
        if self.weight_kg and self.height_cm:
            height_m = self.height_cm / 100
            self.bmi = round(self.weight_kg / (height_m ** 2), 1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'weight_kg': self.weight_kg,
            'height_cm': self.height_cm,
            'bmi': self.bmi,
            'daily_caloric_intake': self.daily_caloric_intake,
            'cholesterol': self.cholesterol,
            'blood_pressure': self.blood_pressure,
            'glucose': self.glucose,
            'physical_activity_level': self.physical_activity_level,
            'weekly_exercise_hours': self.weekly_exercise_hours,
            'dietary_restrictions': self.dietary_restrictions,
            'allergies': self.allergies,
            'preferred_cuisine': self.preferred_cuisine,
            'diet_goal': self.diet_goal,
            'disease_type': self.disease_type,
            'severity': self.severity,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Food(db.Model):
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    category = db.Column(db.String(100))
    
    # Nutritional Information (per 100g)
    calories = db.Column(db.Float)
    protein_g = db.Column(db.Float)
    carbs_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    fiber_g = db.Column(db.Float)
    sugar_g = db.Column(db.Float)
    sodium_mg = db.Column(db.Float)
    cholesterol_mg = db.Column(db.Float)
    
    # Vitamins & Minerals
    vitamin_a = db.Column(db.Float)
    vitamin_c = db.Column(db.Float)
    calcium_mg = db.Column(db.Float)
    iron_mg = db.Column(db.Float)
    
    # Additional Info
    health_score = db.Column(db.Integer)  # 1-100
    health_rating = db.Column(db.String(50))  # Excellent, Good, Fair, Unhealthy
    common_allergens = db.Column(db.String(200))
    cuisine_type = db.Column(db.String(100))
    price_per_serving = db.Column(db.Float)
    serving_size_g = db.Column(db.Float, default=100)
    
    # ML Related
    ml_detected = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'calories': self.calories or 0,
            'protein_g': self.protein_g or 0,
            'carbs_g': self.carbs_g or 0,
            'fat_g': self.fat_g or 0,
            'fiber_g': self.fiber_g or 0,
            'sugar_g': self.sugar_g or 0,
            'sodium_mg': self.sodium_mg or 0,
            'health_score': self.health_score or 50,
            'health_rating': self.health_rating or 'Fair',
            'common_allergens': self.common_allergens or '',
            'price_per_serving': self.price_per_serving or 0,
        }


class FoodLog(db.Model):
    __tablename__ = 'food_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    
    date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(50))  # Breakfast, Lunch, Dinner, Snack
    quantity_g = db.Column(db.Float, default=100)
    
    # Calculated values
    calories_consumed = db.Column(db.Float)
    protein_consumed = db.Column(db.Float)
    carbs_consumed = db.Column(db.Float)
    fat_consumed = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    food = db.relationship('Food', backref='logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'food': self.food.to_dict() if self.food else None,
            'date': self.date.isoformat(),
            'meal_type': self.meal_type,
            'quantity_g': self.quantity_g,
            'calories_consumed': self.calories_consumed,
        }


class MealPlan(db.Model):
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200))
    week_start_date = db.Column(db.Date, nullable=False)
    
    # JSON fields for meal data
    monday = db.Column(db.Text)
    tuesday = db.Column(db.Text)
    wednesday = db.Column(db.Text)
    thursday = db.Column(db.Text)
    friday = db.Column(db.Text)
    saturday = db.Column(db.Text)
    sunday = db.Column(db.Text)
    
    # Nutritional Totals
    total_calories = db.Column(db.Float)
    total_protein = db.Column(db.Float)
    total_carbs = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    estimated_budget = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        import json
        return {
            'id': self.id,
            'name': self.name,
            'week_start_date': self.week_start_date.isoformat(),
            'monday': json.loads(self.monday) if self.monday else {},
            'tuesday': json.loads(self.tuesday) if self.tuesday else {},
            'wednesday': json.loads(self.wednesday) if self.wednesday else {},
            'thursday': json.loads(self.thursday) if self.thursday else {},
            'friday': json.loads(self.friday) if self.friday else {},
            'saturday': json.loads(self.saturday) if self.saturday else {},
            'sunday': json.loads(self.sunday) if self.sunday else {},
            'total_calories': self.total_calories,
            'total_protein': self.total_protein,
            'total_carbs': self.total_carbs,
            'total_fat': self.total_fat,
            'estimated_budget': self.estimated_budget,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }


class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    messages = db.Column(db.Text)  # JSON array of messages
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


class AdminLog(db.Model):
    __tablename__ = 'admin_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200))
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(50))
    
    admin = db.relationship('User', backref='admin_logs')


class MLPrediction(db.Model):
    __tablename__ = 'ml_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model_type = db.Column(db.String(100))  # diet_classifier, food_similarity, etc.
    input_data = db.Column(db.Text)
    prediction = db.Column(db.Text)
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_correct = db.Column(db.Boolean)  # For tracking accuracy


class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserHistory(db.Model):
    __tablename__ = 'user_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Activity Information
    action_type = db.Column(db.String(50), nullable=False)  # search, view, select, recommend, log
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    food_name = db.Column(db.String(200))
    
    # Nutritional Data
    calories = db.Column(db.Float)
    protein_g = db.Column(db.Float)
    carbs_g = db.Column(db.Float)
    fat_g = db.Column(db.Float)
    fiber_g = db.Column(db.Float)
    sugar_g = db.Column(db.Float)
    sodium_mg = db.Column(db.Float)
    
    # Health Metrics
    health_score = db.Column(db.Integer)
    health_rating = db.Column(db.String(50))
    
    # Context
    search_query = db.Column(db.String(200))  # If it was a search
    recommendation_reason = db.Column(db.String(500))  # If it was recommended
    quantity_g = db.Column(db.Float)  # If food was logged/consumed
    
    # Metadata
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    session_id = db.Column(db.String(100))
    source = db.Column(db.String(50))  # web, mobile, api
    
    # Relationships
    food = db.relationship('Food', backref='history_entries')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action_type': self.action_type,
            'food_id': self.food_id,
            'food_name': self.food_name,
            'calories': self.calories,
            'protein_g': self.protein_g,
            'carbs_g': self.carbs_g,
            'fat_g': self.fat_g,
            'fiber_g': self.fiber_g,
            'sugar_g': self.sugar_g,
            'sodium_mg': self.sodium_mg,
            'health_score': self.health_score,
            'health_rating': self.health_rating,
            'search_query': self.search_query,
            'recommendation_reason': self.recommendation_reason,
            'quantity_g': self.quantity_g,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'session_id': self.session_id,
            'source': self.source
        }

