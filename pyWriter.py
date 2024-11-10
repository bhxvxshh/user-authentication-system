from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)

#recovery twilio:MKTCSL9DJXV3W9R2UQB16HLL
# Define your database connection parameters
#pass RS5mP-TDr:NAR29
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ADMIN',
    'database': 'auth_login'
}
app.secret_key = 'e1f72a9d4a9f0e9f3f8506f2dfb7f9d1db657baebd24f676'

ADMIN_EMAIL = "dashaccnull@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = 'studentnidharshan@gmail.com'
EMAIL_PASS = 'qgdd hwmu uone yqkw'  # Replace with your email password

@app.route('/register')
def home():
    return render_template('register.html')

@app.route('/register-func', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get data from the HTML form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if confirm_password != password:
            return render_template('register.html', message="Password and Confirm Password don't match. Please try again.")

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        try:
            # Check if the email already exists in the database
            select_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            existing_user = cursor.fetchone()  # Fetch the result of the query

            if existing_user:
                # If user exists, show a message on the registration page
                return render_template('register.html', message="User already exists. Please try another email.")
            
            # If the email doesn't exist, proceed with registration

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user with 'pending' registration status
            insert_query = """
            INSERT INTO users (username, email, password, registration_status) 
            VALUES (%s, %s, %s, 'pending')
            """
            data = (name, email, hashed_password)
            cursor.execute(insert_query, data)
            connection.commit()

            # Send verification email to admin
            send_verification_email(name, email)

            # Redirect to the registration page with a success message
            return render_template('register.html', message="Registration successful! Awaiting admin approval.", button_text="Go to Login Page", button_link="/login")
        
        except Exception as e:
            print(e)
            return render_template('register.html', message="Registration failed. Please try again.", button_text="Retry Registration", button_link="/register")
        
        finally:
            cursor.close()
            connection.close()

def send_verification_email(username, user_email):
    """Send an email to the admin with a verification link for the new user."""
    verification_link = f"http://localhost:5000/verify-user?email={user_email}"
    subject = "New User Registration Approval"
    
    # Email content
    message = MIMEMultipart()
    message["From"] = EMAIL_USER
    message["To"] = ADMIN_EMAIL
    message["Subject"] = subject
    
    body = f"""
    A new user has registered with the following details:
    
    Username: {username}
    Email: {user_email}
    
    Please click the link below to approve this user:
    <a href="{verification_link}">Verify User</a>
    """
    
    message.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(message)
            print("Verification email sent to admin.")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/verify-user')
def verify_user():
    """Route to verify and approve a user."""
    user_email = request.args.get('email')

    if not user_email:
        return "Invalid request."

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Update user's registration status to 'approved'
        update_query = "UPDATE users SET registration_status = 'approved' WHERE email = %s"
        cursor.execute(update_query, (user_email,))
        connection.commit()

        return "User approved successfully."
    
    except Exception as e:
        print(f"Error approving user: {e}")
        return "Failed to approve user."
    
    finally:
        cursor.close()
        connection.close()



    
@app.route('/login-func', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Fetch data as dictionary
        
        try:
            # Fetch user details from the database using email
            select_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(select_query, (email,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    # Render a page for a successful login (e.g., display user profile)
                    return render_template('display.html', user=user)
                else:
                    # Invalid password error message
                    flash("Invalid password. Please try again.", "error")
                    return redirect(url_for('login'))
            else:
                # User does not exist error message
                flash("User does not exist. Please check your email or register.", "error")
                return redirect(url_for('login'))  # Redirect to login page

        except mysql.connector.Error as db_error:
            print(f"Database error: {db_error}")
            flash("Database error occurred. Please try again.", "error")
            return redirect(url_for('login'))  # Redirect to login page

        except Exception as e:
            print(f"Unexpected error: {e}")
            flash("An unexpected error occurred. Please try again.", "error")
            return redirect(url_for('login'))  # Redirect to login page

        finally:
            cursor.close()
            connection.close()

    # Render the login page with any error messages
    return render_template('login.html')


@app.route('/ad-login-func', methods=['GET', 'POST'])
def ad_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Fetch data as dictionary
        
        try:
            # Fetch admin details from the database using email
            select_query = "SELECT * FROM admins WHERE username = %s"
            cursor.execute(select_query, (email,))
            user = cursor.fetchone()

            if user:
                stored_hashed_password = user['password']
                if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                    # Fetch all users (not just those pending approval)
                    fetch_users_query = "SELECT * FROM users"
                    cursor.execute(fetch_users_query)
                    all_users = cursor.fetchall()

                    # Render the admin dashboard with all users
                    return render_template('admin-dashboard.html', user=user, users=all_users)
                else:
                    # Invalid password error message
                    flash("Invalid password. Please try again.", "error")
            else:
                # User does not exist error message
                flash("User does not exist.", "error")

        except mysql.connector.Error as db_error:
            print(f"Database error: {db_error}")
            flash("Database error occurred. Please try again.", "error")

        except Exception as e:
            print(f"Unexpected error: {e}")
            flash("An unexpected error occurred. Please try again.", "error")

        finally:
            cursor.close()
            connection.close()

    # Render the admin login page with any error messages
    return render_template('admin-login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Fetch all users, not just those pending approval
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return render_template('admin-dashboard.html', users=users)
    
    except Exception as e:
        print(f"Error fetching users: {e}")
        return render_template('admin-dashboard.html', message="Error fetching users.")
    
    finally:
        cursor.close()
        connection.close()

# Route to approve a user
@app.route('/approve-user/<user_email>', methods=['GET'])
def approve_user(user_email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        update_query = "UPDATE users SET registration_status = 'approved' WHERE email = %s"
        cursor.execute(update_query, (user_email,))
        connection.commit()

        flash(f"User {user_email} has been approved.", "success")
        return redirect(url_for('admin_dashboard'))

    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        flash("Database error occurred. Could not approve user.", "error")
        return redirect(url_for('admin_dashboard'))

    finally:
        cursor.close()
        connection.close()

@app.route('/reject-user/<user_email>', methods=['GET'])
def reject_user(user_email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        update_query = "UPDATE users SET registration_status = 'rejected' WHERE email = %s"
        cursor.execute(update_query, (user_email,))
        connection.commit()

        flash(f"User {user_email} has been rejected.", "warning")
        return redirect(url_for('admin_dashboard'))

    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        flash("Database error occurred. Could not reject user.", "error")
        return redirect(url_for('admin_dashboard'))

    finally:
        cursor.close()
        connection.close()

@app.route('/logout')
def logout():
    # Log out the user and redirect to home page
    return redirect(url_for('home'))

@app.route('/adlogout')
def adlogout():
    # Any necessary cleanup (e.g., clearing sessions) can be done here
    flash("Logged out successfully.", "success")  # Optional flash message
    return redirect(url_for('ad_login'))  # Redirect to the admin login page


@app.route('/')
def back():
    return render_template('index.html')

@app.route('/login')
def user_log():
    return render_template('login.html')


@app.route('/ad-login')
def admin_login():
    return render_template('admin-login.html')

if __name__ == '__main__':
    app.run(debug=True)