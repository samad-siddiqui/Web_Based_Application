# Django Middleware Project

## Overview
This Django-based web application includes advanced middleware functionalities for:

- **Logging user IPs**
- **Enforcing rate limiting**
- **Implementing access control based on user roles**

## Middleware Functionality

### 1. Logging Middleware
- Captures and logs the IP address and request time for every incoming request.
- Uses Python's `logging` module to store logged data in a file without overriding it.

### 2. Rate Limiting Middleware
- Limits users to a specific number of requests per minute.
- Default limit: **5 requests per minute**.
- Automatically unblocks users after **1 minute**.
- Returns appropriate exception messages for rate limit violations.

### 3. Role-Based Access Control
Rate limits based on user roles:

- **Gold users**: Up to **10 requests** per minute.
- **Silver users**: Up to **5 requests** per minute.
- **Bronze users**: Up to **2 requests** per minute.
- **Unauthenticated users**: Only **1 request** per minute.

## Views Implemented

- **User Registration View**
- **Login View**
- **Logout View**
- **Class-Based Views** to demonstrate middleware functionalities across various endpoints.

## Custom User Model

- Email is used as the primary identifier instead of a username.
- Users can log in using email instead of username.
- Superusers are created using email.
- Updated Django Admin to display user details in four sections:
  1. **Username & Password**
  2. **is_active, is_staff, is_superuser**
  3. **Last login & other details**

## Testing

- **Comprehensive test cases** for:
  - IP logging
  - Rate limiting
  - Role-based access control

## Pre-commit Setup

1. Install pre-commit:

   ```bash
   pip install pre-commit
2. Set up pre-commit hooks:
    ```bash
   pre-commit install
3. Run pre-commit manually (optional):
    ```bash
   pre-commit run --all-files
## Running the project form scratch
### Prerequisites
- Python 3.8+
- django
- Virtual Environment

### Steps
1. Clone repository
```bash 
git clone https://github.com/samad-siddiqui/Web_Based_Application
cd MainProj
```
2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```
3. Change Directory
```bash
cd core
```
4. Install Dependencies
```bash
pip install -r requirements.txt
```
5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Create Superuser
```bash
python manage.py createsuperuser
```
7. Run the server
```bash
python manage.py runserver
```
### Run Tests
Run all tests cases using:
```bash
python manage.py test
```
