import os
from apartment_reviews.app import app

# Set a default session secret if not provided in environment
if not os.environ.get("SESSION_SECRET"):
    os.environ["SESSION_SECRET"] = "apartment-reviews-secret-key"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)