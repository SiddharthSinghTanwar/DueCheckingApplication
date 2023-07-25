from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Configuration (you can load it from an external config.py file)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# Define routes and views
@app.route('/')
def home():
    # Fetch user details from the database (if applicable)
    user_details = {
        'name': 'John Doe',
        'address': '123 Main St, City',
        'mobile': '123-456-7890',
        'enrollment_id': 'ABCDE123',
        'course_name': 'Computer Science'
    }
    return render_template('home.html', user_details=user_details)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login form submission and authentication logic
    if request.method == 'POST':
        # Process the login form data
        # Check credentials, validate the user, and handle sessions
        return redirect('/home')  # Redirect to the home page after successful login
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle registration form submission and user creation logic
    if request.method == 'POST':
        # Process the registration form data
        # Save the new user details to the database
        return redirect('/login')  # Redirect to the login page after successful registration
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
