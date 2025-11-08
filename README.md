# kudo-backend-service
This backend service manages user recognition by tracking and controlling weekly kudos distribution within organizations, enabling users to give and receive appreciation with personalized messages.


## Login Functionality

We have implemented a simple login API endpoint at `/api/auth/login` using Django REST Framework.  
- The endpoint accepts a POST request with `username` and `password` in the request body.
- The backend checks the credentials against the `User` model (defined in `auth_app`).
- If the credentials are valid, the API returns the user's ID and username.
- For demonstration purposes, passwords are stored in plaintext. **(Do not use this approach in production.)**

**Example request:**
```json
POST /api/auth/login
{
  "username": "testuser",
  "password": "testpass"
}
```

## Creating Test Data for Login

To test the login functionality, you need at least one user in the database.  
