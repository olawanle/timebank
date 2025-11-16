"""
TimeBank - Complete Database Setup Script
Verifies connection, creates tables, and sets up users
"""

import sys
import psycopg2
from main import app, db, User, Service, Transaction, Proposal, Vote, generate_wallet_address

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def verify_connection():
    """Verify database connection"""
    print_header("🔍 STEP 1: Verifying Database Connection")
    
    try:
        # Get database URL from app config
        db_url = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"📡 Connecting to: {db_url[:50]}...")
        
        # Test connection with psycopg2
        conn = psycopg2.connect(db_url, connect_timeout=10, sslmode='require')
        cursor = conn.cursor()
        
        # Get database info
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        cursor.execute('SELECT current_database(), current_user;')
        db_info = cursor.fetchone()
        
        print(f"✓ Connection successful!")
        print(f"  Database: {db_info[0]}")
        print(f"  User: {db_info[1]}")
        print(f"  PostgreSQL: {version[:60]}...")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("\n⚠️  Troubleshooting:")
        print("1. Check your database URL is correct")
        print("2. Verify Supabase project is active")
        print("3. Ensure you're using Session Pooler (IPv4 compatible)")
        print("4. Check your internet connection")
        return False

def create_tables():
    """Create all database tables"""
    print_header("📊 STEP 2: Creating Database Tables")
    
    try:
        with app.app_context():
            # Drop all tables (optional - comment out if you want to keep existing data)
            # db.drop_all()
            # print("⚠️  Dropped existing tables")
            
            # Create all tables
            db.create_all()
            
            print("✓ Tables created successfully:")
            print("  • users - User accounts with wallets")
            print("  • services - Service exchange records")
            print("  • transactions - Token transfer history")
            print("  • proposals - DAO governance proposals")
            print("  • votes - Voting records")
            
            return True
            
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create admin user"""
    print_header("👤 STEP 3: Creating Admin User")
    
    try:
        with app.app_context():
            # Check if admin exists
            admin = User.query.filter_by(username='admin').first()
            
            if admin:
                print("⚠️  Admin user already exists")
                print(f"  Username: {admin.username}")
                print(f"  Email: {admin.email}")
                print(f"  Wallet: {admin.wallet_address}")
                print(f"  Balance: {admin.token_balance} tokens")
                print(f"  Reputation: {admin.reputation_score}")
                return True
            
            # Create admin user
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
            
            # Create welcome transaction
            welcome_tx = Transaction(
                from_user_id=None,
                to_user_id=admin.id,
                amount=1000.0,
                transaction_type='bonus',
                description='Admin account initialization - 1000 tokens'
            )
            db.session.add(welcome_tx)
            db.session.commit()
            
            print("✓ Admin user created successfully!")
            print(f"  Username: admin")
            print(f"  Password: admin123")
            print(f"  Email: {admin.email}")
            print(f"  Wallet: {admin.wallet_address}")
            print(f"  Balance: {admin.token_balance} tokens")
            print(f"  Role: Administrator")
            
            return True
            
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.session.rollback()
        return False

def create_test_user():
    """Create test user"""
    print_header("👥 STEP 4: Creating Test User")
    
    try:
        with app.app_context():
            # Check if test user exists
            test_user = User.query.filter_by(username='testuser').first()
            
            if test_user:
                print("⚠️  Test user already exists")
                print(f"  Username: {test_user.username}")
                print(f"  Email: {test_user.email}")
                print(f"  Wallet: {test_user.wallet_address}")
                print(f"  Balance: {test_user.token_balance} tokens")
                return True
            
            # Create test user
            test_user = User(
                username='testuser',
                email='test@timebank.com',
                wallet_address=generate_wallet_address(),
                is_admin=False,
                token_balance=50.0,
                reputation_score=5.0
            )
            test_user.set_password('test123')
            
            db.session.add(test_user)
            db.session.commit()
            
            # Create welcome transaction
            welcome_tx = Transaction(
                from_user_id=None,
                to_user_id=test_user.id,
                amount=50.0,
                transaction_type='bonus',
                description='Test account initialization - 50 tokens'
            )
            db.session.add(welcome_tx)
            db.session.commit()
            
            print("✓ Test user created successfully!")
            print(f"  Username: testuser")
            print(f"  Password: test123")
            print(f"  Email: {test_user.email}")
            print(f"  Wallet: {test_user.wallet_address}")
            print(f"  Balance: {test_user.token_balance} tokens")
            print(f"  Role: Regular User")
            
            return True
            
    except Exception as e:
        print(f"✗ Error creating test user: {e}")
        db.session.rollback()
        return False

def create_sample_data():
    """Create sample service and proposal"""
    print_header("📝 STEP 5: Creating Sample Data")
    
    try:
        with app.app_context():
            admin = User.query.filter_by(username='admin').first()
            test_user = User.query.filter_by(username='testuser').first()
            
            if not admin or not test_user:
                print("⚠️  Users not found, skipping sample data")
                return True
            
            # Check if sample data exists
            existing_service = Service.query.first()
            if existing_service:
                print("⚠️  Sample data already exists, skipping")
                return True
            
            # Create a sample service request
            service = Service(
                title='Need help with Python programming',
                description='Looking for someone to help me learn Python basics',
                category='tutoring',
                duration=2.0,
                service_type='request',
                requester_id=test_user.id,
                status='pending'
            )
            db.session.add(service)
            
            # Create a sample proposal
            from datetime import datetime, timedelta
            proposal = Proposal(
                title='Increase welcome bonus to 20 tokens',
                description='I propose we increase the welcome bonus from 10 to 20 tokens to attract more users.',
                proposer_id=admin.id,
                status='active',
                ends_at=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(proposal)
            
            db.session.commit()
            
            print("✓ Sample data created successfully!")
            print("  • Sample service request (2 hours)")
            print("  • Sample governance proposal")
            
            return True
            
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        db.session.rollback()
        return False

def verify_setup():
    """Verify the setup"""
    print_header("✅ STEP 6: Verifying Setup")
    
    try:
        with app.app_context():
            # Count records
            user_count = User.query.count()
            service_count = Service.query.count()
            transaction_count = Transaction.query.count()
            proposal_count = Proposal.query.count()
            
            print("📊 Database Statistics:")
            print(f"  Users: {user_count}")
            print(f"  Services: {service_count}")
            print(f"  Transactions: {transaction_count}")
            print(f"  Proposals: {proposal_count}")
            
            # List users
            print("\n👥 Users:")
            users = User.query.all()
            for user in users:
                role = "Admin" if user.is_admin else "User"
                print(f"  • {user.username} ({role}) - {user.token_balance} tokens")
            
            return True
            
    except Exception as e:
        print(f"✗ Error verifying setup: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*20 + "TimeBank Database Setup" + " "*25 + "║")
    print("╚" + "="*68 + "╝")
    
    # Step 1: Verify connection
    if not verify_connection():
        print("\n❌ Setup failed: Cannot connect to database")
        sys.exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        print("\n❌ Setup failed: Cannot create tables")
        sys.exit(1)
    
    # Step 3: Create admin user
    if not create_admin_user():
        print("\n❌ Setup failed: Cannot create admin user")
        sys.exit(1)
    
    # Step 4: Create test user
    if not create_test_user():
        print("\n❌ Setup failed: Cannot create test user")
        sys.exit(1)
    
    # Step 5: Create sample data
    if not create_sample_data():
        print("\n⚠️  Warning: Could not create sample data (non-critical)")
    
    # Step 6: Verify setup
    if not verify_setup():
        print("\n⚠️  Warning: Could not verify setup (non-critical)")
    
    # Success!
    print_header("🎉 SUCCESS! Database Setup Complete")
    
    print("✅ Your TimeBank database is ready!")
    print("\n🔐 Login Credentials:")
    print("\n  Admin Account:")
    print("    Username: admin")
    print("    Password: admin123")
    print("    Balance: 1000 tokens")
    print("\n  Test Account:")
    print("    Username: testuser")
    print("    Password: test123")
    print("    Balance: 50 tokens")
    
    print("\n🚀 Next Steps:")
    print("  1. Run your application: python run.py")
    print("  2. Open: http://localhost:5000")
    print("  3. Login with admin or testuser")
    print("  4. Start using TimeBank!")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()
