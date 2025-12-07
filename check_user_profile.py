"""
Check user profile data in the database
"""
import sqlite3
import os

def check_profile():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'nutriai.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all users
        cursor.execute("SELECT id, username, daily_caloric_intake, protein_goal, carbs_goal, fat_goal FROM users")
        users = cursor.fetchall()
        
        print("User Profile Data:")
        print("-" * 80)
        for user in users:
            user_id, username, calories, protein, carbs, fat = user
            print(f"User: {username} (ID: {user_id})")
            print(f"  Daily Caloric Intake: {calories}")
            print(f"  Protein Goal: {protein}g")
            print(f"  Carbs Goal: {carbs}g")
            print(f"  Fat Goal: {fat}g")
            print("-" * 80)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    check_profile()
