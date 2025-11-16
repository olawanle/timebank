"""
TimeBank - Supabase Database Setup Script
Forces Supabase connection, creates tables, and sets up users
"""

import sys
import os
import psycopg2
from sqlalchemy import create_engine, text

# Force Supabase connection
SUPABASE_URL = 'postgresql://postgres.mvpugxwlufztwqunjysf:olawanle@aws-1-eu-west-1.pooler.supabase.com:5432/postgres'

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def verify_connection():
    """Verify database connection"""
    print_header("🔍 STEP 1: Verifying Supabase Connection")
    
    try:
        print(f"📡 Connecting to Supabase EU West 1...")
        print(f"   Host: aws-1-eu-west-1.pooler.supabase.com")
        print(f"   Port: 5432 (Session Pooler - IPv4)")
        
        # Test connection
        conn = psycopg2.connect(SUPABASE_URL, connect_timeout=10, sslmode='require')
        cursor = conn.cursor()
        
        # Get database info
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        
        cursor.execute('SELECT current_database(), current_user;')
        db_info = cursor.fetchone()
        
        print(f"\n✓ Connection successful!")
        print(f"  Database: {db_info[0]}")
        print(f"  User: {db_info[1]}")
        print(f"  PostgreSQL: {version[:60]}...")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n✗ Connection failed: {e}")
        print("\n⚠️  Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify Supabase project is active")
        print("3. Confirm password is correct: olawanle")
        print("4. Check Supabase dashboard for project status")
        return False

def create_tables():
    """Create all database tables"""
    print_header("📊 STEP 2: Creating Database Tables")
    
    try:
        engine = create_engine(SUPABASE_URL)
        
        with engine.connect() as conn:
            # Create users table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(200) NOT NULL,
                    wallet_address VARCHAR(42) UNIQUE NOT NULL,
                    token_balance FLOAT DEFAULT 10.0,
                    hours_earned FLOAT DEFAULT 0.0,
                    hours_spent FLOAT DEFAULT 0.0,
                    reputation_score FLOAT DEFAULT 5.0,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Create service table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS service (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    duration FLOAT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    service_type VARCHAR(20) NOT NULL,
                    provider_id INTEGER REFERENCES "user"(id),
                    requester_id INTEGER REFERENCES "user"(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP
                );
            """))
            
            # Create transaction table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS transaction (
                    id SERIAL PRIMARY KEY,
                    from_user_id INTEGER REFERENCES "user"(id),
                    to_user_id INTEGER REFERENCES "user"(id),
                    amount FLOAT NOT NULL,
                    transaction_type VARCHAR(50) NOT NULL,
                    service_id INTEGER REFERENCES service(id),
                    description VARCHAR(200) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Create proposal table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS proposal (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    proposer_id INTEGER REFERENCES "user"(id) NOT NULL,
                    status VARCHAR(20) DEFAULT 'active',
                    votes_for INTEGER DEFAULT 0,
                    votes_against INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ends_at TIMESTAMP NOT NULL
                );
            """))
            
            # Create vote table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS vote (
                    id SERIAL PRIMARY KEY,
                    proposal_id INTEGER REFERENCES proposal(id) NOT NULL,
                    voter_id INTEGER REFERENCES "user"(id) NOT NULL,
                    vote_type VARCHAR(10) NOT NULL,
                    voting_power FLOAT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            conn.commit()
        
        print("✓ Tables created successfully:")
        print("  • user - User accounts with wallets")
        print("  • service - Service exchange records")
        print("  • transaction - Token transfer history")
        print("  • proposal - DAO governance proposals")
        print("  • vote - Voting records")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

