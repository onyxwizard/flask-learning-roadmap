
# 🚀 Cybersecurity Knowledge Base - RESTful API

Welcome to the **Cybersecurity Knowledge Base RESTful API**! This project builds upon the [Flask Basics](https://github.com/onyxwizard/flask-learning-roadmap/tree/main/flask-basics) project by adding a **RESTful API layer** using Flask-RESTful. It allows you to manage cybersecurity entries via JSON endpoints while keeping the existing web interface intact.



## 🌟 Features

- **Web Interface**: Still accessible via HTML pages (`templates/`)
- **RESTful API**: Exposes CRUD operations for entries
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **User Roles**: Supports admin users for enhanced permissions
- **Entry Ownership**: Only owners or admins can edit/delete entries
- **SQLite Database**: Stores entries and user data securely



## 🛠️ Folder Structure

```
flask-api/
├── instance/
│   └── knowledge_base.db  # SQLite database file
├── static/
│   ├── css/
│   │   └── style.css      # CSS styles for web interface
│   └── js/
│       └── ...            # JavaScript files (if any)
├── templates/
│   ├── add_entry.html     # Add entry form
│   ├── base.html          # Base template for HTML pages
│   ├── edit_entry.html    # Edit entry form
│   ├── index.html         # Homepage listing entries
│   ├── login.html         # Login page
│   └── register.html      # User registration page
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy models for Entries and Users
├── requirements.txt       # Project dependencies
└── README.md              # This file
```



## 🏃‍♂️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flask-api.git
cd flask-api
```

### 2. Install Dependencies

Make sure you have Python installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

Delete the old `knowledge_base.db` file if you're starting fresh:

```bash
rm instance/knowledge_base.db
```

Run the app to recreate the database:

```bash
python app.py
```

This will create a new SQLite database with tables for `Entries` and `Users`.

### 4. Start the Server

```bash
python app.py
```

Your app will run on `http://127.0.0.1:5000/`.



## 🔗 Endpoints

The API exposes the following endpoints:

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| GET    | `/api/entries`          | Get all entries (JSON response) |
| POST   | `/api/entries`          | Create a new entry             |
| GET    | `/api/entries/<id>`     | Get one entry by ID            |
| PUT    | `/api/entries/<id>`     | Update an entry                |
| DELETE | `/api/entries/<id>`     | Delete an entry                |
| POST   | `/api/login`            | Authenticate user & get token   |

### Example: Login and Access API

1. **Login**:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/login \
        -H "Content-Type: application/json" \
        -d '{"username":"admin", "password":"admin123"}'
   ```

   Response:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx.yyyyy"
   }
   ```

2. **Add Entry**:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/entries \
        -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx.yyyyy" \
        -H "Content-Type: application/json" \
        -d '{"title":"SQL Injection", "category":"Vulnerabilities", "content":"Malicious SQL input.", "user_id":1}'
   ```

   Response:
   ```json
   {
     "message": "Entry created",
     "id": 1
   }
   ```



## 📝 Updates from `flask-basic` to `flask-api`

Here's a detailed list of changes made to transform the `flask-basic` project into a full-fledged RESTful API:

### 1. **Added Flask-RESTful**

- Installed `Flask-RESTful` via `requirements.txt`.
- Created API resources for managing entries:
  - `EntryListResource` for `/api/entries`
  - `EntryResource` for `/api/entries/<id>`
  - `ApiLoginResource` for `/api/login`

### 2. **Implemented JWT Authentication**

- Added `Flask-JWT-Extended` for secure API access.
- Modified `/api/login` to return JWT tokens.
- Protected API routes with `@jwt_required()` decorator.

### 3. **Updated Models**

- Moved models (`Entry`, `User`) to `models.py` for better organization.
- Added `is_admin` field to the `User` model for role-based access control.

### 4. **Enhanced Security**

- Replaced plain-text passwords with hashed passwords using `werkzeug.security`.
- Implemented token expiration (`JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)`).

### 5. **Kept Existing Web Interface**

- Retained all HTML templates (`templates/`) and routes for the web interface.
- Ensured both web and API functionality coexist seamlessly.

### 6. **Improved File Structure**

- Organized files into logical directories:
  - `static/` for assets (CSS, JS, images).
  - `templates/` for HTML templates.
  - `models.py` for database models.
  - `app.py` for main application logic.



## 🧪 Testing the API

You can test the API using tools like:
- **curl**
- **Postman**
- **Thunder Client** (VS Code extension)

### Example: Test All Endpoints

1. **Get All Entries**:
   ```bash
   curl http://127.0.0.1:5000/api/entries
   ```

2. **Create a New Entry**:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/entries \
        -H "Authorization: Bearer YOUR_JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"title":"XSS", "category":"Vulnerabilities", "content":"Cross-site scripting.", "user_id":1}'
   ```

3. **Update an Entry**:
   ```bash
   curl -X PUT http://127.0.0.1:5000/api/entries/1 \
        -H "Authorization: Bearer YOUR_JWT_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"title":"Updated XSS", "category":"Vulnerabilities", "content":"Modified description."}'
   ```

4. **Delete an Entry**:
   ```bash
   curl -X DELETE http://127.0.0.1:5000/api/entries/1 \
        -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```



## 🚀 Next Steps

- **Add Swagger/OpenAPI Documentation**: Use tools like `flasgger` or `connexion` to generate API docs.
- **Build a Frontend**: Develop a React or Vue.js frontend to consume the API.
- **Deploy to Production**: Host your app on platforms like Render, Railway, or Heroku.
- **Enhance Security**: Implement refresh tokens, rate limiting, or HTTPS.



## 🤝 Contributing

Feel free to fork this repository and contribute improvements! Here are some ideas:
- Add more security features.
- Enhance the UI/UX.
- Introduce search/filter functionality.
- Support multi-user collaboration.



## ⚙️ Credits

- **Flask**: The Python microframework powering this project.
- **Flask-RESTful**: Simplifies building REST APIs.
- **Flask-JWT-Extended**: Handles JWT authentication securely.
- **Flask-SQLAlchemy**: Manages database interactions elegantly.


## 📄 License

This project is open-source under the [MIT License](LICENSE).



## 💌 Contact

If you have questions or feedback, feel free to reach out:
- [Medium](https://onyxwizard.medium.com)
- [GitHub](https://github.com/onyxwizard)


## 🎉 Happy Coding!

Thank you for exploring this project! If you found it helpful, consider giving it a star ⭐ on GitHub. 😊