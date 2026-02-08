# Todo List App

#### Video Demo: <[https://youtu.be/kyDo1qXCt0E](https://youtu.be/kyDo1qXCt0E)>

#### Description:

I built this todo list web application as my CS50 final project. The idea was simple - I wanted to create something I'd actually use daily. A place where I can dump all my tasks, track what I'm working on, and feel that satisfaction of marking things complete.

## What I Built

This is a full-stack web app where users can register, login, and manage their personal todo lists. Each user has their own private space. You can't see my todos, and I can't see yours.

The main features include:
- Creating todos with titles and goal descriptions
- Tracking status (incomplete, in progress, complete)
- Editing and deleting todos
- Filtering todos by their status
- A simple dashboard showing how many tasks are in each category

## What I Used and Why

### Flask (Python Web Framework)

I chose Flask because it's beginner-friendly but powerful enough for real projects. Unlike Django, Flask doesn't force you into a specific structure. I got to decide how to organize my code, which helped me understand how web apps actually work under the hood.

### Flask-SQLAlchemy (Database)

This handles all my database stuff. Instead of writing raw SQL queries, I work with Python classes. I created two models - User and Todo. SQLAlchemy translates my Python code into SQL automatically. The actual database is SQLite, which is just a simple file. No complicated setup needed.

### Flask-Login (Authentication)

This library handles user sessions. It remembers who's logged in, protects pages from unauthorized access, and manages the whole login/logout flow. Without it, I'd have to write a lot of security code myself, which is risky for a beginner.

### Flask-WTF (Forms)

Forms are tricky. Users can submit anything, including malicious code. Flask-WTF validates all input and protects against CSRF attacks (where bad websites try to submit forms on your behalf). It made handling registration, login, and todo forms much safer and cleaner.

### Bootstrap 5 (Frontend)

I'm not a designer. Bootstrap gave me a decent-looking interface without writing much CSS. The app is responsive too, meaning it works on phones and tablets, not just desktops.

### Werkzeug (Password Security)

Storing passwords as plain text is a terrible idea. Werkzeug hashes passwords before saving them. Even if someone steals my database, they can't see actual passwords. When users login, it compares hashes, not the original passwords.

## Project Structure
todo-app/
├── app/
│ ├── init.py # Creates and configures the Flask app
│ ├── models.py # Database tables (User and Todo)
│ ├── forms.py # Form definitions and validation
│ ├── routes.py # All the URL endpoints and logic
│ └── templates/ # HTML pages
├── config.py # App settings (secret key, database path)
├── run.py # Starts the server

## How It Works

When you first visit, you'll see a login page. New users register with username, email, and password. After logging in, you land on your todo dashboard. It shows stats at the top - how many todos total and in each status.

Click "Add New Todo" to create a task. Give it a title and optionally describe your goal. Pick a status and save. Your todos appear as cards. Each card has quick buttons to change status with one click. You can also edit details or delete todos you no longer need.

The filter buttons let you focus on specific categories. Want to see only what's in progress? One click.
