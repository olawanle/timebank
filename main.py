"""
TimeBank - Crypto-Powered Time Banking System
A decentralized time economy where 1 token = 1 hour of service
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import os

app = Flask(__name__)

# Configuration for production and development
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Supabase PostgreSQL Database URL
# Replace with your actual Supabase credentials
SUPABASE_DB_URL = os.environ.get('SUPABASE_URL', 'postgresql://postgres:olawanle@db.mvpugxwlufztwqunjysf.supabase.co:5432/postgres')

# Use Supabase URL or fallback to SQLite for local development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', SUPABASE_DB_URL)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PostgreSQL connection pooling settings
if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI']:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 10,
        'max_overflow': 20,
        'connect_args': {
            'connect_timeout': 10,
        }
    }

# Fix for Render PostgreSQL URL (if needed)
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    """User model with wallet and reputation system"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)
    token_balance = db.Column(db.Float, default=10.0)  # Starting bonus
    hours_earned = db.Column(db.Float, default=0.0)
    hours_spent = db.Column(db.Float, default=0.0)
    reputation_score = db.Column(db.Float, default=5.0)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    services_offered = db.relationship('Service', backref='provider', lazy=True, foreign_keys='Service.provider_id')
    services_requested = db.relationship('Service', backref='requester', lazy=True, foreign_keys='Service.requester_id')
    votes = db.relationship('Vote', backref='voter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    """Service exchange records"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Float, nullable=False)  # Hours
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    service_type = db.Column(db.String(20), nullable=False)  # offer or request
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

class Transaction(db.Model):
    """Token transaction records"""
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # service, bonus, governance
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    from_user = db.relationship('User', foreign_keys=[from_user_id], backref='sent_transactions')
    to_user = db.relationship('User', foreign_keys=[to_user_id], backref='received_transactions')
    service = db.relationship('Service', backref='transactions')

class Proposal(db.Model):
    """DAO Governance proposals"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    proposer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, passed, rejected
    votes_for = db.Column(db.Integer, default=0)
    votes_against = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime, nullable=False)
    
    proposer = db.relationship('User', backref='proposals')
    votes = db.relationship('Vote', backref='proposal', lazy=True)

class Vote(db.Model):
    """Voting records for proposals"""
    id = db.Column(db.Integer, primary_key=True)
    proposal_id = db.Column(db.Integer, db.ForeignKey('proposal.id'), nullable=False)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vote_type = db.Column(db.String(10), nullable=False)  # for or against
    voting_power = db.Column(db.Float, nullable=False)  # Based on token balance
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== LOGIN MANAGER ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== HELPER FUNCTIONS ====================

def generate_wallet_address():
    """Generate a mock blockchain wallet address"""
    return '0x' + secrets.token_hex(20)

def create_transaction(from_user, to_user, amount, trans_type, description, service_id=None):
    """Create a token transaction record"""
    transaction = Transaction(
        from_user_id=from_user.id if from_user else None,
        to_user_id=to_user.id if to_user else None,
        amount=amount,
        transaction_type=trans_type,
        description=description,
        service_id=service_id
    )
    db.session.add(transaction)
    return transaction

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Home page explaining TimeBank"""
    return render_template('home.html')

@app.route('/how-it-works')
def how_it_works():
    """Visual guide to time-for-token exchange"""
    return render_template('how_it_works.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with wallet creation"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            wallet_address=generate_wallet_address()
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create welcome bonus transaction
        create_transaction(None, user, 10.0, 'bonus', 'Welcome bonus - 10 time tokens!')
        db.session.commit()
        
        flash(f'Account created! Your wallet: {user.wallet_address}', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing balance and history"""
    recent_transactions = Transaction.query.filter(
        (Transaction.from_user_id == current_user.id) | 
        (Transaction.to_user_id == current_user.id)
    ).order_by(Transaction.timestamp.desc()).limit(10).all()
    
    my_services = Service.query.filter(
        (Service.provider_id == current_user.id) | 
        (Service.requester_id == current_user.id)
    ).order_by(Service.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         transactions=recent_transactions,
                         services=my_services)

@app.route('/offer-service', methods=['GET', 'POST'])
@login_required
def offer_service():
    """Form to record a service given (earns tokens)"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        duration = float(request.form.get('duration'))
        requester_username = request.form.get('requester_username')
        
        requester = User.query.filter_by(username=requester_username).first()
        
        if not requester:
            flash('Requester not found', 'error')
            return redirect(url_for('offer_service'))
        
        if requester.token_balance < duration:
            flash('Requester has insufficient tokens', 'error')
            return redirect(url_for('offer_service'))
        
        # Create service record
        service = Service(
            title=title,
            description=description,
            category=category,
            duration=duration,
            service_type='offer',
            provider_id=current_user.id,
            requester_id=requester.id,
            status='completed',
            completed_at=datetime.utcnow()
        )
        db.session.add(service)
        db.session.flush()
        
        # Transfer tokens
        requester.token_balance -= duration
        requester.hours_spent += duration
        current_user.token_balance += duration
        current_user.hours_earned += duration
        
        # Update reputation
        current_user.reputation_score += 0.1
        
        # Create transaction record
        create_transaction(requester, current_user, duration, 'service', 
                         f'Service: {title}', service.id)
        
        db.session.commit()
        
        flash(f'Service recorded! You earned {duration} tokens', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('offer_service.html')

@app.route('/request-service', methods=['GET', 'POST'])
@login_required
def request_service():
    """Form to spend tokens for help"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        duration = float(request.form.get('duration'))
        
        if current_user.token_balance < duration:
            flash('Insufficient tokens', 'error')
            return redirect(url_for('request_service'))
        
        # Create service request
        service = Service(
            title=title,
            description=description,
            category=category,
            duration=duration,
            service_type='request',
            requester_id=current_user.id,
            status='pending'
        )
        db.session.add(service)
        db.session.commit()
        
        flash('Service request posted! Waiting for a provider', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('request_service.html')

@app.route('/marketplace')
@login_required
def marketplace():
    """View all available service requests"""
    available_services = Service.query.filter_by(
        service_type='request',
        status='pending'
    ).order_by(Service.created_at.desc()).all()
    
    return render_template('marketplace.html', services=available_services)

@app.route('/accept-service/<int:service_id>')
@login_required
def accept_service(service_id):
    """Accept a service request"""
    service = Service.query.get_or_404(service_id)
    
    if service.status != 'pending':
        flash('Service is no longer available', 'error')
        return redirect(url_for('marketplace'))
    
    requester = User.query.get(service.requester_id)
    
    if requester.token_balance < service.duration:
        flash('Requester has insufficient tokens', 'error')
        return redirect(url_for('marketplace'))
    
    # Update service
    service.provider_id = current_user.id
    service.status = 'completed'
    service.completed_at = datetime.utcnow()
    
    # Transfer tokens
    requester.token_balance -= service.duration
    requester.hours_spent += service.duration
    current_user.token_balance += service.duration
    current_user.hours_earned += service.duration
    
    # Update reputation
    current_user.reputation_score += 0.1
    
    # Create transaction
    create_transaction(requester, current_user, service.duration, 'service',
                     f'Service: {service.title}', service.id)
    
    db.session.commit()
    
    flash(f'Service accepted! You earned {service.duration} tokens', 'success')
    return redirect(url_for('dashboard'))

@app.route('/governance')
@login_required
def governance():
    """DAO Governance page with proposals and voting"""
    proposals = Proposal.query.order_by(Proposal.created_at.desc()).all()
    return render_template('governance.html', proposals=proposals)

@app.route('/create-proposal', methods=['GET', 'POST'])
@login_required
def create_proposal():
    """Create a new governance proposal"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        days = int(request.form.get('days', 7))
        
        from datetime import timedelta
        ends_at = datetime.utcnow() + timedelta(days=days)
        
        proposal = Proposal(
            title=title,
            description=description,
            proposer_id=current_user.id,
            ends_at=ends_at
        )
        db.session.add(proposal)
        db.session.commit()
        
        flash('Proposal created successfully!', 'success')
        return redirect(url_for('governance'))
    
    return render_template('create_proposal.html')

@app.route('/vote/<int:proposal_id>/<vote_type>')
@login_required
def vote(proposal_id, vote_type):
    """Vote on a proposal"""
    proposal = Proposal.query.get_or_404(proposal_id)
    
    if proposal.status != 'active':
        flash('Voting has ended for this proposal', 'error')
        return redirect(url_for('governance'))
    
    if datetime.utcnow() > proposal.ends_at:
        proposal.status = 'passed' if proposal.votes_for > proposal.votes_against else 'rejected'
        db.session.commit()
        flash('Voting period has ended', 'error')
        return redirect(url_for('governance'))
    
    # Check if already voted
    existing_vote = Vote.query.filter_by(
        proposal_id=proposal_id,
        voter_id=current_user.id
    ).first()
    
    if existing_vote:
        flash('You have already voted on this proposal', 'error')
        return redirect(url_for('governance'))
    
    # Create vote (voting power based on token balance)
    voting_power = current_user.token_balance
    vote_record = Vote(
        proposal_id=proposal_id,
        voter_id=current_user.id,
        vote_type=vote_type,
        voting_power=voting_power
    )
    db.session.add(vote_record)
    
    if vote_type == 'for':
        proposal.votes_for += 1
    else:
        proposal.votes_against += 1
    
    db.session.commit()
    
    flash(f'Vote recorded! Your voting power: {voting_power:.2f} tokens', 'success')
    return redirect(url_for('governance'))

@app.route('/admin')
@login_required
def admin():
    """Admin panel to manage users and transactions"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    transactions = Transaction.query.order_by(Transaction.timestamp.desc()).limit(50).all()
    services = Service.query.order_by(Service.created_at.desc()).limit(50).all()
    
    return render_template('admin.html', 
                         users=users,
                         transactions=transactions,
                         services=services)

@app.route('/admin/make-admin/<int:user_id>')
@login_required
def make_admin(user_id):
    """Grant admin privileges"""
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    
    flash(f'{user.username} is now an admin', 'success')
    return redirect(url_for('admin'))

# ==================== INITIALIZE DATABASE ====================

def init_db():
    """Initialize database with tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print('✓ Database tables created successfully')
            
            # Create admin user if doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@timebank.com',
                    wallet_address=generate_wallet_address(),
                    is_admin=True,
                    token_balance=1000.0
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print('✓ Admin user created: username=admin, password=admin123')
            else:
                print('✓ Admin user already exists')
                
        except Exception as e:
            print(f'✗ Database initialization error: {e}')
            db.session.rollback()
            raise

# ==================== RUN APP ====================

if __name__ == '__main__':
    init_db()
    # Use environment variables for production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False') == 'True'
    app.run(debug=debug, host='0.0.0.0', port=port)
