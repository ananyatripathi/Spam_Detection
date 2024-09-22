# Spam Detection API

## Overview

Welcome to the Spam Detection API! This Django-based web application manages user profiles, contacts, and spam records. It includes features for user registration, login, profile management, contact management, spam marking, and search functionality.

### Project Structure

The project consists of the following six Django apps:

1. **accounts**: Manages user registration, authentication, and profile operations.
2. **search**: Provides functionality to search for users, contacts, and spam records.
3. **contacts**: Handles operations related to user contacts.
4. **spam_management**: Manages the marking and tracking of spam numbers.
5. **user_profile**: Manages user profile details.
6. **management_utils**: Contains custom management commands for tasks like data population.

## API Endpoints

### 1. User Management

#### Register User
- **Endpoint**: `POST /api/accounts/register/`
- **Request Body**:
    ```json
    {
        "phone_number": "8840627020",
        "name": "Atharva Tripathi",
        "password": "securepassword",
        "email": "atharvatripathi@gmail.com"
    }
    ```
- **Response**:
    ```json
    {
        "id": 263,
        "phone_number": "8840627020",
        "name": "Atharva Tripathi",
        "email": "atharvatripathi@gmail.com"
    }
    ```

#### Login
- **Endpoint**: `POST /api/accounts/login/`
- **Request Body**:
    ```json
    {
        "phone_number": "0987654321",
        "password": "super@123"
    }
    ```
- **Response**:
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMTU2OTA1MSwiaWF0IjoxNzIxNDgyNjUxLCJqdGkiOiIwNzgzN2ZkYTYyNGY0ZGRjODFmMWIxMjQyYmVmYWZlYSIsInVzZXJfaWQiOjV9.JbZbjjZtjwI1U1vzJv1y5iM5fer8HeiX7av8pcBZkMY",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxNDgyOTUxLCJpYXQiOjE3MjE0ODI2NTEsImp0aSI6IjhlYTRlNWJkZTQ4NTQxNDBiYWZhNzQ1NGExM2IzYjk2IiwidXNlcl9pZCI6NX0.3nV87w_62WMi4Xrklmf95p-jKEi0sovzWnujz2RjdtI"
    }
    ```

#### Logout
- **Endpoint**: `POST /api/accounts/logout/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**: Status `205 Reset Content`

### 2. Profile Management

#### Get Profile
- **Endpoint**: `GET /api/profile/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**:
    ```json
    {
        "name": "Super User",
        "email": null,
        "phone_number": "0987654321"
    }
    ```

#### Update Profile
- **Endpoint**: `PUT /api/profile/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Request Body**:
    ```json
    {
        "email": "superuser@gmail.com"
    }
    ```
- **Response**:
    ```json
    {
        "name": "Super User",
        "email": "superuser@gmail.com",
        "phone_number": "0987654321"
    }
    ```

### 3. Contact Management

#### Add Contact
- **Endpoint**: `POST /api/contacts/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Request Body**:
    ```json
    {
        "name": "Aparna",
        "phone_number": "9805678350"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1484,
        "phone_number": "9805678350",
        "name": "Aparna"
    }
    ```

#### Get Contacts
- **Endpoint**: `GET /api/contacts/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**:
    ```json
    [
        {
            "id": 1484,
            "phone_number": "9805678350",
            "name": "Aparna"
        }
    ]
    ```

#### Delete Contact
- **Endpoint**: `DELETE /api/contacts/<contact_id>`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**: Status `204 No Content`

### 4. Spam Management

#### Mark Spam
- **Endpoint**: `POST /api/spam/`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Request Body**:
    ```json
    {
        "phone_number": "6829721936"
    }
    ```
- **Response**:
    ```json
    {
        "message": "Phone number marked as spam.",
        "spam_count": 2
    }
    ```

### 5. Search

#### Search by Name
- **Endpoint**: `GET /api/search/?q=<name>&type=name`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**:
    ```json
    [
        {
            "name": "User0",
            "phone_number": "123456780",
            "email": null,
            "spam_count": 0
        },
        {
            "name": "User1",
            "phone_number": "123456781",
            "email": null,
            "spam_count": 1
        }
    ]
    ```

#### Search by Phone
- **Endpoint**: `GET /api/search/?q=<phone_number>&type=phone`
- **Request Header**:
    ```
    Authorization: Bearer <access_token>
    ```
- **Response**:
    ```json
    [
        {
            "name": "User0",
            "phone_number": "123456780",
            "email": null,
            "spam_count": 0
        },
        {
            "name": "User1",
            "phone_number": "123456781",
            "email": null,
            "spam_count": 1
        }
    ]
    ```

## Management Utilities

The `management_utils` app includes custom Django management commands to help with tasks such as data population.

### Populating Data

To populate the database with sample data, use the following management command:

```bash
python manage.py populate_data
```

## Running the Application

1. **Install Dependencies**: Make a virtual environment and ensure all required packages are installed by running:

    ```bash
    pip install -r requirements.txt
    ```

2. **Apply Migrations**: Apply the database migrations using:

    ```bash
    python manage.py migrate
    ```

3. **Run the Development Server**: Start the Django development server:

    ```bash
    python manage.py runserver
    ```

4. **Access the Admin Panel**: Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser. Log in with the superuser credentials provided below to access the admin interface.

### Superuser Credentials

- **Phone Number**: `0987654321`
- **Password**: `super@123`

## Test Cases

Test cases are included in each of apps to ensure the functionality and reliability of the API endpoints. To run the test cases, use:

```bash
python manage.py test
