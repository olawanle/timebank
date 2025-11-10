# 🔌 Supabase Connection Guide

## ⚠️ Important: Get Your Correct Connection String

The connection string in the code is a template. You need to get your **actual** connection string from Supabase.

## 📋 Steps to Get Your Supabase Connection String

### 1. Go to Supabase Dashboard
Visit: https://app.supabase.com/project/mvpugxwlufztwqunjysf

### 2. Navigate to Database Settings
- Click on **"Settings"** (gear icon in sidebar)
- Click on **"Database"**

### 3. Find Connection String
Scroll down to **"Connection string"** section

You'll see two options:

#### Option A: Connection Pooling (Recommended for Production)
```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

#### Option B: Direct Connection
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 4. Copy the Correct String
- Click **"URI"** tab
- Select **"Connection pooling"** mode
- Click the copy button
- **Important**: Replace `[YOUR-PASSWORD]` with your actual database password

## 🔐 Your Database Password

If you don't know your database password:

1. Go to Supabase Dashboard → Settings → Database
2. Scroll to **"Database password"**
3. Click **"Reset database password"** if needed
4. **Save the new password securely**

## 🔧 Update Your Configuration

### For Local Development

Create a `.env` file:
```bash
DATABASE_URL=your-actual-connection-string-here
SECRET_KEY=your-secret-key
```

### For Render Deployment

1. Go to Render Dashboard
2. Select your web service
3. Go to **Environment** tab
4. Update `DATABASE_URL` with your actual Supabase connection string
5. Save changes

## ✅ Test Your Connection

After getting the correct connection string, test it:

```bash
python test_supabase_connection.py
```

## 🚀 Production-Ready Setup

Once you have the correct connection string:

### 1. Update main.py

Replace the SUPABASE_DB_URL with your actual connection string:

```python
SUPABASE_DB_URL = 'your-actual-connection-string-here'
```

### 2. Update render.yaml

```yaml
- key: DATABASE_URL
  value: your-actual-connection-string-here
```

### 3. Commit and Push

```bash
git add .
git commit -m "Update Supabase connection string"
git push origin main
```

### 4. Deploy to Render

The app will now connect to Supabase successfully!

## 🔍 Common Issues

### Issue 1: "FATAL: password authentication failed"
**Solution**: Your password is incorrect. Reset it in Supabase dashboard.

### Issue 2: "could not translate host name"
**Solution**: Check your internet connection or verify the project reference is correct.

### Issue 3: "connection refused"
**Solution**: 
- Verify your Supabase project is active (not paused)
- Check if you're using the correct port (6543 for pooler, 5432 for direct)

### Issue 4: "SSL required"
**Solution**: The code already includes `sslmode='require'` - this should work.

## 📊 Verify Database is Ready

After connecting, initialize the database:

```bash
python init_supabase_db.py
```

This will:
- Create all tables
- Create admin user
- Verify everything works

## 🎯 Quick Checklist

- [ ] Get connection string from Supabase dashboard
- [ ] Verify password is correct
- [ ] Test connection with test script
- [ ] Update main.py with correct URL
- [ ] Update render.yaml with correct URL
- [ ] Commit and push to GitHub
- [ ] Deploy to Render
- [ ] Verify app works

## 💡 Pro Tip

For security, **never commit your actual database password to GitHub**. Instead:

1. Use environment variables
2. Set `DATABASE_URL` in Render dashboard
3. Keep `.env` file in `.gitignore` (already done)

## 🆘 Still Having Issues?

1. Check Supabase project status in dashboard
2. Verify project is not paused
3. Try resetting database password
4. Check Supabase status page: https://status.supabase.com
5. Contact Supabase support if needed

---

Once you have the correct connection string, your TimeBank will be production-ready! 🚀
