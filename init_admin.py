"""
Initialize admin user for NutriAI
Creates an admin account with username 'admin' and password 'admin123'
"""
from app_new import app, db
from models import User, Food

def init_admin():
    with app.app_context():
        # Create all database tables if they don't exist
        print("🗄️  Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("✓ Admin user already exists")
            print(f"  Username: {admin.username}")
            print(f"  Email: {admin.email}")
            print(f"  Is Admin: {admin.is_admin}")
            
            # Update password to known value
            admin.set_password('admin123')
            admin.is_admin = True
            admin.is_active = True
            db.session.commit()
            print("✓ Admin password updated to 'admin123'")
        else:
            # Create new admin user
            admin = User(
                username='admin',
                email='admin@nutriai.com',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created successfully!")
            print(f"  Username: admin")
            print(f"  Password: admin123")
            print(f"  Email: admin@nutriai.com")
        
        # Check if we have foods in database
        food_count = Food.query.count()
        print(f"\n✓ Database has {food_count} foods")
        
        if food_count == 0:
            print("\n⚠️  Warning: No foods in database. The system won't function properly.")
            print("   Please add foods to the database or run seed script.")
        
        print("\n" + "="*50)
        print("Admin Login Information:")
        print("="*50)
        print("URL: http://127.0.0.1:5000/login")
        print("Username: admin")
        print("Password: admin123")
        print("="*50)
        print("\nAfter logging in, you can access:")
        print("- Dashboard: http://127.0.0.1:5000/dashboard")
        print("- Admin Panel: http://127.0.0.1:5000/admin")
        print("="*50)

if __name__ == '__main__':
    init_admin()
