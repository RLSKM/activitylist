from flask import Flask, render_template, redirect, request, url_for, flash
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("info.db")
cursor = conn.cursor()

@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")
    
@app.route('/home/<username>', methods=['POST'])
def home(username):
    return render_template("index.html")


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
        has_digit = False
        has_upper = False
        has_lower = False
        has_special = False
        if password == confirm_password:  #checks if passwords match
            for char in password:
                if char.isdigit():
                    has_digit = True
                if char.isalpha():
                    if char.isupper():
                        has_upper = True
                    if char.islower():
                        has_lower = True
                if char in ['@', '#', '$', '%', '/', '*', '^', '&', '?', '!']:
                    has_special = True
            if not has_digit:
                alert = "Password lacks a digit"
            elif not has_upper:
                alert = "Password lacks an uppercase letter"
            elif not has_lower:
                alert = "Password lacks a lowercase letter"
            elif not has_special:
                alert = "Password should include at least one of these characters: @#$%/*^&?!"
            else:
                #password check
                cursor.execute("SELECT * FROM user WHERE password = ?", (password,))
                existing_password = cursor.fetchone()
                if existing_password:  #if value not None, flash username exists
                    flash('Password already exists!')
                else:
                    password_check = True
        else:
            flash('Passwords do not match!')

        #email check
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:  #if value not None, flash username exists
            flash('Email already exists!')
        else:
            email_check = True

        if username_check and password_check and email_check:
            #inputs information into database, redirects to login page
            cursor.execute("""
           INSERT INTO user (first_name, last_name, username, email, password)
            VALUES (?, ?, ?, ?, ?)""", (first_name, last_name, username, email, password))
            conn.commit()
            return redirect(url_for('login'))
            
    return render_template("register.html", alert=alert)
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
