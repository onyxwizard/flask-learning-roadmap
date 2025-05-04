# 🔐 Cybersecurity Knowledge Base - Dockerized Flask API

A RESTful Flask API for managing cybersecurity entries — built with:

- 🔐 JWT Authentication  
- 📄 CRUD operations (via web & JSON API)  
- 🔧 Docker support  
- 🛡️ User roles and permissions  
- 💾 SQLite database  

This is the **dockerized version** of the [Cybersecurity Knowledge Base](https://github.com/onyxwizard/flask-learning-roadmap) Flask app.



## 🧩 Features

| Feature | Description |
|--------|-------------|
| ✅ Web Interface | HTML pages for browsing and editing entries |
| 🌐 REST API | `/api/entries`, `/api/login`, JWT-protected |
| 🔒 JWT Authentication | Secure login system using `flask-jwt-extended` |
| 👤 Admin Role | Restrict access to certain users |
| 🧱 Docker Support | Containerized app ready for deployment |
| 🧪 Easy Development | Live reload via volume mounting |
| 📦 Lightweight | Uses Python slim base image |



## 📁 Folder Structure

```
flask-cyber-kb/
├── app/
│   ├── __init__.py       # App factory + extensions
│   ├── models.py           # Entry & User models
│   ├── routes.py           # Web routes (HTML pages)
│   └── api.py              # Flask-RESTful API resources
├── static/
│   └── css/
│       └── style.css       # CSS styling
├── templates/
│   ├── add_entry.html
│   ├── edit_entry.html
│   ├── index.html
│   ├── login.html
│   └── register.html
├── main.py                 # Flask entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Build instructions
├── docker-compose.yml      # Multi-container setup
└── README.md               # This file 🎉
```



## 🛠️ Setup Instructions

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/onyxwizard/flask-cyber-kb.git
cd flask-cyber-kb
```



### 2. 🧰 Install Dependencies (Optional for Dev)

If you want to run locally without Docker:

```bash
pip install -r requirements.txt
```



### 3. ⚙️ Build the Docker Image

```bash
docker build -t flask-cyber-kb .
```



### 4. 🚀 Run the App in Docker

Start the container:

```bash
docker run -p 5000:5000 -v $(pwd):/app flask-cyber-kb
```

> On Windows PowerShell:
```powershell
docker run -d -p 5000:5000 --name flask-app flask-cyber-kb
```



### 5. 🌐 Access the App

Visit:
```
http://localhost:5000
```

You should see the homepage listing all entries.



## 🔄 Or Use Docker Compose

If you're using `docker-compose.yml`, just run:

```bash
docker-compose up --build
```



## 🔗 Endpoints

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| GET    | `/`                     | Homepage with all entries       |
| POST   | `/login`                | Log in via web form             |
| GET    | `/register`             | Register new user               |
| POST   | `/api/login`            | Authenticate and get JWT token  |
| GET    | `/api/entries`          | Get all entries (JSON)          |
| POST   | `/api/entries`          | Create new entry (JWT required) |
| GET    | `/api/entries/<id>`     | Get one entry by ID              |
| PUT    | `/api/entries/<id>`     | Update an entry (JWT required)   |
| DELETE | `/api/entries/<id>`     | Delete an entry (JWT required)   |



## 🔑 Example: Login and Add Entry via API

### 🔐 Step 1: Get a Token

```bash
curl -X POST http://localhost:5000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin", "password":"admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx"
}
```

### 📦 Step 2: Use Token to Add Entry

```bash
curl -X POST http://localhost:5000/api/entries \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx" \
     -H "Content-Type: application/json" \
     -d '{"title":"XSS", "category":"Vulnerabilities", "content":"Cross-site scripting.", "user_id":1}'
```



## 🧪 Testing Tips

Use tools like:
- 🐢 **Postman**
- ⚡ **Thunder Client (VS Code extension)**
- 📦 **curl**

To test endpoints and headers.



## 📦 Optional: Push to Docker Hub

Want others to pull your image easily?

### 1. Tag Your Image

```bash
docker tag flask-cyber-kb your-dockerhub-user/flask-cyber-kb
```

### 2. Push to Docker Hub

```bash
docker push your-dockerhub-user/flask-cyber-kb
```

Now anyone can use:

```bash
docker pull your-dockerhub-user/flask-cyber-kb
```



## 📝 Notes on Security

- 🔐 `JWT_SECRET_KEY` should be changed before production.
- 🛡️ Avoid running in debug mode (`debug=True`) in production.
- 📊 Consider switching from SQLite to PostgreSQL or MySQL when deploying.



## 🧱 Want to Contribute?

Feel free to fork this repository and contribute improvements!

### Ideas:
- 🔍 Add search/filter functionality
- 📊 Build a dashboard
- 📦 Add Redis caching
- 📖 Generate Swagger/OpenAPI docs
- 🧬 Implement refresh tokens


## 💬 Contact

Got questions or feedback? Feel free to reach out:

- 🐙 [GitHub](https://github.com/onyxwizard)
- 🐳  [Docker hub](https://hub.docker.com/u/onyxwizard)



## 🎉 Thank You!

Thank you for exploring this project! If you found it helpful, please give it a ⭐ on GitHub. Happy coding! 😎



## 🚀 Future Roadmap (Optional)

Would you like me to help you:
- Add **Swagger/OpenAPI documentation**
- Set up **GitHub Actions CI/CD**
- Deploy to **Render**, **Railway**, or **Heroku**
- Add **unit tests**
- Migrate to **FastAPI** for production-ready APIs

Let me know how you'd like to continue! 😊