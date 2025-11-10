"""
Simple runner script for TimeBank application
"""
import sys
import traceback

try:
    from main import app, init_db
    
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
    
    print("\n" + "="*60)
    print("TimeBank - Crypto-Powered Time Banking System")
    print("="*60)
    print("\nServer starting on http://localhost:5000")
    print("\nDemo Account:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"\nError starting application: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
