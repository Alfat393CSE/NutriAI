from app_new import app, db, Food, User
import sys

with app.app_context():
    # Check foods
    foods = Food.query.all()
    print(f"\n📊 Database Status:")
    print(f"=" * 50)
    print(f"Total foods in database: {len(foods)}")
    
    if len(foods) > 0:
        print(f"\nFirst 5 foods:")
        for f in foods[:5]:
            print(f"  - {f.name} ({f.category})")
            print(f"    Calories: {f.calories}, Protein: {f.protein_g}g")
    else:
        print("\n❌ No foods in database!")
        print("Run: python populate_foods.py")
    
    # Check users
    users = User.query.all()
    print(f"\nTotal users: {len(users)}")
    if len(users) > 0:
        for u in users[:3]:
            print(f"  - {u.username} (Age: {u.age}, Goal: {u.diet_goal})")
    
    print(f"\n" + "=" * 50)
