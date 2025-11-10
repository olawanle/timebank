# TimeBank - Crypto-Powered Time Banking System

A decentralized time economy where **1 token = 1 hour of service**. Built with pure Python (Flask) and server-side rendering.

## 🌟 Features

### Core Functionality
- **User System**: Registration with automatic wallet creation and 10 welcome tokens
- **Service Exchange**: Offer services to earn tokens, request services to spend tokens
- **Marketplace**: Browse and accept service requests from the community
- **DAO Governance**: Create proposals and vote using token-based voting power
- **Admin Panel**: Manage users, transactions, and services
- **Reputation System**: Build trust through verified service exchanges

### Technical Features
- Pure Python backend with Flask
- Server-side rendering (no JavaScript frameworks)
- SQLite database with SQLAlchemy ORM
- User authentication with Flask-Login
- Responsive dark-themed UI with Bootstrap 5
- Mock blockchain wallet addresses
- Transaction history tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Demo Account
- **Username**: `admin`
- **Password**: `admin123`

## 📖 How It Works

### 1. Register & Get Your Wallet
- Create an account with username, email, and password
- Receive a unique blockchain wallet address (e.g., `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`)
- Get 10 welcome tokens to start trading

### 2. Offer Services
- Record services you've provided (tutoring, repairs, consulting, etc.)
- Specify duration in hours
- Earn 1 token per hour
- Build reputation (+0.1 per service)

### 3. Request Services
- Post service requests to the marketplace
- Set duration (tokens required)
- Community members can accept your request
- Tokens transfer automatically

### 4. DAO Governance
- Create proposals for community changes
- Vote with your token balance as voting power
- One vote per user per proposal
- Proposals pass based on majority votes

## 🎨 UI Features

- **Dark Mode Theme**: Futuristic, minimal design
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Cards**: Hover effects and smooth transitions
- **Color-Coded Stats**: Visual representation of data
- **Bootstrap Icons**: Clean, modern iconography

## 📊 Database Models

### User
- Username, email, password (hashed)
- Wallet address (unique)
- Token balance, hours earned/spent
- Reputation score
- Admin status

### Service
- Title, description, category
- Duration (hours)
- Provider and requester
- Status (pending, completed, cancelled)

### Transaction
- From/to users
- Amount, type, description
- Timestamp
- Linked service

### Proposal
- Title, description
- Proposer, status
- Votes for/against
- Creation and end dates

### Vote
- Proposal and voter
- Vote type (for/against)
- Voting power (based on tokens)

## 🔐 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection ready (Flask-WTF)
- SQL injection prevention (SQLAlchemy ORM)

## 🛠️ Project Structure

```
timebank/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── timebank.db           # SQLite database (auto-created)
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── home.html         # Landing page
    ├── how_it_works.html # Visual guide
    ├── register.html     # User registration
    ├── login.html        # User login
    ├── dashboard.html    # User dashboard
    ├── offer_service.html    # Offer service form
    ├── request_service.html  # Request service form
    ├── marketplace.html      # Service marketplace
    ├── governance.html       # DAO governance
    ├── create_proposal.html  # Create proposal form
    └── admin.html           # Admin panel
```

## 🎯 Key Principles

1. **Equal Value**: Every hour is worth 1 token, regardless of service type
2. **Trust-Based**: Build reputation through verified exchanges
3. **Decentralized**: Community-governed with transparent principles
4. **Blockchain-Ready**: Built with wallet addresses and transaction records

## 🔄 Future Enhancements

- [ ] Connect to real blockchain (Ethereum, Polygon, etc.)
- [ ] Email notifications for service confirmations
- [ ] Service ratings and reviews
- [ ] Advanced search and filtering
- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Smart contract integration
- [ ] Token staking and rewards

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📧 Support

For questions or support, please open an issue on the repository.

---

**Built with ❤️ using Python & Flask**

*TimeBank - Where Time is Money, and Everyone's Time is Equal*