def create_users():
    """Create admin and test users"""
    print_header("👥 STEP 3: Creating Users")
    
    try:
        from werkzeug.security import generate_password_hash
        import secrets
        
        engine = create_engine(SUPABASE_URL)
        
        with engine.connect() as conn:
            # Generate wallet addresses
            admin_wallet = '0x' + secrets.token_hex(20)
            test_wallet = '0x' + secrets.token_hex(20)
            
            # Hash passwords
            admin_password = generate_password_hash('admin123')
            test_password = generate_password_hash('test123')
            
            # Check if admin exists
            result = conn.execute(text("SELECT id FROM \"user\" WHERE username = 'admin'"))
            admin_exists = result.fetchone()
            
            if not admin_exists:
                # Create admin user
                conn.execute(text("""
                    INSERT INTO "user" (username, email, password_hash, wallet_address, 
                                       token_balance, reputation_score, is_admin)
                    VALUES (:username, :email, :password, :wallet, :balance, :reputation, :is_admin)
                """), {
                    'username': 'admin',
                    'email': 'admin@timebank.com',
                    'password': admin_password,
                    'wallet': admin_wallet,
                    'balance': 1000.0,
                    'reputation': 10.0,
                    'is_admin': True
                })
                
                # Get admin ID
                result = conn.execute(text("SELECT id FROM \"user\" WHERE username = 'admin'"))
                admin_id = result.fetchone()[0]
                
                # Create welcome transaction
                conn.execute(text("""
                    INSERT INTO transaction (to_user_id, amount, transaction_type, description)
                    VALUES (:user_id, :amount, :type, :description)
                """), {
                    'user_id': admin_id,
                    'amount': 1000.0,
                    'type': 'bonus',
                    'description': 'Admin account initialization - 1000 tokens'
                })
                
                print("✓ Admin user created!")
                print(f"  Username: admin")
                print(f"  Password: admin123")
                print(f"  Wallet: {admin_wallet}")
                print(f"  Balance: 1000 tokens")
            else:
                print("⚠️  Admin user already exists")
            
            # Check if test user exists
            result = conn.execute(text("SELECT id FROM \"user\" WHERE username = 'testuser'"))
            test_exists = result.fetchone()
            
            if not test_exists:
                # Create test user
                conn.execute(text("""
                    INSERT INTO "user" (username, email, password_hash, wallet_address, 
                                       token_balance, reputation_score, is_admin)
                    VALUES (:username, :email, :password, :wallet, :balance, :reputation, :is_admin)
                """), {
                    'username': 'testuser',
                    'email': 'test@timebank.com',
                    'password': test_password,
                    'wallet': test_wallet,
                    'balance': 50.0,
                    'reputation': 5.0,
                    'is_admin': False
                })
                
                # Get test user ID
                result = conn.execute(text("SELECT id FROM \"user\" WHERE username = 'testuser'"))
                test_id = result.fetchone()[0]
                
                # Create welcome transaction
                conn.execute(text("""
                    INSERT INTO transaction (to_user_id, amount, transaction_type, description)
                    VALUES (:user_id, :amount, :type, :description)
                """), {
                    'user_id': test_id,
                    'amount': 50.0,
                    'type': 'bonus',
                    'description': 'Test account initialization - 50 tokens'
                })
                
                print("\n✓ Test user created!")
                print(f"  Username: testuser")
                print(f"  Password: test123")
                print(f"  Wallet: {test_wallet}")
                print(f"  Balance: 50 tokens")
            else:
                print("\n⚠️  Test user already exists")
            
            conn.commit()
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating users: {e}")
        return False

def verify_setup():
    """Verify the setup"""
    print_header("✅ STEP 4: Verifying Setup")
    
    try:
        engine = create_engine(SUPABASE_URL)
        
        with engine.connect() as conn:
            # Count records
            result = conn.execute(text('SELECT COUNT(*) FROM "user"'))
            user_count = result.fetchone()[0]
            
            result = conn.execute(text('SELECT COUNT(*) FROM service'))
            service_count = result.fetchone()[0]
            
            result = conn.execute(text('SELECT COUNT(*) FROM transaction'))
            transaction_count = result.fetchone()[0]
            
            print("📊 Database Statistics:")
            print(f"  Users: {user_count}")
            print(f"  Services: {service_count}")
            print(f"  Transactions: {transaction_count}")
            
            # List users
            print("\n👥 Users:")
            result = conn.execute(text('SELECT username, token_balance, is_admin FROM "user"'))
            for row in result:
                role = "Admin" if row[2] else "User"
                print(f"  • {row[0]} ({role}) - {row[1]} tokens")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verifying setup: {e}")
        return False

def main():
    """Main setup function"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "TimeBank Supabase Database Setup" + " "*20 + "║")
    print("╚" + "="*68 + "╝")
    
    # Step 1: Verify connection
    if not verify_connection():
        print("\n❌ Setup failed: Cannot connect to Supabase")
        print("\n💡 Make sure:")
        print("  • Your internet connection is working")
        print("  • Supabase project is active")
        print("  • Password is correct: olawanle")
        sys.exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        print("\n❌ Setup failed: Cannot create tables")
        sys.exit(1)
    
    # Step 3: Create users
    if not create_users():
        print("\n❌ Setup failed: Cannot create users")
        sys.exit(1)
    
    # Step 4: Verify setup
    if not verify_setup():
        print("\n⚠️  Warning: Could not verify setup (non-critical)")
    
    # Success!
    print_header("🎉 SUCCESS! Supabase Database Setup Complete")
    
    print("✅ Your TimeBank database is ready on Supabase!")
    print("\n🔐 Login Credentials:")
    print("\n  Admin Account:")
    print("    Username: admin")
    print("    Password: admin123")
    print("    Balance: 1000 tokens")
    print("    Role: Administrator")
    print("\n  Test Account:")
    print("    Username: testuser")
    print("    Password: test123")
    print("    Balance: 50 tokens")
    print("    Role: Regular User")
    
    print("\n🚀 Next Steps:")
    print("  1. Deploy to Render (will use this database)")
    print("  2. Or set DATABASE_URL environment variable locally")
    print("  3. Run: python run.py")
    print("  4. Login and start using TimeBank!")
    
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()
