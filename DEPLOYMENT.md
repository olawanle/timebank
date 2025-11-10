# TimeBank - Deployment Guide

## 🚀 Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available at https://render.com)

### Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - TimeBank crypto time banking system"

# Add remote repository
git remote add origin https://github.com/olawanle/timebank.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect GitHub Repository**
   - Select "Connect a repository"
   - Choose `olawanle/timebank`
   - Click "Connect"

3. **Configure Web Service**
   - **Name**: `timebank`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Plan**: Free (or choose paid plan)

4. **Add Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add these variables:
     ```
     SECRET_KEY = (auto-generated or your own secret)
     PYTHON_VERSION = 3.11.0
     ```

5. **Create Database (Optional - for PostgreSQL)**
   - Click "New +" → "PostgreSQL"
   - Name: `timebank-db`
   - Plan: Free
   - After creation, copy the "Internal Database URL"
   - Add to web service as `DATABASE_URL`

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://timebank-xxxx.onrender.com`

### Step 3: Initialize Database

After first deployment:
1. Go to Render Dashboard → Your Service → Shell
2. Run: `python -c "from main import init_db; init_db()"`

Or the database will auto-initialize on first request.

## 🔧 Configuration Files

### Procfile
Tells Render how to run the app:
```
web: gunicorn main:app
```

### requirements.txt
All Python dependencies including `gunicorn` for production.

### runtime.txt
Specifies Python version:
```
python-3.11.0
```

### render.yaml (Optional)
Infrastructure as code for Render deployment.

## 🌐 Environment Variables

### Required:
- `SECRET_KEY` - Flask secret key (auto-generated on Render)

### Optional:
- `DATABASE_URL` - PostgreSQL connection string (defaults to SQLite)
- `PORT` - Port number (auto-set by Render)
- `DEBUG` - Set to 'False' in production (default)

## 📊 Database Options

### Option 1: SQLite (Default)
- Good for testing and small deployments
- File-based database
- No additional setup needed

### Option 2: PostgreSQL (Recommended for Production)
- Better for production use
- Persistent data
- Better performance
- Free tier available on Render

To use PostgreSQL:
1. Create PostgreSQL database on Render
2. Copy "Internal Database URL"
3. Add as `DATABASE_URL` environment variable
4. Redeploy

## 🔐 Security Notes

1. **Secret Key**: Always use environment variable in production
2. **Debug Mode**: Set `DEBUG=False` in production
3. **Database**: Use PostgreSQL for production, not SQLite
4. **HTTPS**: Render provides free SSL certificates

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` for correct package versions
- Verify Python version in `runtime.txt`

### App Crashes
- Check logs in Render Dashboard
- Verify environment variables are set
- Ensure database is initialized

### Database Issues
- For PostgreSQL: Check `DATABASE_URL` is correct
- For SQLite: Database will be created automatically

### Static Files Not Loading
- Ensure templates folder is committed to Git
- Check file paths are relative

## 📝 Post-Deployment

1. **Test the Application**
   - Visit your Render URL
   - Register a new account
   - Test all features

2. **Create Admin Account**
   - Default admin: username=`admin`, password=`admin123`
   - Change password immediately!

3. **Monitor Performance**
   - Check Render Dashboard for metrics
   - Monitor logs for errors

## 🔄 Updates

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Render will automatically redeploy on push to main branch.

## 💰 Costs

### Free Tier (Render)
- Web Service: Free (spins down after inactivity)
- PostgreSQL: Free (90 days, then $7/month)
- SSL Certificate: Free
- Custom Domain: Free

### Paid Tier
- Web Service: $7/month (always on)
- PostgreSQL: $7/month (persistent)
- Better performance and uptime

## 🎉 Success!

Your TimeBank application is now live and accessible worldwide!

**Live URL**: `https://timebank-xxxx.onrender.com`

Share it with your community and start building the time economy! ⏰💰

---

For issues or questions, check the Render documentation:
https://render.com/docs
