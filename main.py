from flask import Flask, render_template, redirect, request, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'WHYISTHISSOHARDAHHHHHHHHH'

conn = sqlite3.connect("info.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
cursor = conn.cursor()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()s
        
        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out")
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("Please log in first")
        return redirect(url_for('login'))
    
    search = request.args.get('search')
    if search:
        search_query = "%" + search.lower() + "%"
        cursor.execute("SELECT name, description FROM Activity WHERE LOWER(name) LIKE ? ORDER BY name", (search_query,))

    else:
        cursor.execute("SELECT name, description FROM Activity ORDER BY name")
        search = ""
        
    activities = cursor.fetchall()
    
    # Get the page, default is 1
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Calculate start and end indexes for slicing the list
    start = (page - 1) * per_page
    end = start + per_page

    displayed_activities = activities[start:end]
    
    # Determine the total number of pages
    total_pages = (len(activities) + per_page - 1) // per_page  #ensures that page rounds up

    return render_template("index.html", search=search, activities=displayed_activities, page=page, total_pages=total_pages)

@app.route('/activitypage/<activity>')
def activitypage(activity):
    cursor.execute("SELECT activity.name, activity.description FROM activity WHERE activity.name = ?", (activity,))
    activity = cursor.fetchone()
    if activity:
        activity_details = {
            'name': activity['name'],
            'description': activity['description'],
            'rating': activity['rating']
        }
        return render_template('activitypage.html', activity=activity_details)
    else:
        return "Activity not found", 404

#registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    alert = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        username_check = False
        password_check = False
        email_check = False
        
        #username check
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_username = cursor.fetchone()
        if existing_username:  #if value not None, flash username exists
            flash('Username already exists!')
        else:
            username_check = True
            
        #password validation
        if password == confirm_password:
            if validate_password(password):
                password_check = True
            else:
                flash('Password must contain at least one digit, one uppercase, one lowercase letter, and one special character (@#$%/*^&?!).')
        else:
            flash('Passwords do not match!')

        #email check
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:  #if value not None, flash username exists
            flash('Email already exists!')
        else:
            email_check = True

        if username_check and password_check and email_check:   #inputs information into database, redirects to login page
            cursor.execute("""INSERT INTO user (first_name, last_name, username, email, password)
            VALUES (?, ?, ?, ?, ?)""", (first_name, last_name, username, email, password))
            conn.commit()
            return redirect(url_for('login'))
            
    return render_template("register.html", alert=alert)
            
def validate_password(password):
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_special = any(char in ['@', '#', '$', '%', '/', '*', '^', '&', '?', '!'] for char in password)
    return has_digit and has_upper and has_lower and has_special

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, redirect, request, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'WHYISTHISSOHARDAHHHHHHHHH'

conn = sqlite3.connect("info.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
cursor = conn.cursor()

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        user = cursor.fetchone()s
        
        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out")
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("Please log in first")
        return redirect(url_for('login'))
    
    search = request.args.get('search')
    if search:
        search_query = "%" + search.lower() + "%"
        cursor.execute("SELECT name, description FROM Activity WHERE LOWER(name) LIKE ? ORDER BY name", (search_query,))

    else:
        cursor.execute("SELECT name, description FROM Activity ORDER BY name")
        search = ""
        
    activities = cursor.fetchall()
    
    # Get the page, default is 1
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Calculate start and end indexes for slicing the list
    start = (page - 1) * per_page
    end = start + per_page

    displayed_activities = activities[start:end]
    
    # Determine the total number of pages
    total_pages = (len(activities) + per_page - 1) // per_page  #ensures that page rounds up

    return render_template("index.html", search=search, activities=displayed_activities, page=page, total_pages=total_pages)

@app.route('/activitypage/<activity>')
def activitypage(activity):
    cursor.execute("SELECT activity.name, activity.description FROM activity WHERE activity.name = ?", (activity,))
    activity = cursor.fetchone()
    if activity:
        activity_details = {
            'name': activity['name'],
            'description': activity['description'],
            'rating': activity['rating']
        }
        return render_template('activitypage.html', activity=activity_details)
    else:
        return "Activity not found", 404

#registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    alert = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        username_check = False
        password_check = False
        email_check = False
        
        #username check
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        existing_username = cursor.fetchone()
        if existing_username:  #if value not None, flash username exists
            flash('Username already exists!')
        else:
            username_check = True
            
        #password validation
        if password == confirm_password:
            if validate_password(password):
                password_check = True
            else:
                flash('Password must contain at least one digit, one uppercase, one lowercase letter, and one special character (@#$%/*^&?!).')
        else:
            flash('Passwords do not match!')

        #email check
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:  #if value not None, flash username exists
            flash('Email already exists!')
        else:
            email_check = True

        if username_check and password_check and email_check:   #inputs information into database, redirects to login page
            cursor.execute("""INSERT INTO user (first_name, last_name, username, email, password)
            VALUES (?, ?, ?, ?, ?)""", (first_name, last_name, username, email, password))
            conn.commit()
            return redirect(url_for('login'))
            
    return render_template("register.html", alert=alert)
            
def validate_password(password):
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_special = any(char in ['@', '#', '$', '%', '/', '*', '^', '&', '?', '!'] for char in password)
    return has_digit and has_upper and has_lower and has_special

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
