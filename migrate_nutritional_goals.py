"""
Migration script to add nutritional goal columns to users table
"""
import sqlite3
import os

def migrate_database():
    # Get the database path
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'nutriai.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add protein_goal column if it doesn't exist
        if 'protein_goal' not in columns:
            print("Adding protein_goal column...")
            cursor.execute("ALTER TABLE users ADD COLUMN protein_goal INTEGER")
            print("✓ protein_goal column added")
        else:
            print("protein_goal column already exists")
        
        # Add carbs_goal column if it doesn't exist
        if 'carbs_goal' not in columns:
            print("Adding carbs_goal column...")
            cursor.execute("ALTER TABLE users ADD COLUMN carbs_goal INTEGER")
            print("✓ carbs_goal column added")
        else:
            print("carbs_goal column already exists")
        
        # Add fat_goal column if it doesn't exist
        if 'fat_goal' not in columns:
            print("Adding fat_goal column...")
            cursor.execute("ALTER TABLE users ADD COLUMN fat_goal INTEGER")
            print("✓ fat_goal column added")
        else:
            print("fat_goal column already exists")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
