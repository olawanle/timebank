"""
Find the correct Supabase connection string
This will try multiple connection formats
"""
import psycopg2
import sys

print("\n" + "="*70)
print("🔍 Finding Correct Supabase Connection String")
print("="*70 + "\n")

# Your Supabase project details
PROJECT_REF = "mvpugxwlufztwqunjysf"
PASSWORD = "olawanle"  # Your provided password

# Different connection string formats to try
connection_formats = [
    {
        'name': 'Transaction Mode (Port 6543)',
        'url': f'postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-us-east-1.pooler.supabase.com:6543/postgres',
        'params': {'sslmode': 'require'}
    },
    {
        'name': 'Session Mode (Port 5432)',
        'url': f'postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-us-east-1.pooler.supabase.com:5432/postgres',
        'params': {'sslmode': 'require'}
    },
    {
        'name': 'Direct Connection (Port 5432)',
        'url': f'postgresql://postgres:{PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres',
        'params': {'sslmode': 'require'}
    },
    {
        'name': 'Direct Connection with SSL Prefer',
        'url': f'postgresql://postgres:{PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres',
        'params': {'sslmode': 'prefer'}
    },
    {
        'name': 'IPv6 Connection',
        'url': f'postgresql://postgres:{PASSWORD}@db.{PROJECT_REF}.supabase.co:5432/postgres',
        'params': {'sslmode': 'require', 'connect_timeout': '30'}
    },
]

successful_connection = None

for i, conn_info in enumerate(connection_formats, 1):
    print(f"[{i}/{len(connection_formats)}] Testing: {conn_info['name']}")
    print(f"    URL: {conn_info['url'][:60]}...")
    
    try:
        # Try to connect
        conn = psycopg2.connect(
            conn_info['url'],
            **conn_info['params']
        )
        cursor = conn.cursor()
        
        # Test query
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        # Get database info
        cursor.execute('SELECT current_database(), current_user;')
        db_info = cursor.fetchone()
        
        print(f"    ✓ SUCCESS! Connection works!")
        print(f"    Database: {db_info[0]}")
        print(f"    User: {db_info[1]}")
        print(f"    PostgreSQL: {version[0][:60]}...")
        
        successful_connection = conn_info
        
        cursor.close()
        conn.close()
        
        print(f"\n{'='*70}")
        print("✓ FOUND WORKING CONNECTION!")
        print("="*70)
        print(f"\nConnection String:")
        print(f"{conn_info['url']}\n")
        print(f"SSL Mode: {conn_info['params'].get('sslmode', 'default')}\n")
        print("="*70 + "\n")
        
        # Save to file
        with open('WORKING_SUPABASE_URL.txt', 'w') as f:
            f.write("="*70 + "\n")
            f.write("WORKING SUPABASE CONNECTION STRING\n")
            f.write("="*70 + "\n\n")
            f.write(f"Connection Type: {conn_info['name']}\n\n")
            f.write(f"URL:\n{conn_info['url']}\n\n")
            f.write(f"SSL Mode: {conn_info['params'].get('sslmode', 'default')}\n\n")
            f.write("="*70 + "\n")
            f.write("Use this URL in:\n")
            f.write("1. main.py (SUPABASE_DB_URL variable)\n")
            f.write("2. render.yaml (DATABASE_URL value)\n")
            f.write("3. .env file (DATABASE_URL=...)\n")
            f.write("="*70 + "\n")
        
        print("✓ Connection string saved to: WORKING_SUPABASE_URL.txt\n")
        sys.exit(0)
        
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        if "password authentication failed" in error_msg:
            print(f"    ✗ Password incorrect")
        elif "could not translate host name" in error_msg:
            print(f"    ✗ Cannot resolve hostname (DNS issue)")
        elif "Connection refused" in error_msg:
            print(f"    ✗ Connection refused")
        elif "timeout" in error_msg:
            print(f"    ✗ Connection timeout")
        else:
            print(f"    ✗ Error: {error_msg[:80]}")
    except Exception as e:
        print(f"    ✗ Error: {str(e)[:80]}")
    
    print()

print("="*70)
print("✗ NO WORKING CONNECTION FOUND")
print("="*70)
print("\n⚠️  POSSIBLE ISSUES:\n")
print("1. Password is incorrect")
print("   → Go to Supabase Dashboard → Settings → Database")
print("   → Reset your database password")
print("   → Update the PASSWORD variable in this script\n")
print("2. Project is paused or inactive")
print("   → Check Supabase dashboard")
print("   → Ensure project is active\n")
print("3. Network/Firewall blocking connection")
print("   → Check your internet connection")
print("   → Try from a different network\n")
print("4. Project reference might be wrong")
print("   → Verify project ref: mvpugxwlufztwqunjysf")
print("   → Check in Supabase dashboard URL\n")
print("="*70)
print("\n📖 Next Steps:")
print("1. Go to: https://app.supabase.com/project/mvpugxwlufztwqunjysf")
print("2. Settings → Database → Reset password")
print("3. Update PASSWORD in this script")
print("4. Run again: python find_supabase_connection.py\n")
print("="*70 + "\n")

sys.exit(1)
