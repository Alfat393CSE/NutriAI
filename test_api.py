"""
Test the dashboard API to verify it returns target values
"""
import requests

# Test the dashboard stats endpoint
try:
    # You'll need to be logged in to test this
    # This is just to show what the API should return
    print("Testing /api/dashboard/stats endpoint")
    print("\nExpected response structure:")
    print({
        'today': {
            'calories': 0,
            'protein': 0,
            'carbs': 0,
            'fat': 0,
            'target_calories': 3000,
            'target_protein': 200,
            'target_carbs': 120,
            'target_fat': 60,
            'meals_logged': 0
        }
    })
    
    print("\nTo verify the API is working:")
    print("1. Open browser DevTools (F12)")
    print("2. Go to Network tab")
    print("3. Refresh the dashboard page")
    print("4. Look for the '/api/dashboard/stats' request")
    print("5. Check the Response tab to see if target values are included")
    
except Exception as e:
    print(f"Error: {e}")
