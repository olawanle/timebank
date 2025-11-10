# TimeBank - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5000**

## 🎯 Demo Account

Login with these credentials to explore all features:
- **Username**: `admin`
- **Password**: `admin123`

The admin account has 1000 tokens and full admin panel access.

## ✨ What to Try First

### 1. Explore the Homepage
- Learn about the TimeBank concept
- Understand how 1 token = 1 hour works

### 2. Create a New Account
- Click "Register" in the navigation
- Get your unique wallet address
- Receive 10 welcome tokens automatically

### 3. Offer a Service
- Go to Dashboard → "Offer Service"
- Record a service you provided
- Earn tokens (1 token per hour)
- Example: Offer "Python Tutoring" to user "admin" for 2 hours

### 4. Request a Service
- Go to Dashboard → "Request Service"
- Post what help you need
- Set duration (tokens required)
- Wait for community members to accept

### 5. Browse the Marketplace
- Click "Marketplace" in navigation
- See all available service requests
- Accept requests to earn tokens

### 6. Participate in Governance
- Click "Governance" in navigation
- Create a proposal for community changes
- Vote on existing proposals
- Your voting power = your token balance

### 7. Admin Panel (admin account only)
- Click "Admin" in navigation
- View all users, transactions, and services
- Grant admin privileges to other users
- Monitor the entire system

## 📊 Understanding Your Dashboard

Your dashboard shows:
- **Token Balance**: Available tokens to spend
- **Hours Earned**: Total hours of service provided
- **Hours Spent**: Total hours of service received
- **Reputation Score**: Increases with each service (+0.1)
- **Recent Transactions**: Your token transfer history
- **Service History**: All your service exchanges

## 🎨 Features Showcase

### User System
- Secure registration and login
- Unique blockchain wallet addresses
- Password hashing for security

### Service Exchange
- Offer services to earn tokens
- Request services to spend tokens
- Automatic token transfers
- Service status tracking

### Marketplace
- Browse available service requests
- Accept requests instantly
- Real-time token balance updates

### DAO Governance
- Create community proposals
- Token-weighted voting system
- Transparent decision making
- Proposal status tracking

### Admin Panel
- User management
- Transaction monitoring
- Service oversight
- Grant admin privileges

## 🔧 Troubleshooting

### Port Already in Use
If port 5000 is busy, edit `main.py` line 505:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Database Issues
Delete `timebank.db` and restart:
```bash
del timebank.db  # Windows
rm timebank.db   # Linux/Mac
python run.py
```

### Module Not Found
Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## 📱 Responsive Design

The website works perfectly on:
- Desktop computers
- Tablets
- Mobile phones

Try resizing your browser window to see the responsive design in action!

## 🎯 Test Scenarios

### Scenario 1: Complete Service Exchange
1. Login as admin
2. Create a new user account (logout first)
3. Login as new user
4. Request a service (e.g., "Need help with website")
5. Logout and login as admin
6. Go to Marketplace
7. Accept the service request
8. Check both dashboards to see token transfers

### Scenario 2: DAO Governance
1. Login as admin
2. Go to Governance
3. Create a proposal (e.g., "Increase welcome bonus to 20 tokens")
4. Create another user account
5. Login as new user
6. Vote on the proposal
7. See voting results update

### Scenario 3: Build Reputation
1. Offer multiple services
2. Watch your reputation score increase
3. Earn tokens with each service
4. Build trust in the community

## 🌟 Key Features to Highlight

- **Pure Python**: No JavaScript frameworks, all server-side rendering
- **Dark Theme**: Beautiful, futuristic UI design
- **Responsive**: Works on all devices
- **Secure**: Password hashing, session management
- **Real-time**: Instant token transfers and updates
- **Blockchain-Ready**: Wallet addresses and transaction records

## 📚 Next Steps

After exploring the demo:
1. Read the full README.md for technical details
2. Check the code structure in main.py
3. Explore the templates/ directory for UI customization
4. Consider integrating with real blockchain networks

## 🎉 Enjoy TimeBank!

You now have a fully functional crypto-powered time banking system. Every hour is valued equally, and the community governs itself through decentralized voting.

**Welcome to the Time Economy!** ⏰💰
