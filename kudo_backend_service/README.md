# kudo-backend-service
This backend service manages user recognition by tracking and controlling weekly kudos distribution within organizations, enabling users to give and receive appreciation with personalized messages.

---

## How to Run the Application

## Navigate into the project

   ```
   cd kudo_backend_service
   ```

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

   ## Populate the database (recommended)

      After running migrations, use the provided management command to seed sample organizations, users and kudos (idempotent and hashes passwords correctly):

      Give your db details in .env file (change the details accordingly)
      DB_ENGINE=django.db.backends.postgresql
      DB_NAME=kudos_db
      DB_USER=postgres
      DB_PASSWORD=root
      DB_HOST=localhost
      DB_PORT=5432

      Windows / Terminal:
      ```bash
      python manage.py makemigrations
      python manage.py migrate

      python manage.py shell

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
      ```
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

