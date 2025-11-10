"""
Initialize Supabase Database for TimeBank
Run this script to set up tables and create admin user
"""

from main import app, db, User, generate_wallet_address
import sys

def initialize_database():
    """Initialize database with tables and admin user"""
    print("\n" + "="*60)
    print("TimeBank - Supabase Database Initialization")
    print("="*60 + "\n")
    
    with app.app_context():
        try:
            # Test database connection
            print("📡 Testing database connection...")
            db.engine.connect()
            print("✓ Connected to Supabase PostgreSQL\n")
            
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✓ Tables created successfully:")
            print("  • users")
            print("  • services")
            print("  • transactions")
            print("  • proposals")
            print("  • votes\n")
            
            # Create admin user
            print("👤 Creating admin user...")
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("⚠ Admin user already exists")
                print(f"  Username: admin")
                print(f"  Email: {admin.email}")
                print(f"  Wallet: {admin.wallet_address}")
                print(f"  Balance: {admin.token_balance} tokens")
            else:
                admin = User(
                    username='admin',
                    email='admin@timebank.com',
                    wallet_address=generate_wallet_address(),
                    is_admin=True,
                    token_balance=1000.0
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                
                print("✓ Admin user created successfully!")
                print(f"  Username: admin")
                print(f"  Password: admin123")
                print(f"  Email: {admin.email}")
                print(f"  Wallet: {admin.wallet_address}")
                print(f"  Balance: {admin.token_balance} tokens")
            
            print("\n" + "="*60)
            print("✓ Database initialization complete!")
            print("="*60 + "\n")
            
            print("🚀 You can now run the application:")
            print("   python run.py")
            print("\n   or")
            print("\n   gunicorn main:app\n")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("\nTroubleshooting:")
            print("1. Check your database URL is correct")
            print("2. Verify Supabase database is accessible")
            print("3. Ensure psycopg2-binary is installed")
            print("4. Check your internet connection\n")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = initialize_database()
    sys.exit(0 if success else 1)
