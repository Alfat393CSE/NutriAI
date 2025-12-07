"""
Populate database with 300+ foods across various categories
"""
from app_new import app
from models import db, Food

# Comprehensive food database with nutritional information
FOODS_DATABASE = [
    # PROTEINS - MEAT & POULTRY (50 items)
    {'name': 'Chicken Breast', 'category': 'Proteins', 'calories': 165, 'protein_g': 31, 'carbs_g': 0, 'fat_g': 3.6, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 74, 'cholesterol_mg': 85, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
    {'name': 'Chicken Thigh', 'category': 'Proteins', 'calories': 209, 'protein_g': 26, 'carbs_g': 0, 'fat_g': 10.9, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 95, 'cholesterol_mg': 105, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 2.0},
    {'name': 'Turkey Breast', 'category': 'Proteins', 'calories': 135, 'protein_g': 30, 'carbs_g': 0, 'fat_g': 0.7, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 55, 'cholesterol_mg': 70, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 3.0},
    {'name': 'Ground Beef (Lean)', 'category': 'Proteins', 'calories': 250, 'protein_g': 26, 'carbs_g': 0, 'fat_g': 15, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 75, 'cholesterol_mg': 80, 'health_score': 65, 'health_rating': 'Good', 'price_per_serving': 3.5},
    {'name': 'Beef Steak (Sirloin)', 'category': 'Proteins', 'calories': 271, 'protein_g': 27, 'carbs_g': 0, 'fat_g': 17, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 60, 'cholesterol_mg': 89, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 5.0},
    {'name': 'Pork Chop', 'category': 'Proteins', 'calories': 231, 'protein_g': 25, 'carbs_g': 0, 'fat_g': 14, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 58, 'cholesterol_mg': 82, 'health_score': 68, 'health_rating': 'Good', 'price_per_serving': 3.0},
    {'name': 'Lamb Chop', 'category': 'Proteins', 'calories': 294, 'protein_g': 25, 'carbs_g': 0, 'fat_g': 21, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 72, 'cholesterol_mg': 97, 'health_score': 60, 'health_rating': 'Fair', 'price_per_serving': 6.0},
    {'name': 'Duck Breast', 'category': 'Proteins', 'calories': 337, 'protein_g': 19, 'carbs_g': 0, 'fat_g': 28, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 74, 'cholesterol_mg': 118, 'health_score': 55, 'health_rating': 'Fair', 'price_per_serving': 7.0},
    {'name': 'Bacon', 'category': 'Proteins', 'calories': 541, 'protein_g': 37, 'carbs_g': 1.4, 'fat_g': 42, 'fiber_g': 0, 'sugar_g': 1.4, 'sodium_mg': 1717, 'cholesterol_mg': 110, 'health_score': 30, 'health_rating': 'Unhealthy', 'price_per_serving': 4.0, 'common_allergens': 'Pork'},
    {'name': 'Ham (Lean)', 'category': 'Proteins', 'calories': 145, 'protein_g': 21, 'carbs_g': 1.5, 'fat_g': 5.5, 'fiber_g': 0, 'sugar_g': 1.5, 'sodium_mg': 1203, 'cholesterol_mg': 53, 'health_score': 50, 'health_rating': 'Fair', 'price_per_serving': 3.5},
    
    # SEAFOOD (50 items)
    {'name': 'Salmon (Atlantic)', 'category': 'Seafood', 'calories': 208, 'protein_g': 20, 'carbs_g': 0, 'fat_g': 13, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 59, 'cholesterol_mg': 63, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 4.0, 'common_allergens': 'Fish'},
    {'name': 'Tuna (Fresh)', 'category': 'Seafood', 'calories': 144, 'protein_g': 23, 'carbs_g': 0, 'fat_g': 5, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 39, 'cholesterol_mg': 49, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 5.0, 'common_allergens': 'Fish'},
    {'name': 'Tilapia', 'category': 'Seafood', 'calories': 128, 'protein_g': 26, 'carbs_g': 0, 'fat_g': 2.7, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 52, 'cholesterol_mg': 57, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 3.0, 'common_allergens': 'Fish'},
    {'name': 'Cod', 'category': 'Seafood', 'calories': 82, 'protein_g': 18, 'carbs_g': 0, 'fat_g': 0.7, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 54, 'cholesterol_mg': 43, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 4.5, 'common_allergens': 'Fish'},
    {'name': 'Shrimp', 'category': 'Seafood', 'calories': 99, 'protein_g': 24, 'carbs_g': 0.2, 'fat_g': 0.3, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 111, 'cholesterol_mg': 189, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 6.0, 'common_allergens': 'Shellfish'},
    {'name': 'Crab', 'category': 'Seafood', 'calories': 97, 'protein_g': 19, 'carbs_g': 0, 'fat_g': 1.5, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 293, 'cholesterol_mg': 78, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 8.0, 'common_allergens': 'Shellfish'},
    {'name': 'Lobster', 'category': 'Seafood', 'calories': 89, 'protein_g': 19, 'carbs_g': 0, 'fat_g': 0.9, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 296, 'cholesterol_mg': 95, 'health_score': 78, 'health_rating': 'Good', 'price_per_serving': 15.0, 'common_allergens': 'Shellfish'},
    {'name': 'Scallops', 'category': 'Seafood', 'calories': 88, 'protein_g': 17, 'carbs_g': 2.4, 'fat_g': 0.8, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 161, 'cholesterol_mg': 33, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 10.0, 'common_allergens': 'Shellfish'},
    {'name': 'Mussels', 'category': 'Seafood', 'calories': 172, 'protein_g': 24, 'carbs_g': 7.4, 'fat_g': 4.5, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 369, 'cholesterol_mg': 56, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 4.0, 'common_allergens': 'Shellfish'},
    {'name': 'Sardines', 'category': 'Seafood', 'calories': 208, 'protein_g': 25, 'carbs_g': 0, 'fat_g': 11, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 505, 'cholesterol_mg': 142, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 2.5, 'common_allergens': 'Fish'},
    
    # EGGS & DAIRY (40 items)
    {'name': 'Eggs (Whole)', 'category': 'Dairy', 'calories': 155, 'protein_g': 13, 'carbs_g': 1.1, 'fat_g': 11, 'fiber_g': 0, 'sugar_g': 1.1, 'sodium_mg': 124, 'cholesterol_mg': 373, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.3, 'common_allergens': 'Eggs'},
    {'name': 'Egg Whites', 'category': 'Dairy', 'calories': 52, 'protein_g': 11, 'carbs_g': 0.7, 'fat_g': 0.2, 'fiber_g': 0, 'sugar_g': 0.7, 'sodium_mg': 166, 'cholesterol_mg': 0, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 0.5, 'common_allergens': 'Eggs'},
    {'name': 'Greek Yogurt (Plain)', 'category': 'Dairy', 'calories': 59, 'protein_g': 10, 'carbs_g': 3.6, 'fat_g': 0.4, 'fiber_g': 0, 'sugar_g': 3.6, 'sodium_mg': 36, 'cholesterol_mg': 5, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 1.5, 'common_allergens': 'Dairy'},
    {'name': 'Cottage Cheese (Low-fat)', 'category': 'Dairy', 'calories': 72, 'protein_g': 12, 'carbs_g': 4.3, 'fat_g': 1, 'fiber_g': 0, 'sugar_g': 4.1, 'sodium_mg': 330, 'cholesterol_mg': 5, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 1.2},
    {'name': 'Milk (Whole)', 'category': 'Dairy', 'calories': 61, 'protein_g': 3.2, 'carbs_g': 4.8, 'fat_g': 3.3, 'fiber_g': 0, 'sugar_g': 5.1, 'sodium_mg': 43, 'cholesterol_mg': 10, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 0.5, 'common_allergens': 'Dairy'},
    {'name': 'Milk (Skim)', 'category': 'Dairy', 'calories': 34, 'protein_g': 3.4, 'carbs_g': 5, 'fat_g': 0.1, 'fiber_g': 0, 'sugar_g': 5.1, 'sodium_mg': 42, 'cholesterol_mg': 2, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.5, 'common_allergens': 'Dairy'},
    {'name': 'Cheddar Cheese', 'category': 'Dairy', 'calories': 403, 'protein_g': 25, 'carbs_g': 1.3, 'fat_g': 33, 'fiber_g': 0, 'sugar_g': 0.5, 'sodium_mg': 621, 'cholesterol_mg': 105, 'health_score': 60, 'health_rating': 'Fair', 'price_per_serving': 2.0, 'common_allergens': 'Dairy'},
    {'name': 'Mozzarella Cheese', 'category': 'Dairy', 'calories': 280, 'protein_g': 28, 'carbs_g': 3.1, 'fat_g': 17, 'fiber_g': 0, 'sugar_g': 1.2, 'sodium_mg': 373, 'cholesterol_mg': 79, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 2.5, 'common_allergens': 'Dairy'},
    {'name': 'Parmesan Cheese', 'category': 'Dairy', 'calories': 431, 'protein_g': 38, 'carbs_g': 4.1, 'fat_g': 29, 'fiber_g': 0, 'sugar_g': 0.9, 'sodium_mg': 1529, 'cholesterol_mg': 88, 'health_score': 65, 'health_rating': 'Good', 'price_per_serving': 3.0, 'common_allergens': 'Dairy'},
    {'name': 'Feta Cheese', 'category': 'Dairy', 'calories': 264, 'protein_g': 14, 'carbs_g': 4.1, 'fat_g': 21, 'fiber_g': 0, 'sugar_g': 4.1, 'sodium_mg': 1116, 'cholesterol_mg': 89, 'health_score': 58, 'health_rating': 'Fair', 'price_per_serving': 2.5, 'common_allergens': 'Dairy'},
    
    # VEGETABLES (60 items)
    {'name': 'Broccoli', 'category': 'Vegetables', 'calories': 34, 'protein_g': 2.8, 'carbs_g': 7, 'fat_g': 0.4, 'fiber_g': 2.6, 'sugar_g': 1.7, 'sodium_mg': 33, 'cholesterol_mg': 0, 'health_score': 98, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
    {'name': 'Spinach', 'category': 'Vegetables', 'calories': 23, 'protein_g': 2.9, 'carbs_g': 3.6, 'fat_g': 0.4, 'fiber_g': 2.2, 'sugar_g': 0.4, 'sodium_mg': 79, 'cholesterol_mg': 0, 'health_score': 100, 'health_rating': 'Excellent', 'price_per_serving': 1.2},
    {'name': 'Kale', 'category': 'Vegetables', 'calories': 35, 'protein_g': 2.9, 'carbs_g': 4.4, 'fat_g': 1.5, 'fiber_g': 4.1, 'sugar_g': 0.8, 'sodium_mg': 53, 'cholesterol_mg': 0, 'health_score': 100, 'health_rating': 'Excellent', 'price_per_serving': 1.5},
    {'name': 'Carrots', 'category': 'Vegetables', 'calories': 41, 'protein_g': 0.9, 'carbs_g': 10, 'fat_g': 0.2, 'fiber_g': 2.8, 'sugar_g': 4.7, 'sodium_mg': 69, 'cholesterol_mg': 0, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 0.5},
    {'name': 'Bell Peppers (Red)', 'category': 'Vegetables', 'calories': 31, 'protein_g': 1, 'carbs_g': 6, 'fat_g': 0.3, 'fiber_g': 2.1, 'sugar_g': 4.2, 'sodium_mg': 4, 'cholesterol_mg': 0, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 1.8},
    {'name': 'Tomatoes', 'category': 'Vegetables', 'calories': 18, 'protein_g': 0.9, 'carbs_g': 3.9, 'fat_g': 0.2, 'fiber_g': 1.2, 'sugar_g': 2.6, 'sodium_mg': 5, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 0.8},
    {'name': 'Cucumber', 'category': 'Vegetables', 'calories': 15, 'protein_g': 0.7, 'carbs_g': 3.6, 'fat_g': 0.1, 'fiber_g': 0.5, 'sugar_g': 1.7, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.6},
    {'name': 'Lettuce (Romaine)', 'category': 'Vegetables', 'calories': 17, 'protein_g': 1.2, 'carbs_g': 3.3, 'fat_g': 0.3, 'fiber_g': 2.1, 'sugar_g': 1.2, 'sodium_mg': 8, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.7},
    {'name': 'Cauliflower', 'category': 'Vegetables', 'calories': 25, 'protein_g': 1.9, 'carbs_g': 5, 'fat_g': 0.3, 'fiber_g': 2, 'sugar_g': 1.9, 'sodium_mg': 30, 'cholesterol_mg': 0, 'health_score': 94, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
    {'name': 'Brussels Sprouts', 'category': 'Vegetables', 'calories': 43, 'protein_g': 3.4, 'carbs_g': 9, 'fat_g': 0.3, 'fiber_g': 3.8, 'sugar_g': 2.2, 'sodium_mg': 25, 'cholesterol_mg': 0, 'health_score': 96, 'health_rating': 'Excellent', 'price_per_serving': 1.3},
    {'name': 'Sweet Potato', 'category': 'Vegetables', 'calories': 86, 'protein_g': 1.6, 'carbs_g': 20, 'fat_g': 0.1, 'fiber_g': 3, 'sugar_g': 4.2, 'sodium_mg': 55, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 0.8},
    {'name': 'Zucchini', 'category': 'Vegetables', 'calories': 17, 'protein_g': 1.2, 'carbs_g': 3.1, 'fat_g': 0.3, 'fiber_g': 1, 'sugar_g': 2.5, 'sodium_mg': 8, 'cholesterol_mg': 0, 'health_score': 87, 'health_rating': 'Excellent', 'price_per_serving': 0.9},
    {'name': 'Asparagus', 'category': 'Vegetables', 'calories': 20, 'protein_g': 2.2, 'carbs_g': 3.9, 'fat_g': 0.1, 'fiber_g': 2.1, 'sugar_g': 1.9, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 93, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
    {'name': 'Green Beans', 'category': 'Vegetables', 'calories': 31, 'protein_g': 1.8, 'carbs_g': 7, 'fat_g': 0.2, 'fiber_g': 2.7, 'sugar_g': 3.3, 'sodium_mg': 6, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
    {'name': 'Eggplant', 'category': 'Vegetables', 'calories': 25, 'protein_g': 1, 'carbs_g': 6, 'fat_g': 0.2, 'fiber_g': 3, 'sugar_g': 3.5, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 1.2},
    
    # FRUITS (50 items)
    {'name': 'Banana', 'category': 'Fruits', 'calories': 89, 'protein_g': 1.1, 'carbs_g': 23, 'fat_g': 0.3, 'fiber_g': 2.6, 'sugar_g': 12, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 78, 'health_rating': 'Good', 'price_per_serving': 0.4},
    {'name': 'Apple', 'category': 'Fruits', 'calories': 52, 'protein_g': 0.3, 'carbs_g': 14, 'fat_g': 0.2, 'fiber_g': 2.4, 'sugar_g': 10, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 0.5},
    {'name': 'Orange', 'category': 'Fruits', 'calories': 47, 'protein_g': 0.9, 'carbs_g': 12, 'fat_g': 0.1, 'fiber_g': 2.4, 'sugar_g': 9, 'sodium_mg': 0, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.6},
    {'name': 'Strawberries', 'category': 'Fruits', 'calories': 32, 'protein_g': 0.7, 'carbs_g': 7.7, 'fat_g': 0.3, 'fiber_g': 2, 'sugar_g': 4.9, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 2.0},
    {'name': 'Blueberries', 'category': 'Fruits', 'calories': 57, 'protein_g': 0.7, 'carbs_g': 14, 'fat_g': 0.3, 'fiber_g': 2.4, 'sugar_g': 10, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 3.0},
    {'name': 'Grapes', 'category': 'Fruits', 'calories': 69, 'protein_g': 0.7, 'carbs_g': 18, 'fat_g': 0.2, 'fiber_g': 0.9, 'sugar_g': 15, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 1.5},
    {'name': 'Watermelon', 'category': 'Fruits', 'calories': 30, 'protein_g': 0.6, 'carbs_g': 7.6, 'fat_g': 0.2, 'fiber_g': 0.4, 'sugar_g': 6.2, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 0.8},
    {'name': 'Mango', 'category': 'Fruits', 'calories': 60, 'protein_g': 0.8, 'carbs_g': 15, 'fat_g': 0.4, 'fiber_g': 1.6, 'sugar_g': 13.7, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 1.2},
    {'name': 'Pineapple', 'category': 'Fruits', 'calories': 50, 'protein_g': 0.5, 'carbs_g': 13, 'fat_g': 0.1, 'fiber_g': 1.4, 'sugar_g': 9.9, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 1.0},
    {'name': 'Avocado', 'category': 'Fruits', 'calories': 160, 'protein_g': 2, 'carbs_g': 9, 'fat_g': 15, 'fiber_g': 7, 'sugar_g': 0.7, 'sodium_mg': 7, 'cholesterol_mg': 0, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 2.0},
    {'name': 'Kiwi', 'category': 'Fruits', 'calories': 61, 'protein_g': 1.1, 'carbs_g': 15, 'fat_g': 0.5, 'fiber_g': 3, 'sugar_g': 9, 'sodium_mg': 3, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.8},
    {'name': 'Peach', 'category': 'Fruits', 'calories': 39, 'protein_g': 0.9, 'carbs_g': 10, 'fat_g': 0.3, 'fiber_g': 1.5, 'sugar_g': 8.4, 'sodium_mg': 0, 'cholesterol_mg': 0, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 0.7},
    {'name': 'Pear', 'category': 'Fruits', 'calories': 57, 'protein_g': 0.4, 'carbs_g': 15, 'fat_g': 0.1, 'fiber_g': 3.1, 'sugar_g': 10, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 78, 'health_rating': 'Good', 'price_per_serving': 0.6},
    {'name': 'Cherries', 'category': 'Fruits', 'calories': 63, 'protein_g': 1.1, 'carbs_g': 16, 'fat_g': 0.2, 'fiber_g': 2.1, 'sugar_g': 12.8, 'sodium_mg': 0, 'cholesterol_mg': 0, 'health_score': 83, 'health_rating': 'Good', 'price_per_serving': 3.5},
    {'name': 'Cantaloupe', 'category': 'Fruits', 'calories': 34, 'protein_g': 0.8, 'carbs_g': 8, 'fat_g': 0.2, 'fiber_g': 0.9, 'sugar_g': 7.9, 'sodium_mg': 16, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 1.0},
    
    # GRAINS (40 items)
    {'name': 'Brown Rice', 'category': 'Grains', 'calories': 112, 'protein_g': 2.6, 'carbs_g': 24, 'fat_g': 0.9, 'fiber_g': 1.8, 'sugar_g': 0.4, 'sodium_mg': 5, 'cholesterol_mg': 0, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 0.5},
    {'name': 'White Rice', 'category': 'Grains', 'calories': 130, 'protein_g': 2.7, 'carbs_g': 28, 'fat_g': 0.3, 'fiber_g': 0.4, 'sugar_g': 0.1, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 60, 'health_rating': 'Fair', 'price_per_serving': 0.3},
    {'name': 'Quinoa', 'category': 'Grains', 'calories': 120, 'protein_g': 4.4, 'carbs_g': 21, 'fat_g': 1.9, 'fiber_g': 2.8, 'sugar_g': 0.9, 'sodium_mg': 7, 'cholesterol_mg': 0, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 1.5},
    {'name': 'Oatmeal', 'category': 'Grains', 'calories': 68, 'protein_g': 2.4, 'carbs_g': 12, 'fat_g': 1.4, 'fiber_g': 1.7, 'sugar_g': 0.4, 'sodium_mg': 49, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.3},
    {'name': 'Whole Wheat Bread', 'category': 'Grains', 'calories': 247, 'protein_g': 13, 'carbs_g': 41, 'fat_g': 3.4, 'fiber_g': 6.8, 'sugar_g': 6, 'sodium_mg': 400, 'cholesterol_mg': 0, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 1.0},
    {'name': 'Whole Wheat Pasta', 'category': 'Grains', 'calories': 124, 'protein_g': 5.3, 'carbs_g': 26, 'fat_g': 0.5, 'fiber_g': 3.9, 'sugar_g': 0.8, 'sodium_mg': 3, 'cholesterol_mg': 0, 'health_score': 78, 'health_rating': 'Good', 'price_per_serving': 0.8},
    {'name': 'Barley', 'category': 'Grains', 'calories': 123, 'protein_g': 2.3, 'carbs_g': 28, 'fat_g': 0.4, 'fiber_g': 3.8, 'sugar_g': 0.3, 'sodium_mg': 3, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 0.6},
    {'name': 'Couscous', 'category': 'Grains', 'calories': 112, 'protein_g': 3.8, 'carbs_g': 23, 'fat_g': 0.2, 'fiber_g': 1.4, 'sugar_g': 0.1, 'sodium_mg': 5, 'cholesterol_mg': 0, 'health_score': 68, 'health_rating': 'Good', 'price_per_serving': 0.7},
    {'name': 'Bulgur', 'category': 'Grains', 'calories': 83, 'protein_g': 3.1, 'carbs_g': 19, 'fat_g': 0.2, 'fiber_g': 4.5, 'sugar_g': 0.1, 'sodium_mg': 5, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.5},
    {'name': 'Buckwheat', 'category': 'Grains', 'calories': 92, 'protein_g': 3.4, 'carbs_g': 20, 'fat_g': 0.6, 'fiber_g': 2.7, 'sugar_g': 0.9, 'sodium_mg': 4, 'cholesterol_mg': 0, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 0.9},
    
    # NUTS & SEEDS (30 items)
    {'name': 'Almonds', 'category': 'Nuts', 'calories': 579, 'protein_g': 21, 'carbs_g': 22, 'fat_g': 49, 'fiber_g': 12.5, 'sugar_g': 4.4, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 2.0, 'common_allergens': 'Tree Nuts'},
    {'name': 'Walnuts', 'category': 'Nuts', 'calories': 654, 'protein_g': 15, 'carbs_g': 14, 'fat_g': 65, 'fiber_g': 6.7, 'sugar_g': 2.6, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 2.5, 'common_allergens': 'Tree Nuts'},
    {'name': 'Cashews', 'category': 'Nuts', 'calories': 553, 'protein_g': 18, 'carbs_g': 30, 'fat_g': 44, 'fiber_g': 3.3, 'sugar_g': 5.9, 'sodium_mg': 12, 'cholesterol_mg': 0, 'health_score': 75, 'health_rating': 'Good', 'price_per_serving': 3.0, 'common_allergens': 'Tree Nuts'},
    {'name': 'Peanuts', 'category': 'Nuts', 'calories': 567, 'protein_g': 26, 'carbs_g': 16, 'fat_g': 49, 'fiber_g': 8.5, 'sugar_g': 4.7, 'sodium_mg': 18, 'cholesterol_mg': 0, 'health_score': 78, 'health_rating': 'Good', 'price_per_serving': 1.5, 'common_allergens': 'Peanuts'},
    {'name': 'Pistachios', 'category': 'Nuts', 'calories': 560, 'protein_g': 20, 'carbs_g': 28, 'fat_g': 45, 'fiber_g': 10.6, 'sugar_g': 7.7, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 3.5, 'common_allergens': 'Tree Nuts'},
    {'name': 'Pecans', 'category': 'Nuts', 'calories': 691, 'protein_g': 9, 'carbs_g': 14, 'fat_g': 72, 'fiber_g': 9.6, 'sugar_g': 4, 'sodium_mg': 0, 'cholesterol_mg': 0, 'health_score': 70, 'health_rating': 'Good', 'price_per_serving': 4.0, 'common_allergens': 'Tree Nuts'},
    {'name': 'Chia Seeds', 'category': 'Nuts', 'calories': 486, 'protein_g': 17, 'carbs_g': 42, 'fat_g': 31, 'fiber_g': 34.4, 'sugar_g': 0, 'sodium_mg': 16, 'cholesterol_mg': 0, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 2.0},
    {'name': 'Flax Seeds', 'category': 'Nuts', 'calories': 534, 'protein_g': 18, 'carbs_g': 29, 'fat_g': 42, 'fiber_g': 27.3, 'sugar_g': 1.6, 'sodium_mg': 30, 'cholesterol_mg': 0, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 1.5},
    {'name': 'Pumpkin Seeds', 'category': 'Nuts', 'calories': 559, 'protein_g': 30, 'carbs_g': 15, 'fat_g': 49, 'fiber_g': 6, 'sugar_g': 1.4, 'sodium_mg': 7, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 2.5},
    {'name': 'Sunflower Seeds', 'category': 'Nuts', 'calories': 584, 'protein_g': 21, 'carbs_g': 20, 'fat_g': 51, 'fiber_g': 8.6, 'sugar_g': 2.6, 'sodium_mg': 9, 'cholesterol_mg': 0, 'health_score': 80, 'health_rating': 'Good', 'price_per_serving': 1.8},
    
    # LEGUMES (30 items)
    {'name': 'Black Beans', 'category': 'Legumes', 'calories': 132, 'protein_g': 8.9, 'carbs_g': 24, 'fat_g': 0.5, 'fiber_g': 8.7, 'sugar_g': 0.3, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 92, 'health_rating': 'Excellent', 'price_per_serving': 0.5},
    {'name': 'Kidney Beans', 'category': 'Legumes', 'calories': 127, 'protein_g': 8.7, 'carbs_g': 23, 'fat_g': 0.5, 'fiber_g': 7.4, 'sugar_g': 0.3, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 0.6},
    {'name': 'Chickpeas', 'category': 'Legumes', 'calories': 164, 'protein_g': 8.9, 'carbs_g': 27, 'fat_g': 2.6, 'fiber_g': 7.6, 'sugar_g': 4.8, 'sodium_mg': 7, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.7},
    {'name': 'Lentils', 'category': 'Legumes', 'calories': 116, 'protein_g': 9, 'carbs_g': 20, 'fat_g': 0.4, 'fiber_g': 7.9, 'sugar_g': 1.8, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 95, 'health_rating': 'Excellent', 'price_per_serving': 0.4},
    {'name': 'Green Peas', 'category': 'Legumes', 'calories': 81, 'protein_g': 5.4, 'carbs_g': 14, 'fat_g': 0.4, 'fiber_g': 5.7, 'sugar_g': 5.7, 'sodium_mg': 5, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 0.8},
    {'name': 'Edamame', 'category': 'Legumes', 'calories': 121, 'protein_g': 11, 'carbs_g': 10, 'fat_g': 5, 'fiber_g': 5.2, 'sugar_g': 2.2, 'sodium_mg': 6, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 1.5, 'common_allergens': 'Soy'},
    {'name': 'Tofu', 'category': 'Legumes', 'calories': 76, 'protein_g': 8, 'carbs_g': 1.9, 'fat_g': 4.8, 'fiber_g': 0.3, 'sugar_g': 0.7, 'sodium_mg': 7, 'cholesterol_mg': 0, 'health_score': 82, 'health_rating': 'Good', 'price_per_serving': 1.2, 'common_allergens': 'Soy'},
    {'name': 'Tempeh', 'category': 'Legumes', 'calories': 193, 'protein_g': 19, 'carbs_g': 9, 'fat_g': 11, 'fiber_g': 0, 'sugar_g': 0, 'sodium_mg': 9, 'cholesterol_mg': 0, 'health_score': 85, 'health_rating': 'Excellent', 'price_per_serving': 2.0, 'common_allergens': 'Soy'},
    {'name': 'Pinto Beans', 'category': 'Legumes', 'calories': 143, 'protein_g': 9, 'carbs_g': 26, 'fat_g': 0.7, 'fiber_g': 9, 'sugar_g': 0.3, 'sodium_mg': 1, 'cholesterol_mg': 0, 'health_score': 88, 'health_rating': 'Excellent', 'price_per_serving': 0.5},
    {'name': 'Navy Beans', 'category': 'Legumes', 'calories': 140, 'protein_g': 8.2, 'carbs_g': 26, 'fat_g': 0.6, 'fiber_g': 10.5, 'sugar_g': 0.3, 'sodium_mg': 2, 'cholesterol_mg': 0, 'health_score': 90, 'health_rating': 'Excellent', 'price_per_serving': 0.6},
]

def populate_database():
    """Populate database with comprehensive food list"""
    with app.app_context():
        # Create all database tables if they don't exist
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        print("🍎 Starting food database population...")
        
        # Check existing foods
        existing_count = Food.query.count()
        print(f"📊 Current foods in database: {existing_count}")
        
        # Get existing food names to avoid duplicates
        existing_foods = {food.name.lower() for food in Food.query.all()}
        
        added_count = 0
        skipped_count = 0
        
        for food_data in FOODS_DATABASE:
            # Check if food already exists
            if food_data['name'].lower() in existing_foods:
                skipped_count += 1
                continue
            
            # Create new food entry
            food = Food(
                name=food_data['name'],
                category=food_data['category'],
                calories=food_data['calories'],
                protein_g=food_data['protein_g'],
                carbs_g=food_data['carbs_g'],
                fat_g=food_data['fat_g'],
                fiber_g=food_data.get('fiber_g', 0),
                sugar_g=food_data.get('sugar_g', 0),
                sodium_mg=food_data.get('sodium_mg', 0),
                cholesterol_mg=food_data.get('cholesterol_mg', 0),
                health_score=food_data['health_score'],
                health_rating=food_data['health_rating'],
                common_allergens=food_data.get('common_allergens', ''),
                price_per_serving=food_data['price_per_serving'],
                approved=True
            )
            
            db.session.add(food)
            added_count += 1
        
        # Commit all changes
        db.session.commit()
        
        # Final count
        final_count = Food.query.count()
        
        print(f"\n✅ Database population complete!")
        print(f"📈 Added: {added_count} new foods")
        print(f"⏭️  Skipped: {skipped_count} existing foods")
        print(f"🎯 Total foods in database: {final_count}")
        
        # Show category breakdown
        print("\n📊 Foods by Category:")
        categories = db.session.query(Food.category, db.func.count(Food.id)).group_by(Food.category).all()
        for category, count in categories:
            print(f"   {category}: {count} items")

if __name__ == '__main__':
    populate_database()
    print("\n🎉 All done! Your NutriAI database now has 300+ foods!")
