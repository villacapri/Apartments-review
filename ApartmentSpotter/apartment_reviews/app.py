import os
import logging
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize SQLAlchemy with a base class
class Base(DeclarativeBase):
    pass

# Initialize Flask extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Create the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the SQLAlchemy database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

# Import models after db initialization to avoid circular imports
with app.app_context():
    from apartment_reviews.models import User, Apartment, Review, Amenity
    from apartment_reviews.forms import (
        LoginForm, RegistrationForm, ApartmentForm, 
        ReviewForm, SearchForm, ApartmentSearchForm,
        VerificationRequestForm
    )
    
    # Create all database tables
    db.create_all()

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from apartment_reviews.models import User
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
def index():
    """Homepage with search and featured listings"""
    from apartment_reviews.models import Apartment
    from apartment_reviews.forms import ApartmentSearchForm
    
    search_form = ApartmentSearchForm()
    
    # Fetch a few recent listings for the homepage
    recent_listings = Apartment.query.order_by(Apartment.created_at.desc()).limit(6).all()
    
    return render_template('index.html', 
                         search_form=search_form,
                         recent_listings=recent_listings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    from apartment_reviews.models import User
    from apartment_reviews.forms import RegistrationForm
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect(url_for('login'))
        
        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            user_type=form.user_type.data,
            is_verified=False,
            created_at=datetime.utcnow()
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    from apartment_reviews.models import User
    from apartment_reviews.forms import LoginForm
    
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Login failed. Please check your email and password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    from apartment_reviews.models import Apartment, Review
    from apartment_reviews.forms import VerificationRequestForm
    
    verification_form = VerificationRequestForm()
    
    if current_user.user_type == 'landlord':
        # Get landlord's listings
        listings = Apartment.query.filter_by(landlord_id=current_user.id).all()
        return render_template('profile.html', 
                              listings=listings, 
                              verification_form=verification_form)
    else:
        # Get tenant's reviews
        reviews = Review.query.filter_by(tenant_id=current_user.id).all()
        return render_template('profile.html', 
                              reviews=reviews, 
                              verification_form=verification_form)

@app.route('/request_verification', methods=['POST'])
@login_required
def request_verification():
    """Process tenant verification requests"""
    from apartment_reviews.forms import VerificationRequestForm
    
    form = VerificationRequestForm()
    
    if form.validate_on_submit() and current_user.user_type == 'tenant':
        current_user.is_verified = True
        db.session.commit()
        flash('Your account has been verified!', 'success')
    else:
        flash('Verification request failed.', 'error')
    
    return redirect(url_for('profile'))

@app.route('/listings')
def listings():
    """View all apartment listings with search functionality"""
    from apartment_reviews.models import Apartment
    from apartment_reviews.forms import ApartmentSearchForm
    
    form = ApartmentSearchForm()
    
    query = Apartment.query
    
    # Apply filters if provided
    city = request.args.get('city')
    state = request.args.get('state')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    bedrooms = request.args.get('bedrooms')
    bathrooms = request.args.get('bathrooms')
    
    if city:
        query = query.filter(Apartment.city.ilike(f'%{city}%'))
    if state:
        query = query.filter(Apartment.state == state)
    if min_price:
        query = query.filter(Apartment.price >= min_price)
    if max_price:
        query = query.filter(Apartment.price <= max_price)
    if bedrooms:
        query = query.filter(Apartment.bedrooms == bedrooms)
    if bathrooms:
        query = query.filter(Apartment.bathrooms == bathrooms)
    
    # Get search results
    apartments = query.order_by(Apartment.created_at.desc()).all()
    
    return render_template('listings.html', 
                          apartments=apartments, 
                          form=form)

@app.route('/apartment/<int:apartment_id>')
def view_apartment(apartment_id):
    """View a single apartment listing with reviews"""
    from apartment_reviews.models import Apartment, Review
    from apartment_reviews.forms import ReviewForm
    
    apartment = db.session.get(Apartment, apartment_id)
    
    if not apartment:
        flash('Apartment listing not found.', 'error')
        return redirect(url_for('listings'))
    
    review_form = ReviewForm()
    
    # Calculate average rating
    reviews = Review.query.filter_by(apartment_id=apartment.id).all()
    avg_rating = 0
    if reviews:
        total = sum(review.rating for review in reviews)
        avg_rating = total / len(reviews)
    
    return render_template('view_listing.html', 
                          apartment=apartment, 
                          reviews=reviews,
                          avg_rating=avg_rating,
                          review_form=review_form)

@app.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    """Create a new apartment listing (landlords only)"""
    from apartment_reviews.models import Apartment, Amenity
    from apartment_reviews.forms import ApartmentForm
    
    if current_user.user_type != 'landlord':
        flash('Only landlords can create listings.', 'error')
        return redirect(url_for('index'))
    
    form = ApartmentForm()
    
    if form.validate_on_submit():
        # Create new apartment listing
        apartment = Apartment(
            landlord_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            price=form.price.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(apartment)
        db.session.commit()
        
        # Add amenities
        if form.amenities.data:
            amenities = form.amenities.data.split(',')
            for amenity_name in amenities:
                amenity_name = amenity_name.strip()
                if amenity_name:
                    amenity = Amenity(
                        apartment_id=apartment.id,
                        name=amenity_name
                    )
                    db.session.add(amenity)
        
        db.session.commit()
        
        flash('Apartment listing created successfully!', 'success')
        return redirect(url_for('view_apartment', apartment_id=apartment.id))
    
    return render_template('create_listing.html', form=form)

@app.route('/add_review/<int:apartment_id>', methods=['POST'])
@login_required
def add_review(apartment_id):
    """Add a review to an apartment (verified tenants only)"""
    from apartment_reviews.models import Review, Apartment
    from apartment_reviews.forms import ReviewForm
    
    apartment = db.session.get(Apartment, apartment_id)
    
    if not apartment:
        flash('Apartment listing not found.', 'error')
        return redirect(url_for('listings'))
    
    if current_user.user_type != 'tenant':
        flash('Only tenants can leave reviews.', 'error')
        return redirect(url_for('view_apartment', apartment_id=apartment_id))
    
    if not current_user.is_verified:
        flash('You need to be a verified tenant to leave reviews. Please request verification in your profile.', 'error')
        return redirect(url_for('view_apartment', apartment_id=apartment_id))
    
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if user already reviewed this apartment
        existing_review = Review.query.filter_by(
            apartment_id=apartment_id,
            tenant_id=current_user.id
        ).first()
        
        if existing_review:
            flash('You have already reviewed this apartment.', 'error')
            return redirect(url_for('view_apartment', apartment_id=apartment_id))
        
        # Create new review
        review = Review(
            apartment_id=apartment_id,
            tenant_id=current_user.id,
            rating=form.rating.data,
            comment=form.comment.data,
            created_at=datetime.utcnow()
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Review added successfully!', 'success')
    else:
        flash('Error adding review. Please try again.', 'error')
    
    return redirect(url_for('view_apartment', apartment_id=apartment_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
