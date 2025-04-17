from datetime import datetime
from flask_login import UserMixin
from apartment_reviews.app import db

class User(UserMixin, db.Model):
    """User model for both landlords and tenants"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'landlord' or 'tenant'
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    apartments = db.relationship('Apartment', backref='landlord', lazy=True)
    reviews = db.relationship('Review', backref='tenant', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Apartment(db.Model):
    """Apartment listing model"""
    __tablename__ = 'apartments'
    
    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    amenities = db.relationship('Amenity', backref='apartment', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='apartment', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Apartment {self.title}>'
    
    @property
    def average_rating(self):
        """Calculate the average rating for this apartment"""
        if not self.reviews:
            return 0
        
        total = sum(review.rating for review in self.reviews)
        return total / len(self.reviews)
    
    @property
    def amenities_list(self):
        """Return a list of amenity names"""
        return [amenity.name for amenity in self.amenities]

class Amenity(db.Model):
    """Amenity model for apartment features"""
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Amenity {self.name}>'

class Review(db.Model):
    """Review model for tenant ratings and comments"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id} - Rating: {self.rating}>'
