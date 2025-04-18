# 🌟 **Cybersecurity Knowledge Base: Flask Basics**

Welcome to your first Flask project! This repository is designed to help you learn the core concepts of Flask by building a **Cybersecurity Knowledge Base**. The app allows users to add, view, edit, and delete entries about cybersecurity tools, techniques, vulnerabilities, and best practices. Along the way, you'll explore key Flask features like routing, templates, forms, and database integration.



## 📋 Table of Contents
1. [What is Flask?](#what-is-flask)
2. [Core Concepts of Flask](#core-concepts-of-flask)
3. [How Flask is Implemented in This Blog](#how-flask-is-implemented-in-this-blog)
4. [Features of the Cybersecurity Knowledge Base](#features-of-the-cybersecurity-knowledge-base)
5. [Setup Instructions](#setup-instructions)
6. [Folder Structure](#folder-structure)
7. [Resources](#resources)



## 🌟 What is Flask?
Flask is a lightweight and flexible Python web framework that allows you to build web applications quickly and easily. It’s often referred to as a "microframework" because it provides the essentials for web development without imposing too many restrictions. Flask is perfect for beginners and is widely used for building APIs, small websites, and prototypes.



## 🔧 Core Concepts of Flask

### 1. **Routing**
Routing maps URLs to Python functions (views). For example:
```python
@app.route('/')
def index():
    return "Welcome to the Cybersecurity Knowledge Base!"
```
In this project:
- `/` displays the homepage with all entries.
- `/add` lets users create new entries.
- `/edit/<id>` allows users to update an entry.
- `/delete/<id>` removes an entry.

### 2. **Templates**
Flask uses the Jinja2 templating engine to render HTML dynamically. Templates allow you to separate the logic (Python code) from the presentation (HTML). For example:
```html
<h2>{{ entry.title }}</h2>
<p>{{ entry.content }}</p>
```
In this project:
- `index.html` lists all entries.
- `add_entry.html` contains a form to create new entries.
- `edit_entry.html` contains a form to update existing entries.

### 3. **Forms**
Forms are used to collect user input. Flask handles form data via the `request` object:
```python
title = request.form['title']
content = request.form['content']
```
In this project:
- Users can submit forms to add or edit entries.

### 4. **Database Integration**
Flask integrates with databases using extensions like **Flask-SQLAlchemy**. SQLAlchemy is an Object-Relational Mapping (ORM) library that simplifies database interactions. For example:
```python
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
```
In this project:
- SQLite is used as the database.
- Entries are stored in the `Entry` table.

### 5. **Contexts**
Flask uses two types of contexts:
- **Application Context**: Used for app-wide configurations (e.g., database initialization).
- **Request Context**: Used for handling HTTP requests (e.g., accessing form data).



## 🛠️ How Flask is Implemented in This Blog

### 1. **Homepage (`/`)**
The homepage displays all entries in the knowledge base. Flask queries the database and passes the results to the `index.html` template:
```python
@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)
```

### 2. **Adding Entries (`/add`)**
Users can add new entries using a form. Flask processes the form data and saves it to the database:
```python
@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        new_entry = Entry(title=title, category=category, content=content)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_entry.html')
```

### 3. **Editing Entries (`/edit/<id>`)**
Users can update existing entries. Flask retrieves the entry by its ID, updates it with the form data, and saves the changes:
```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = Entry.query.get_or_404(id)
    if request.method == 'POST':
        entry.title = request.form['title']
        entry.category = request.form['category']
        entry.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_entry.html', entry=entry)
```

### 4. **Deleting Entries (`/delete/<id>`)**
Users can delete entries. Flask retrieves the entry by its ID and removes it from the database:
```python
@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))
```



## ✨ Features of the Cybersecurity Knowledge Base
- **View Entries**: Display all cybersecurity tips, tools, and resources on the homepage.
- **Add Entries**: Create new entries with a title, category, and content.
- **Edit Entries**: Update existing entries with new information.
- **Delete Entries**: Remove outdated or irrelevant entries.
- **Categories**: Organize entries into categories like "Tools", "Vulnerabilities", and "Best Practices".



## 🔧 Setup Instructions

### 1. Clone the Repository
If you’re following along, clone the repository and navigate to the `flask-basics` folder:
```bash
git clone https://github.com/yourusername/flask-learning-roadmap.git
cd flask-learning-roadmap/flask-basics
```

### 2. Install Dependencies
Install the required Python packages using `pip`:
```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
```

### 3. Run the App
Start the Flask development server:
```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser to see the app in action.



## 📂 Folder Structure
Here’s the structure of the `flask-basics` folder:
```
flask-basics/
├── app.py                  # Main Flask application file
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage (list of entries)
│   ├── add_entry.html      # Form to add a new entry
│   └── edit_entry.html     # Form to edit an existing entry
├── requirements.txt        # Python dependencies
└── README.md               # Instructions for this module
```



## 📚 Resources
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask Tutorial for Beginners](https://realpython.com/tutorials/flask/)

<center>

### ------------------------------------- Happy Coding! 🌟 -------------------------------------

</center>

