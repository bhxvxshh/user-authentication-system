# user-authentication-system
A Flask-based user authentication system featuring registration, login, and admin approval. It includes email verification, password hashing with bcrypt, and an admin dashboard for managing user approvals. The project uses MySQL for the database and SMTP for email notifications.
# User Authentication System

A Flask-based user authentication system with features like registration, login, and admin approval. It includes email verification, password hashing with bcrypt, and an admin dashboard to manage user approvals. The system is backed by a MySQL database and uses SMTP for email notifications.

## Features

- **User Registration**: New users can register by providing a name, email, and password. Passwords are securely hashed using bcrypt.
- **Admin Approval**: After registration, the admin receives an email with a verification link to approve or reject the user.
- **Login**: Users can log in with their registered email and password.
- **Admin Dashboard**: Admins can view and manage all users, approving or rejecting them based on their registration status.
- **Email Notifications**: Admins are notified by email when a new user registers, with a link to approve the user.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Bcrypt (for password hashing)
- **Email**: SMTP (for sending email notifications)
- **Frontend**: HTML, CSS (via Flask templates)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/bhxvxshh/user-authentication-system.git
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up your MySQL database and update the db_config in the app.py with your MySQL credentials.

Create the required tables in your MySQL database using the following queries:

sql
Copy code
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    registration_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending'
);
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255)
);
Set up your SMTP email configuration (replace with your email details in app.py).

Run the Flask app:

bash
Copy code
python app.py
Open your browser and navigate to http://localhost:5000 to see the app in action.

License
This project is licensed under the MIT License - see the LICENSE file for details.

javascript
Copy code

This `README.md` includes installation instructions, usage, and setup steps for your project.
