# 🔧 Fix Render Deployment - Update Start Command

## ⚠️ Issue

Render is trying to run `gunicorn app:app` but we deleted `app.py` and are using `main.py` instead.

## ✅ Solution: Update Render Dashboard Settings

### Step 1: Go to Render Dashboard

Visit: https://dashboard.render.com

### Step 2: Select Your TimeBank Service

Click on your **timebank** web service

### Step 3: Update Start Command

1. Click on **"Settings"** tab (left sidebar)
2. Scroll down to **"Build & Deploy"** section
3. Find **"Start Command"** field
4. Change from: `gunicorn app:app`
5. Change to: **`gunicorn main:app`**
6. Click **"Save Changes"**

### Step 4: Trigger Manual Deploy

1. Go to **"Manual Deploy"** section (top right)
2. Click **"Deploy latest commit"**
3. Wait for deployment to complete (5-10 minutes)

## 🎯 Alternative: Use Environment Variable

If the above doesn't work, you can also:

1. Go to **"Environment"** tab
2. Add a new environment variable:
   - **Key**: `GUNICORN_CMD_ARGS`
   - **Value**: `--bind=0.0.0.0:$PORT main:app`
3. Save and redeploy

## ✅ Verification

After deployment, check the logs. You should see:

```
✓ Using Supabase PostgreSQL database
📡 Testing database connection...
✓ Database connection successful
📊 Creating database tables...
✓ Database tables created successfully
👤 Checking admin user...
✓ Admin user created: username=admin, password=admin123
```

## 🚀 Your App Will Be Live!

Once deployed successfully:
- URL: `https://timebank-xxxx.onrender.com`
- Login: admin / admin123
- Fully functional with Supabase!

## 📋 Quick Checklist

- [ ] Go to Render Dashboard
- [ ] Select timebank service
- [ ] Settings → Start Command
- [ ] Change to: `gunicorn main:app`
- [ ] Save Changes
- [ ] Manual Deploy → Deploy latest commit
- [ ] Wait for deployment
- [ ] Test your live URL
- [ ] Login with admin/admin123

---

**The code is correct!** You just need to update the Render dashboard settings to use `main:app` instead of `app:app`.
