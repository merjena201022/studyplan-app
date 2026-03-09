from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'study_green_secret' # Required for login sessions
DATA_FILE = 'data.json'
USER_FILE = 'users.json' # Separate file to store users

# --- AUTH FUNCTIONS ---
def load_users():
    if not os.path.exists(USER_FILE): return {"admin": "password123"}
    with open(USER_FILE, 'r') as f:
        try: return json.load(f)
        except: return {"admin": "password123"}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# --- LOGIN/REGISTER ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        return "Invalid Login! Try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            return "User already exists!"
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# --- YOUR ORIGINAL CODE (UNCHANGED LOGIC) ---
def load_tasks():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    # Only allow access if logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks, user=session['user'])

@app.route('/add', methods=['POST'])
def add_task():
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1 if tasks else 1,
        "name": request.form.get('name'),
        "details": request.form.get('details'),
        "deadline": request.form.get('deadline'),
        "priority": request.form.get('priority'),
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/check/<int:task_id>')
def check(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = not t['completed']
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)