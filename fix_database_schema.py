"""
Fix Database Schema - Ensure tables match SQLAlchemy models exactly
"""

import sys
from sqlalchemy import create_engine, text, inspect

# Supabase connection
SUPABASE_URL = 'postgresql://postgres.mvpugxwlufztwqunjysf:olawanle@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_tables():
    """Check existing tables"""
    print_header("🔍 Checking Existing Tables")
    
    try:
        engine = create_engine(SUPABASE_URL)
        inspector = inspect(engine)
        
        tables = inspector.get_table_names()
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  • {table}")
            columns = inspector.get_columns(table)
            print(f"    Columns: {len(columns)}")
            for col in columns:
                print(f"      - {col['name']} ({col['type']})")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def drop_and_recreate():
    """Drop all tables and recreate using SQLAlchemy"""
    print_header("🔄 Recreating Tables with SQLAlchemy")
    
    try:
        # Import after setting environment
        import os
        os.environ['DATABASE_URL'] = SUPABASE_URL
        
        from main import app, db
        
        with app.app_context():
            print("⚠️  Dropping all existing tables...")
            db.drop_all()
            print("✓ Tables dropped")
            
            print("\n📊 Creating tables with SQLAlchemy...")
            db.create_all()
            print("✓ Tables created")
            
            # Verify tables
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n✓ Created {len(tables)} tables:")
            for table in tables:
                print(f"  • {table}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_users():
    """Create admin and test users"""
    print_header("👥 Creating Users")
    
    try:
        import os
        os.environ['DATABASE_URL'] = SUPABASE_URL
        
        from main import app, db, User, Transaction, generate_wallet_address
        
        with app.app_context():
            # Create admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@timebank.com',
                    wallet_address=generate_wallet_address(),
                    is_admin=True,
                    token_balance=1000.0,
                    reputation_score=10.0
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                
                # Create transaction
                tx = Transaction(
                    to_user_id=admin.id,
                    amount=1000.0,
                    transaction_type='bonus',
                    description='Admin initialization'
                )
                db.session.add(tx)
                db.session.commit()
                
                print(f"✓ Admin created: admin / admin123")
            else:
                print("⚠️  Admin already exists")
            
            # Create test user
            test = User.query.filter_by(username='testuser').first()
            if not test:
                test = User(
                    username='testuser',
                    email='test@timebank.com',
                    wallet_address=generate_wallet_address(),
                    is_admin=False,
                    token_balance=50.0,
                    reputation_score=5.0
                )
                test.set_password('test123')
                db.session.add(test)
                db.session.commit()
                
                # Create transaction
                tx = Transaction(
                    to_user_id=test.id,
                    amount=50.0,
                    transaction_type='bonus',
                    description='Test user initialization'
                )
                db.session.add(tx)
                db.session.commit()
                
                print(f"✓ Test user created: testuser / test123")
            else:
                print("⚠️  Test user already exists")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*20 + "Fix Database Schema" + " "*27 + "║")
    print("╚" + "="*68 + "╝")
    
    # Check existing tables
    check_tables()
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will drop all existing tables and recreate them!")
    print("   All data will be lost.")
    response = input("\nContinue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("\n❌ Aborted")
        sys.exit(0)
    
    # Drop and recreate
    if not drop_and_recreate():
        print("\n❌ Failed to recreate tables")
        sys.exit(1)
    
    # Create users
    if not create_users():
        print("\n❌ Failed to create users")
        sys.exit(1)
    
    print_header("✅ SUCCESS! Database Fixed")
    print("✓ Tables recreated with correct schema")
    print("✓ Users created")
    print("\n🔐 Login Credentials:")
    print("  Admin: admin / admin123")
    print("  Test: testuser / test123")
    print("\n🚀 Your app should work now!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
