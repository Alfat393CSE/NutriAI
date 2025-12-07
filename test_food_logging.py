"""
Test food logging to see what's happening
"""
import sqlite3
import os
from datetime import date

def test_logging():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'nutriai.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if foods exist
        cursor.execute("SELECT COUNT(*) FROM foods")
        food_count = cursor.fetchone()[0]
        print(f"Total foods in database: {food_count}")
        
        if food_count > 0:
            cursor.execute("SELECT id, name, calories, protein_g, carbs_g, fat_g FROM foods LIMIT 5")
            print("\nSample foods:")
            for food in cursor.fetchall():
                print(f"  {food}")
        
        # Check today's food logs for all users
        today = date.today()
        cursor.execute("""
            SELECT fl.id, u.username, f.name, fl.quantity_g, fl.calories_consumed, 
                   fl.protein_consumed, fl.carbs_consumed, fl.fat_consumed, fl.date
            FROM food_logs fl
            JOIN users u ON fl.user_id = u.id
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.date = ?
        """, (today,))
        
        logs = cursor.fetchall()
        print(f"\n\nToday's food logs ({today}): {len(logs)} entries")
        for log in logs:
            print(f"  {log}")
        
        # Check all recent logs
        cursor.execute("""
            SELECT fl.id, u.username, f.name, fl.quantity_g, fl.calories_consumed, fl.date
            FROM food_logs fl
            JOIN users u ON fl.user_id = u.id
            JOIN foods f ON fl.food_id = f.id
            ORDER BY fl.date DESC, fl.id DESC
            LIMIT 10
        """)
        
        recent_logs = cursor.fetchall()
        print(f"\n\nRecent food logs (last 10):")
        for log in recent_logs:
            print(f"  {log}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == '__main__':
    test_logging()
