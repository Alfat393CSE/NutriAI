import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import json
from datetime import datetime, timedelta
import random

class FoodSimilarityEngine:
    """TF-IDF based food similarity search"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.food_vectors = None
        self.food_data = []
    
    def fit(self, foods):
        """Train on food database"""
        self.food_data = foods
        # Create text representation of foods
        food_texts = [
            f"{f['name']} {f['category']} {f.get('cuisine_type', '')} "
            f"protein{int(f.get('protein_g', 0))} carbs{int(f.get('carbs_g', 0))} "
            f"fat{int(f.get('fat_g', 0))} calories{int(f.get('calories', 0))}"
            for f in foods
        ]
        self.food_vectors = self.vectorizer.fit_transform(food_texts)
        return self
    
    def find_similar(self, food_name, n=5):
        """Find n similar foods"""
        if self.food_vectors is None or len(self.food_data) == 0:
            return []
        
        # Convert food_name to string to handle any type issues
        food_name = str(food_name).lower()
        
        # Find the food
        food_idx = None
        for idx, food in enumerate(self.food_data):
            if str(food.get('name', '')).lower() == food_name:
                food_idx = int(idx)  # Ensure it's a Python int
                break
        
        if food_idx is None:
            return []
        
        # Calculate similarities
        similarities = cosine_similarity(
            self.food_vectors[food_idx:food_idx+1],
            self.food_vectors
        ).flatten()
        
        # Get top n similar (excluding itself)
        # Convert to numpy array explicitly and get indices
        similar_indices = np.argsort(similarities)[-n-1:-1][::-1]
        
        results = []
        for numpy_idx in similar_indices:
            idx = int(numpy_idx)  # Convert numpy type to Python int
            if idx != food_idx:
                results.append({
                    'food': self.food_data[idx],
                    'similarity_score': float(similarities[idx])
                })
        
        return results


class DietGoalClassifier:
    """Predicts optimal diet based on user profile"""
    
    def __init__(self, model_path='best_model.pkl'):
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except:
            self.model = None
    
    def predict(self, user_profile):
        """Predict diet recommendation"""
        if not self.model:
            return self._rule_based_prediction(user_profile)
        
        try:
            # Prepare features
            features_df = self._prepare_features(user_profile)
            prediction = self.model.predict(features_df)[0]
            
            # Get probability/confidence if available
            confidence = 0.85
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(features_df)
                confidence = float(np.max(proba))
            
            return {
                'diet_type': prediction,
                'confidence': confidence
            }
        except:
            return self._rule_based_prediction(user_profile)
    
    def _prepare_features(self, profile):
        """Convert user profile to model features"""
        numeric_features = [
            profile.get('age', 30),
            profile.get('weight_kg', 70),
            profile.get('height_cm', 170),
            profile.get('bmi', 24),
            profile.get('daily_caloric_intake', 2000),
            profile.get('cholesterol', 180),
            profile.get('blood_pressure', 120),
            profile.get('glucose', 100),
            profile.get('weekly_exercise_hours', 3),
            profile.get('adherence_to_diet_plan', 70),
            profile.get('dietary_nutrient_imbalance_score', 2)
        ]
        
        categorical_features = [
            profile.get('gender', 'Male'),
            profile.get('disease_type', 'None'),
            profile.get('severity', 'Mild'),
            profile.get('physical_activity_level', 'Moderate'),
            profile.get('dietary_restrictions', 'None'),
            profile.get('allergies', 'None'),
            profile.get('preferred_cuisine', 'Italian')
        ]
        
        columns = [
            "Age", "Weight_kg", "Height_cm", "BMI", "Daily_Caloric_Intake",
            "Cholesterol_mg/dL", "Blood_Pressure_mmHg", "Glucose_mg/dL",
            "Weekly_Exercise_Hours", "Adherence_to_Diet_Plan",
            "Dietary_Nutrient_Imbalance_Score",
            "Gender", "Disease_Type", "Severity", "Physical_Activity_Level",
            "Dietary_Restrictions", "Allergies", "Preferred_Cuisine"
        ]
        
        return pd.DataFrame([numeric_features + categorical_features], columns=columns)
    
    def _rule_based_prediction(self, profile):
        """Fallback rule-based prediction"""
        bmi = profile.get('bmi', 24)
        disease = profile.get('disease_type', 'None')
        goal = (profile.get('diet_goal') or '').lower()
        
        if disease == 'Diabetes' or profile.get('glucose', 100) > 140:
            return {'diet_type': 'Low_Carb', 'confidence': 0.80}
        elif disease == 'Hypertension' or profile.get('blood_pressure', 120) > 140:
            return {'diet_type': 'Low_Sodium', 'confidence': 0.80}
        elif bmi > 30 or 'weight loss' in goal:
            return {'diet_type': 'Low_Calorie', 'confidence': 0.75}
        elif 'muscle' in goal or 'protein' in goal:
            return {'diet_type': 'High_Protein', 'confidence': 0.75}
        else:
            return {'diet_type': 'Balanced', 'confidence': 0.70}


class MealPlanGenerator:
    """Creates personalized 7-day meal plans"""
    
    def __init__(self, food_database):
        self.foods = food_database
    
    def generate_plan(self, user_profile, diet_type='Balanced'):
        """Generate 7-day meal plan"""
        daily_calories = user_profile.get('daily_caloric_intake') or 2000
        dietary_restrictions = (user_profile.get('dietary_restrictions') or '').lower()
        allergies_str = (user_profile.get('allergies') or '')
        if isinstance(allergies_str, list):
            allergies = [str(a).lower() for a in allergies_str]
        else:
            allergies = str(allergies_str).lower().split(',')
        budget = user_profile.get('budget_per_day') or 20
        
        # Filter foods based on restrictions
        available_foods = self._filter_foods(diet_type, dietary_restrictions, allergies)
        
        meal_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            daily_meals = self._generate_daily_meals(
                available_foods,
                daily_calories,
                budget
            )
            meal_plan[day.lower()] = daily_meals
        
        # Calculate totals
        totals = self._calculate_totals(meal_plan)
        
        return {
            'meal_plan': meal_plan,
            'totals': totals
        }
    
    def _filter_foods(self, diet_type, restrictions, allergies):
        """Filter foods based on diet and restrictions"""
        filtered = []
        
        for food in self.foods:
            # Check allergens
            food_allergens = str(food.get('common_allergens', '')).lower()
            if any(str(allergy).strip() in food_allergens for allergy in allergies if str(allergy).strip()):
                continue
            
            # Check diet type
            if diet_type == 'Low_Carb' and food.get('carbs_g', 0) > 20:
                continue
            elif diet_type == 'Low_Sodium' and food.get('sodium_mg', 0) > 300:
                continue
            elif diet_type == 'High_Protein' and food.get('protein_g', 0) < 10:
                continue
            
            filtered.append(food)
        
        return filtered if filtered else self.foods
    
    def _generate_daily_meals(self, foods, daily_calories, budget):
        """Generate meals for one day"""
        # Calorie distribution: Breakfast 25%, Lunch 35%, Dinner 30%, Snack 10%
        target_cals = {
            'Breakfast': daily_calories * 0.25,
            'Lunch': daily_calories * 0.35,
            'Dinner': daily_calories * 0.30,
            'Snack': daily_calories * 0.10
        }
        
        meals = {}
        for meal_type, target in target_cals.items():
            # Select random foods that fit the calorie target
            selected = self._select_meal_items(foods, target, budget / 4)
            meals[meal_type] = selected
        
        return meals
    
    def _select_meal_items(self, foods, target_calories, budget):
        """Select food items for a meal"""
        if not foods:
            return []
        
        selected = []
        remaining_cals = target_calories
        remaining_budget = budget
        
        # Try to get 1-3 items per meal
        num_items = random.randint(1, 3)
        
        for _ in range(num_items):
            if remaining_cals <= 0 or not foods:
                break
            
            # Filter foods that fit budget and calories
            suitable = [
                f for f in foods
                if f.get('calories', 0) <= remaining_cals * 1.5
                and f.get('price_per_serving', 0) <= remaining_budget
            ]
            
            if not suitable:
                suitable = foods
            
            food = random.choice(suitable)
            quantity = min(150, max(50, remaining_cals / max(food.get('calories', 100), 1)))
            
            selected.append({
                'food_id': food['id'],
                'name': food['name'],
                'quantity_g': round(quantity, 1),
                'calories': round(food.get('calories', 0) * quantity / 100, 1),
                'protein': round(food.get('protein_g', 0) * quantity / 100, 1),
                'carbs': round(food.get('carbs_g', 0) * quantity / 100, 1),
                'fat': round(food.get('fat_g', 0) * quantity / 100, 1),
            })
            
            remaining_cals -= selected[-1]['calories']
            remaining_budget -= food.get('price_per_serving', 0)
        
        return selected
    
    def _calculate_totals(self, meal_plan):
        """Calculate weekly totals"""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for day, meals in meal_plan.items():
            for meal_type, items in meals.items():
                for item in items:
                    total_calories += item.get('calories', 0)
                    total_protein += item.get('protein', 0)
                    total_carbs += item.get('carbs', 0)
                    total_fat += item.get('fat', 0)
        
        return {
            'total_calories': round(total_calories, 1),
            'total_protein': round(total_protein, 1),
            'total_carbs': round(total_carbs, 1),
            'total_fat': round(total_fat, 1),
            'daily_avg_calories': round(total_calories / 7, 1)
        }


class CNNFoodClassifier:
    """Placeholder for CNN-based food image recognition"""
    
    def __init__(self):
        self.model = None
        self.labels = []
    
    def predict_from_image(self, image_path):
        """Predict food from image (placeholder)"""
        # This would integrate with a trained CNN model
        return {
            'food_name': 'Apple',
            'confidence': 0.92,
            'message': 'CNN model not yet trained. This is a placeholder.'
        }
    
    def train(self, image_dataset):
        """Train CNN model (placeholder)"""
        pass


class ChatbotEngine:
    """Natural language understanding for diet chatbot"""
    
    def __init__(self, food_database):
        self.foods = food_database
        self.intents = self._load_intents()
    
    def _load_intents(self):
        """Define intent patterns"""
        return {
            'food_info': ['what is', 'tell me about', 'nutrition of', 'calories in'],
            'recommendation': ['recommend', 'suggest', 'what should i eat', 'food for'],
            'alternative': ['alternative to', 'substitute for', 'replace', 'instead of'],
            'health_tip': ['tip', 'advice', 'help me', 'how to'],
            'meal_plan': ['meal plan', 'diet plan', 'weekly plan', 'menu'],
            'weight': ['lose weight', 'gain weight', 'weight loss', 'weight gain'],
            'macro': ['protein', 'carbs', 'fat', 'macro', 'macros'],
            'allergy': ['allergy', 'allergic', 'allergen'],
            'mood': ['mood', 'feeling', 'stressed', 'tired', 'energetic'],
            'budget': ['cheap', 'expensive', 'budget', 'affordable', 'price'],
        }
    
    def process_message(self, message, user_profile=None):
        """Process user message and generate response"""
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Generate response based on intent
        if intent == 'food_info':
            return self._handle_food_info(message_lower)
        elif intent == 'recommendation':
            return self._handle_recommendation(message_lower, user_profile)
        elif intent == 'alternative':
            return self._handle_alternative(message_lower)
        elif intent == 'health_tip':
            return self._handle_health_tip(user_profile)
        elif intent == 'mood':
            return self._handle_mood_food(message_lower)
        elif intent == 'budget':
            return self._handle_budget_food(message_lower)
        else:
            return self._default_response()
    
    def _detect_intent(self, message):
        """Detect user intent from message"""
        for intent, patterns in self.intents.items():
            if any(pattern in message for pattern in patterns):
                return intent
        return 'general'
    
    def _handle_food_info(self, message):
        """Provide food information"""
        # Extract food name from message
        for food in self.foods:
            if food['name'].lower() in message:
                return {
                    'response': f"{food['name']}: {food.get('calories', 0)} calories per 100g, "
                                f"Protein: {food.get('protein_g', 0)}g, Carbs: {food.get('carbs_g', 0)}g, "
                                f"Fat: {food.get('fat_g', 0)}g. Health Rating: {food.get('health_rating', 'N/A')}",
                    'food': food
                }
        
        return {'response': "I couldn't find that food in my database. Try searching in the Food Search page!"}
    
    def _handle_recommendation(self, message, user_profile):
        """Recommend foods based on context"""
        if user_profile:
            diet_goal = (user_profile.get('diet_goal') or '').lower()
            
            if 'weight loss' in diet_goal or 'lose' in message:
                foods = [f for f in self.foods if f.get('calories', 1000) < 150 and f.get('fiber_g', 0) > 3]
            elif 'muscle' in diet_goal or 'protein' in message:
                foods = [f for f in self.foods if f.get('protein_g', 0) > 15]
            else:
                foods = [f for f in self.foods if f.get('health_score', 50) > 70]
        else:
            foods = [f for f in self.foods if f.get('health_score', 50) > 70]
        
        if foods:
            recommended = random.sample(foods, min(3, len(foods)))
            response = "Here are some recommendations for you:\n"
            for food in recommended:
                response += f"• {food['name']} - {food.get('calories', 0)} cal, Health Score: {food.get('health_score', 0)}\n"
            return {'response': response, 'recommended_foods': recommended}
        
        return {'response': "Let me suggest a balanced diet with fruits, vegetables, lean proteins, and whole grains!"}
    
    def _handle_alternative(self, message):
        """Suggest food alternatives"""
        for food in self.foods:
            if food['name'].lower() in message:
                # Find healthier alternatives
                alternatives = [
                    f for f in self.foods
                    if f['category'] == food.get('category')
                    and f.get('health_score', 0) > food.get('health_score', 0)
                ][:3]
                
                if alternatives:
                    response = f"Healthier alternatives to {food['name']}:\n"
                    for alt in alternatives:
                        response += f"• {alt['name']} - {alt.get('calories', 0)} cal\n"
                    return {'response': response, 'alternatives': alternatives}
        
        return {'response': "Try swapping processed foods with whole foods, white rice with brown rice, or sugary snacks with fruits!"}
    
    def _handle_health_tip(self, user_profile):
        """Provide personalized health tips"""
        tips = [
            "💧 Drink at least 8 glasses of water daily for optimal hydration.",
            "🥗 Fill half your plate with vegetables for better nutrition.",
            "🏃 Combine diet with 30 minutes of daily exercise for best results.",
            "😴 Get 7-8 hours of sleep - it's crucial for weight management.",
            "🍽️ Practice mindful eating - eat slowly and without distractions.",
            "📱 Track your meals to stay accountable and aware of your intake.",
            "🥜 Include healthy fats like nuts and avocados for satiety.",
            "🍎 Prep meals in advance to avoid unhealthy last-minute choices.",
        ]
        
        tip = random.choice(tips)
        
        if user_profile:
            bmi = user_profile.get('bmi', 24)
            if bmi > 30:
                tip = "Focus on portion control and include more fiber-rich foods to help with weight management."
            elif bmi < 18.5:
                tip = "Consider increasing your calorie intake with nutrient-dense foods like nuts, avocados, and whole grains."
        
        return {'response': tip}
    
    def _handle_mood_food(self, message):
        """Recommend foods based on mood"""
        mood_foods = {
            'stress': ['Dark Chocolate', 'Salmon', 'Spinach', 'Avocado'],
            'tired': ['Banana', 'Oatmeal', 'Almonds', 'Sweet Potato'],
            'happy': ['Berries', 'Yogurt', 'Green Tea', 'Chicken'],
            'sad': ['Fatty Fish', 'Walnuts', 'Leafy Greens', 'Turkey']
        }
        
        for mood, foods in mood_foods.items():
            if mood in message:
                return {'response': f"For {mood} feelings, try: {', '.join(foods)}"}
        
        return {'response': "Food affects mood! Try omega-3 rich foods, complex carbs, and foods high in tryptophan."}
    
    def _handle_budget_food(self, message):
        """Recommend budget-friendly foods"""
        budget_foods = [f for f in self.foods if f.get('price_per_serving', 10) < 3]
        
        if budget_foods:
            recommendations = random.sample(budget_foods, min(5, len(budget_foods)))
            response = "Budget-friendly options:\n"
            for food in recommendations:
                response += f"• {food['name']} - ${food.get('price_per_serving', 0):.2f}\n"
            return {'response': response}
        
        return {'response': "Budget tip: Buy seasonal produce, cook in bulk, and choose whole grains like rice and oats!"}
    
    def _default_response(self):
        """Default response"""
        responses = [
            "I'm here to help with your nutrition questions! Ask me about foods, meal plans, or health tips.",
            "You can ask me about specific foods, request recommendations, or get diet advice!",
            "Try asking: 'What are the calories in chicken?' or 'Recommend foods for weight loss'",
        ]
        return {'response': random.choice(responses)}
