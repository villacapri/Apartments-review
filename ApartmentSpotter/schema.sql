-- Database schema for Apartment Reviews Platform

-- Users table (both landlords and tenants)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    user_type VARCHAR(10) NOT NULL, -- 'landlord' or 'tenant'
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Apartments table (property listings)
CREATE TABLE apartments (
    id SERIAL PRIMARY KEY,
    landlord_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    address VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    price FLOAT NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Amenities table (apartment features)
CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    apartment_id INTEGER NOT NULL REFERENCES apartments(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL
);

-- Reviews table (tenant ratings and comments)
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    apartment_id INTEGER NOT NULL REFERENCES apartments(id) ON DELETE CASCADE,
    tenant_id INTEGER NOT NULL REFERENCES users(id),
    rating INTEGER NOT NULL, -- 1-5 stars
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(apartment_id, tenant_id) -- One review per tenant per apartment
);

-- Indexes for performance
CREATE INDEX idx_apartments_landlord ON apartments(landlord_id);
CREATE INDEX idx_apartments_city ON apartments(city);
CREATE INDEX idx_apartments_state ON apartments(state);
CREATE INDEX idx_amenities_apartment ON amenities(apartment_id);
CREATE INDEX idx_reviews_apartment ON reviews(apartment_id);
CREATE INDEX idx_reviews_tenant ON reviews(tenant_id);