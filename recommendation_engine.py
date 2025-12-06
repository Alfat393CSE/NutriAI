import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


class NutritionRecommendationEngine:
    """
    Personalized Nutrition Recommendation Engine
    Analyzes user profile and provides tailored nutrition recommendations
    """
    
    def __init__(self):
        self.activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        self.goal_adjustments = {
            'weight_loss': -500,      # -500 cal deficit
            'fat_loss': -400,
            'muscle_gain': 300,       # +300 cal surplus
            'maintenance': 0,
            'diabetes_friendly': -200,
            'heart_healthy': -100,
            'general_health': 0
        }
        
        # Macro ratios for different goals (protein, carbs, fat)
        self.macro_ratios = {
            'weight_loss': (0.30, 0.40, 0.30),
            'fat_loss': (0.35, 0.35, 0.30),
            'muscle_gain': (0.30, 0.45, 0.25),
            'maintenance': (0.25, 0.45, 0.30),
            'diabetes_friendly': (0.25, 0.40, 0.35),
            'heart_healthy': (0.25, 0.50, 0.25),
            'general_health': (0.25, 0.45, 0.30)
        }
    
    def calculate_bmr(self, age, gender, weight_kg, height_cm):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        return bmr
    
    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        multiplier = self.activity_multipliers.get(activity_level.lower().replace(' ', '_'), 1.2)
        return bmr * multiplier
    
    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate Body Mass Index"""
        height_m = height_cm / 100
        return weight_kg / (height_m ** 2)
    
    def get_calorie_target(self, user_profile):
        """Calculate personalized calorie target"""
        age = user_profile.get('age', 30)
        gender = user_profile.get('gender', 'male')
        weight = user_profile.get('weight_kg', 70)
        height = user_profile.get('height_cm', 170)
        activity = user_profile.get('physical_activity_level', 'moderate')
        goal = user_profile.get('diet_goal', 'maintenance')
        
        # Calculate BMR and TDEE
        bmr = self.calculate_bmr(age, gender, weight, height)
        tdee = self.calculate_tdee(bmr, activity)
        
        # Adjust for goal
        goal_key = goal.lower().replace(' ', '_')
        adjustment = self.goal_adjustments.get(goal_key, 0)
        
        target_calories = int(tdee + adjustment)
        
        # Safety bounds
        if target_calories < 1200:
            target_calories = 1200
        elif target_calories > 4000:
            target_calories = 4000
        
        return {
            'target_calories': target_calories,
            'bmr': int(bmr),
            'tdee': int(tdee),
            'adjustment': adjustment
        }
    
    def calculate_macros(self, calories, goal):
        """Calculate macro distribution"""
        goal_key = goal.lower().replace(' ', '_')
        protein_ratio, carb_ratio, fat_ratio = self.macro_ratios.get(
            goal_key, (0.25, 0.45, 0.30)
        )
        
        # Calculate grams
        protein_g = int((calories * protein_ratio) / 4)  # 4 cal per gram
        carbs_g = int((calories * carb_ratio) / 4)       # 4 cal per gram
        fat_g = int((calories * fat_ratio) / 9)          # 9 cal per gram
        
        return {
            'protein_g': protein_g,
            'carbs_g': carbs_g,
            'fat_g': fat_g,
            'protein_percentage': int(protein_ratio * 100),
            'carbs_percentage': int(carb_ratio * 100),
            'fat_percentage': int(fat_ratio * 100)
        }
    
    def calculate_nutrient_score(self, food, goal, restrictions=None):
        """
        Calculate a nutrient score for a food based on user goal
        Higher score = better fit for user's goals
        """
        score = 0
        goal_key = goal.lower().replace(' ', '_')
        
        # Get food nutritional values
        calories = food.get('calories', 0)
        protein = food.get('protein_g', 0)
        carbs = food.get('carbs_g', 0)
        fat = food.get('fat_g', 0)
        fiber = food.get('fiber_g', 0)
        sugar = food.get('sugar_g', 0)
        sodium = food.get('sodium_mg', 0)
        health_score = food.get('health_score', 50)
        
        # Base health score
        score += health_score
        
        # Goal-specific scoring
        if 'weight_loss' in goal_key or 'fat_loss' in goal_key:
            score += (protein * 3)           # High protein good
            score -= (calories / 10)         # Low calorie good
            score += (fiber * 5)             # High fiber good
            score -= (sugar / 2)             # Low sugar good
            
        elif 'muscle_gain' in goal_key:
            score += (protein * 5)           # Very high protein good
            score += (carbs / 5)             # Moderate carbs good
            score += (calories / 20)         # Higher calories ok
            
        elif 'diabetes_friendly' in goal_key:
            score -= (sugar * 3)             # Very low sugar important
            score -= (carbs / 3)             # Lower carbs important
            score += (fiber * 6)             # High fiber very important
            score += (protein * 2)           # Moderate protein good
            
        elif 'heart_healthy' in goal_key:
            score -= (sodium / 50)           # Low sodium important
            score -= (fat * 2)               # Lower fat important
            score += (fiber * 5)             # High fiber important
            score += (protein * 2)           # Moderate protein good
            
        else:  # general_health, maintenance
            score += (protein * 2)
            score += (fiber * 3)
            score -= (sugar / 3)
            score -= (sodium / 100)
        
        # Apply dietary restrictions penalty
        if restrictions:
            restrictions_list = [r.strip().lower() for r in restrictions.split(',')]
            food_name = food.get('name', '').lower()
            food_category = food.get('category', '').lower()
            
            # Check for allergens and restrictions
            if any(r in food_name or r in food_category for r in restrictions_list):
                score = -1000  # Exclude this food
        
        return max(0, score)
    
    def rank_foods(self, foods, user_profile):
        """
        Rank foods based on user profile and goals
        Returns sorted list with scores
        """
        goal = user_profile.get('diet_goal', 'general_health')
        restrictions = user_profile.get('dietary_restrictions', '')
        allergies = user_profile.get('allergies', '')
        
        # Combine restrictions and allergies
        all_restrictions = f"{restrictions}, {allergies}".strip(', ')
        
        # Calculate scores for all foods
        scored_foods = []
        for food in foods:
            score = self.calculate_nutrient_score(food, goal, all_restrictions)
            if score >= 0:  # Only include non-excluded foods
                scored_foods.append({
                    'food': food,
                    'score': score,
                    'fit_percentage': min(100, int((score / 200) * 100))
                })
        
        # Sort by score
        scored_foods.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_foods
    
    def get_foods_to_avoid(self, user_profile):
        """
        Return foods/categories to avoid based on user profile
        """
        goal = user_profile.get('diet_goal', '').lower()
        restrictions = user_profile.get('dietary_restrictions', '').lower()
        allergies = user_profile.get('allergies', '').lower()
        disease = user_profile.get('disease_type', '').lower()
        
        avoid_list = []
        
        # Based on goal
        if 'weight_loss' in goal or 'fat_loss' in goal:
            avoid_list.extend([
                {'item': 'High-sugar foods', 'reason': 'Can spike insulin and hinder fat loss'},
                {'item': 'Fried foods', 'reason': 'High in calories and unhealthy fats'},
                {'item': 'Processed snacks', 'reason': 'Low nutrition, high calories'},
                {'item': 'Sugary beverages', 'reason': 'Empty calories without satiety'}
            ])
        
        elif 'muscle_gain' in goal:
            avoid_list.extend([
                {'item': 'Alcohol', 'reason': 'Interferes with muscle protein synthesis'},
                {'item': 'Low-protein foods', 'reason': 'Insufficient for muscle building'},
                {'item': 'Excessive cardio', 'reason': 'Can interfere with muscle recovery'}
            ])
        
        elif 'diabetes' in goal or 'diabetes' in disease:
            avoid_list.extend([
                {'item': 'High-GI foods', 'reason': 'Cause rapid blood sugar spikes'},
                {'item': 'White bread/rice', 'reason': 'Quickly converted to glucose'},
                {'item': 'Sugary desserts', 'reason': 'Dangerous for blood sugar control'},
                {'item': 'Fruit juices', 'reason': 'High sugar without fiber'}
            ])
        
        elif 'heart' in goal or 'cardiovascular' in disease:
            avoid_list.extend([
                {'item': 'High-sodium foods', 'reason': 'Increases blood pressure'},
                {'item': 'Saturated fats', 'reason': 'Raises LDL cholesterol'},
                {'item': 'Trans fats', 'reason': 'Extremely harmful to heart health'},
                {'item': 'Processed meats', 'reason': 'High in sodium and preservatives'}
            ])
        
        # Based on restrictions and allergies
        restriction_list = [r.strip() for r in f"{restrictions},{allergies}".split(',') if r.strip()]
        for restriction in restriction_list:
            avoid_list.append({
                'item': restriction.title(),
                'reason': 'Dietary restriction or allergy'
            })
        
        return avoid_list
    
    def generate_recommendations(self, user_profile, all_foods):
        """
        Generate complete personalized recommendations
        """
        # Calculate calorie target and macros
        calorie_info = self.get_calorie_target(user_profile)
        target_calories = calorie_info['target_calories']
        macros = self.calculate_macros(target_calories, user_profile.get('diet_goal', 'maintenance'))
        
        # Calculate BMI
        bmi = self.calculate_bmi(
            user_profile.get('weight_kg', 70),
            user_profile.get('height_cm', 170)
        )
        
        # Get BMI category
        if bmi < 18.5:
            bmi_category = 'Underweight'
            bmi_advice = 'Consider increasing calorie intake with nutrient-dense foods'
        elif bmi < 25:
            bmi_category = 'Normal weight'
            bmi_advice = 'Maintain your current healthy weight with balanced nutrition'
        elif bmi < 30:
            bmi_category = 'Overweight'
            bmi_advice = 'Consider a moderate calorie deficit and regular exercise'
        else:
            bmi_category = 'Obese'
            bmi_advice = 'Consult a healthcare provider for a personalized weight loss plan'
        
        # Rank all foods
        ranked_foods = self.rank_foods(all_foods, user_profile)
        
        # Get top recommendations
        top_foods = ranked_foods[:10]
        
        # Get foods to avoid
        foods_to_avoid = self.get_foods_to_avoid(user_profile)
        
        # Generate meal suggestions
        meal_suggestions = self._generate_meal_suggestions(ranked_foods)
        
        # Calculate nutrition targets for different meals
        meal_distribution = {
            'breakfast': int(target_calories * 0.30),
            'lunch': int(target_calories * 0.35),
            'dinner': int(target_calories * 0.30),
            'snacks': int(target_calories * 0.05)
        }
        
        return {
            'user_profile': {
                'age': user_profile.get('age'),
                'gender': user_profile.get('gender'),
                'weight_kg': user_profile.get('weight_kg'),
                'height_cm': user_profile.get('height_cm'),
                'bmi': round(bmi, 2),
                'bmi_category': bmi_category,
                'bmi_advice': bmi_advice,
                'activity_level': user_profile.get('physical_activity_level'),
                'goal': user_profile.get('diet_goal')
            },
            'calorie_target': calorie_info,
            'macros': macros,
            'top_recommended_foods': top_foods,
            'foods_to_avoid': foods_to_avoid,
            'meal_suggestions': meal_suggestions,
            'meal_distribution': meal_distribution,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_meal_suggestions(self, ranked_foods):
        """Generate meal suggestions from ranked foods"""
        suggestions = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': []
        }
        
        # Categorize foods by typical meal time
        for item in ranked_foods[:20]:
            food = item['food']
            category = food.get('category', '').lower()
            name = food.get('name', '').lower()
            
            # Breakfast foods
            if any(word in name for word in ['egg', 'oat', 'yogurt', 'milk', 'cereal']):
                suggestions['breakfast'].append(food)
            # Snack foods
            elif any(word in name for word in ['nuts', 'fruit', 'berry', 'apple', 'banana']):
                suggestions['snacks'].append(food)
            # Dinner/Lunch proteins
            elif any(word in category for word in ['protein', 'meat', 'fish']):
                if len(suggestions['dinner']) < 3:
                    suggestions['dinner'].append(food)
                else:
                    suggestions['lunch'].append(food)
            # General
            else:
                if len(suggestions['lunch']) < 3:
                    suggestions['lunch'].append(food)
                elif len(suggestions['dinner']) < 3:
                    suggestions['dinner'].append(food)
        
        # Limit to 3 per meal
        for meal in suggestions:
            suggestions[meal] = suggestions[meal][:3]
        
        return suggestions
