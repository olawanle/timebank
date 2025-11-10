# 🗄️ Supabase Database Setup for TimeBank

## ✅ Database Configuration Complete!

Your TimeBank is now configured to use Supabase PostgreSQL database.

**Database URL:**
```
postgresql://postgres:olawanle@db.mvpugxwlufztwqunjysf.supabase.co:5432/postgres
```

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask and extensions
- SQLAlchemy (ORM)
- psycopg2-binary (PostgreSQL adapter)
- gunicorn (production server)

### Step 2: Initialize Database

Run the initialization script:

```bash
python init_supabase_db.py
```

This will:
- ✓ Test connection to Supabase
- ✓ Create all database tables
- ✓ Create admin user (username: admin, password: admin123)

### Step 3: Run the Application

**Development:**
```bash
python run.py
```

**Production:**
```bash
gunicorn main:app
```

## 📊 Database Tables

The following tables will be created:

### 1. users
- User accounts with wallet addresses
- Token balances and reputation scores
- Admin privileges

### 2. services
- Service exchange records
- Offer and request types
- Status tracking

### 3. transactions
- Token transfer history
- Transaction types and descriptions
- Linked to services

### 4. proposals
- DAO governance proposals
- Voting status and results
- Time-based expiration

### 5. votes
- Voting records
- Token-weighted voting power
- One vote per user per proposal

## 🔐 Admin User

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@timebank.com`
- Balance: 1000 tokens
- Role: Administrator

**⚠️ Important:** Change the admin password after first login!

## 🌐 Supabase Dashboard

Access your database at:
https://app.supabase.com/project/mvpugxwlufztwqunjysf

From the dashboard you can:
- View tables and data
- Run SQL queries
- Monitor performance
- Set up backups
- Configure security

## 🔧 Configuration

### Environment Variables

For local development, create a `.env` file:

```bash
DATABASE_URL=postgresql://postgres:olawanle@db.mvpugxwlufztwqunjysf.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
DEBUG=False
PORT=5000
```

### For Render Deployment

Add these environment variables in Render dashboard:

```
DATABASE_URL = postgresql://postgres:olawanle@db.mvpugxwlufztwqunjysf.supabase.co:5432/postgres
SECRET_KEY = (generate a secure key)
```

## 🔍 Verify Setup

### Check Database Connection

```python
python -c "from main import db, app; app.app_context().push(); print('Connected!' if db.engine.connect() else 'Failed')"
```

### Check Admin User

```python
python -c "from main import User, app; app.app_context().push(); admin = User.query.filter_by(username='admin').first(); print(f'Admin exists: {admin is not None}')"
```

### View All Users

```python
python -c "from main import User, app; app.app_context().push(); users = User.query.all(); print(f'Total users: {len(users)}')"
```

## 🛠️ Troubleshooting

### Connection Error

**Problem:** Can't connect to Supabase database

**Solutions:**
1. Check your internet connection
2. Verify the database URL is correct
3. Ensure Supabase project is active
4. Check if IP is whitelisted (Supabase allows all by default)

### psycopg2 Error

**Problem:** `psycopg2` module not found

**Solution:**
```bash
pip install psycopg2-binary
```

### Table Already Exists

**Problem:** Tables already exist error

**Solution:**
This is normal if you've run the initialization before. The app will use existing tables.

### Admin User Already Exists

**Problem:** Admin user creation fails

**Solution:**
This is normal if admin was created before. You can login with existing credentials.

## 🔄 Database Migrations

For schema changes, you can use Flask-Migrate:

```bash
pip install Flask-Migrate
```

Then in your code:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

Run migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📈 Performance Tips

### Connection Pooling

Already configured in `main.py`:
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### Indexes

For better performance, add indexes in Supabase dashboard:

```sql
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_services_status ON services(status);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp);
```

## 🔐 Security Best Practices

1. **Change Admin Password**
   - Login and change from default `admin123`

2. **Use Environment Variables**
   - Never commit database credentials to Git
   - Use `.env` file for local development

3. **Enable Row Level Security (RLS)**
   - Configure in Supabase dashboard
   - Restrict access to sensitive data

4. **Regular Backups**
   - Supabase provides automatic backups
   - Download manual backups periodically

## 📊 Monitoring

### Supabase Dashboard

Monitor your database:
- Query performance
- Connection count
- Storage usage
- API requests

### Application Logs

Check logs for database errors:
```bash
# Local
python run.py

# Render
View logs in Render dashboard
```

## 🎉 Success!

Your TimeBank is now connected to Supabase PostgreSQL!

**Next Steps:**
1. Run `python init_supabase_db.py` to initialize
2. Start the app with `python run.py`
3. Login with admin/admin123
4. Deploy to Render

---

**Database:** Supabase PostgreSQL
**Connection:** Secure SSL
**Location:** Cloud-hosted
**Backup:** Automatic

Your time economy is ready to scale! ⏰💰
