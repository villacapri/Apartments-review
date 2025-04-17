# Apartment Reviews Platform

A Flask-based web application that allows landlords to list properties and verified tenants to leave reviews.

## Features

### User Authentication
- User registration for both landlords and tenants
- Secure login/logout functionality
- Role-based access control
- Tenant verification system

### Property Management
- Landlords can create and manage apartment listings
- Detailed property information (price, bedrooms, bathrooms, amenities)
- Location-based information (address, city, state, ZIP)

### Review System
- Verified tenants can submit apartment reviews
- Star rating system (1-5 stars)
- Detailed review comments
- One review per tenant per apartment policy

### Search and Discovery
- Browse all available listings
- Filter by location (city, state, ZIP)
- Filter by price range and number of bedrooms/bathrooms
- View apartment details and reviews

## Technology Stack

- **Backend:** Python with Flask framework
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Frontend:** Pure HTML and CSS (no JavaScript dependencies)
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF with form validation

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database

### Environment Variables
Set up the following environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for session security

### Installation Steps
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/apartment-reviews.git
   cd apartment-reviews
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application
   ```bash
   python main.py
   ```

4. Navigate to `http://localhost:5000` in your browser

## Project Structure

```
apartment_reviews/
├── static/              # CSS and static assets
├── templates/           # HTML templates
├── __init__.py          # Package initialization
├── app.py               # Application configuration
├── forms.py             # Form definitions
├── models.py            # Database models
└── main.py              # Application entry point
```

## Database Schema

- **Users:** Landlords and tenants with authentication details
- **Apartments:** Property listings with details and amenities
- **Reviews:** Tenant reviews of apartments with ratings
- **Amenities:** Features of apartments listed by landlords

## License

This project is licensed under the MIT License - see the LICENSE file for details.