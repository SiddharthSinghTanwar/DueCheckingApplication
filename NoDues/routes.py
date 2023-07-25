from flask import render_template, url_for, flash, redirect, request
from NoDues import app, db, bcrypt
from NoDues.forms import RegistrationForm, LoginForm
from NoDues.models import User, Nodue
from flask_login import login_user, current_user, logout_user, login_required

with app.app_context():
    db.create_all()


@app.route('/home')
def home():
    # Fetch user details from the database (if applicable)
    user_details = {
        'name': 'John Doe',
        'address': '123 Main St, City',
        'mobile': '123-456-7890',
        'enrollment_id': '123',
        'course_name': 'Computer Science'
    }
    user_due = {
        'library': 'No Due',
        'exam': 'No Due',
        'tuition': 'No Due',
        'other': 'No Due',
        'hostel': 'No Due',
        'miscellaneous': 'No Due'
    }
    return render_template('home.html', user_details=user_details, user_due=user_due)


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user(user, remember=form.remember.data)
            return redirect('/home')
            # return redirect(url_for('user_profile', user_email=user.email))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(enrollment_no=form.enrollment_no.data, name=form.name.data, email=form.email.data,
                    password=hashed_password, course=form.course.data, batch=form.batch.data, address=form.address.data)
        db.session.add(user)
        db.session.commit()
        flash("Your Account has been created!", "success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/forgot_password")
def forgot_password():
    pass


@app.route('/user/<string:user_email>', methods=['GET', 'POST'])
@login_required
def user_profile(user_email):
    # Fetch user profile data (Replace with actual database queries)

    # actual code for querying data-model do not delete, it will fetch from an actual database (currently empty)
    # will give list index out of range error
    # user_data = User.query.filter_by(email=user_email).first()

    # if user_data:
    #     user_profile_data = user_data.nodue
    #     if request.method == 'POST':
    #         return "Profile action successful."
    #
    #     # Render the specific user profile template for GET request
    #     return render_template('user_profile.html', user=user_profile_data[0], title=f"{user_profile_data[0].name}'s "
    #                                                                                  f"Profile")

    # If user not found, handle error (e.g., redirect to a 404 page)
    return "User not found or profile not available."


@app.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route("/account")
# @login_required
# def account():
#     return render_template('account.html', title='Account')
