"""
Test Supabase Database Connection
"""
import psycopg2
import sys

# Connection strings to test
connections = [
    {
        'name': 'Connection Pooler (Recommended)',
        'url': 'postgresql://postgres.mvpugxwlufztwqunjysf:olawanle@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
    },
    {
        'name': 'Direct Connection',
        'url': 'postgresql://postgres:olawanle@db.mvpugxwlufztwqunjysf.supabase.co:5432/postgres'
    }
]

print("\n" + "="*60)
print("Testing Supabase Database Connections")
print("="*60 + "\n")

for conn_info in connections:
    print(f"Testing: {conn_info['name']}")
    print(f"URL: {conn_info['url'][:50]}...")
    
    try:
        # Try to connect
        conn = psycopg2.connect(conn_info['url'], connect_timeout=10, sslmode='require')
        cursor = conn.cursor()
        
        # Test query
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        print(f"✓ Connection successful!")
        print(f"  PostgreSQL version: {version[0][:50]}...")
        
        cursor.close()
        conn.close()
        
        print(f"\n✓ This connection works! Use this URL.\n")
        print("="*60 + "\n")
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Connection failed: {str(e)[:100]}")
        print()

print("="*60)
print("✗ All connection attempts failed")
print("\nTroubleshooting:")
print("1. Verify your Supabase project is active")
print("2. Check the password is correct")
print("3. Ensure your IP is not blocked")
print("4. Try accessing Supabase dashboard to confirm project status")
print("="*60 + "\n")
sys.exit(1)
