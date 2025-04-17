# Contributing to Apartment Reviews Platform

Thank you for considering contributing to the Apartment Reviews Platform! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug in the application:

1. Check if the bug has already been reported in the Issues section
2. If not, create a new issue with a descriptive title and detailed information:
   - Steps to reproduce the bug
   - Expected behavior
   - Actual behavior
   - Screenshots (if applicable)
   - Environment details (OS, browser, etc.)

### Suggesting Enhancements

If you have ideas for improvements:

1. Check if the enhancement has already been suggested in the Issues section
2. If not, create a new issue with a descriptive title and detailed information:
   - Clear description of the enhancement
   - Rationale and use cases
   - Any references or examples

### Pull Requests

1. Fork the repository
2. Create a new branch from `main` for your feature or bugfix
3. Make your changes
4. Write or update tests as needed
5. Ensure all tests pass
6. Submit a pull request with a descriptive title and details about your changes

## Development Setup

1. Clone the repository
2. Install dependencies from `project_requirements.txt`
3. Set up environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SESSION_SECRET`: Secret key for session security
4. Run the application with `python main.py`

## Coding Guidelines

### Python Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Include docstrings for functions and classes

### HTML/CSS Style

- Use semantic HTML elements
- Keep CSS organized and minimal
- Ensure accessibility standards are met

### Git Commit Messages

- Use clear, concise commit messages
- Begin with a verb in the present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

## Testing

- Write tests for new features or bug fixes
- Ensure all existing tests pass before submitting a pull request

Thank you for your contributions!