# kudo-backend-service
This backend service manages user recognition by tracking and controlling weekly kudos distribution within organizations, enabling users to give and receive appreciation with personalized messages.

---

## How to Run the Application

1. **Install dependencies**  
   Make sure you have Python 3 and Django installed.  
   Install requirements (if you have a `requirements.txt`):
   ```
   pip install -r requirements.txt
   ```

2. **Apply migrations**  
   Create the necessary database tables:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create dummy data for testing**  
   Open the Django shell:
   ```
   python manage.py shell
   ```
   Then run the following in the shell:
   ```python
   from kudos_app.models import Organization, User, Kudo
   from django.contrib.auth.hashers import make_password

   # Create organizations
   org1 = Organization.objects.create(name="Alpha Org")
   org2 = Organization.objects.create(name="Beta Org")

   # Create users
   user1 = User.objects.create(username="alice", password=make_password("pass"), first_name="Alice", last_name="Anderson", email="alice@example.com", organization=org1)
   user2 = User.objects.create(username="bob", password=make_password("pass"), first_name="Bob", last_name="Brown", email="bob@example.com", organization=org1)
   user3 = User.objects.create(username="carol", password=make_password("pass"), first_name="Carol", last_name="Clark", email="carol@example.com", organization=org2)
   user4 = User.objects.create(username="dave", password=make_password("pass"), first_name="Dave", last_name="Davis", email="dave@example.com", organization=org1)
   user5 = User.objects.create(username="eve", password=make_password("pass"), first_name="Eve", last_name="Evans", email="eve@example.com", organization=org2)
   user6 = User.objects.create(username="frank", password=make_password("pass"), first_name="Frank", last_name="Foster", email="frank@example.com", organization=org2)
   user7 = User.objects.create(username="grace", password=make_password("pass"), first_name="Grace", last_name="Green", email="grace@example.com", organization=org1)

   # Create kudos
   Kudo.objects.create(kudos_from=user1, kudos_to=user2, message="Great teamwork!")
   Kudo.objects.create(kudos_from=user2, kudos_to=user1, message="Thanks for your help!")
   Kudo.objects.create(kudos_from=user3, kudos_to=user1, message="Well done on the project!")
   ```
   Exit the shell.

4. **Run the development server**
   ```
   python manage.py runserver
   ```

---

## Kudos App API Endpoints

All endpoints are prefixed with `/kudos/`.

### 1. Give Kudos
- **Endpoint:** `POST /kudos/give-kudos/`
- **Query Params:** `user-id: <kudos_from_user_id>`
- **Body:**
  ```json
  {
    "kudos_to_id": <kudos_to_user_id>,
    "message": "Your message here"
  }
  ```

### 2. List Received Kudos
- **Endpoint:** `GET /kudos/received-kudos/`
- **Query Params:** `user-id: <user_id>`

### 3. List Given Kudos
- **Endpoint:** `GET /kudos/given-kudos/`
- **Query Params:** `user-id: <user_id>`

---

## Creating Test Data for Login - This is just for reference(No need to run these steps)

To test the login functionality, you need at least one user in the database.  
You can use the shell steps above or create a user like this:

```python
from auth_app.models import User
from kudos_app.models import Organization

org = Organization.objects.create(name="Test Org")
user = User.objects.create(
    username="testuser",
    password="testpass",  # For demo only
    first_name="Test",
    last_name="User",
    email="testuser@example.com",
    organization=org
)
print(user.id)
```

You can now use these credentials to authenticate via the `/api/auth/login` endpoint.

---

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