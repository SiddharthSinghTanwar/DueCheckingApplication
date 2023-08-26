import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from nodues import app, db, bcrypt
from nodues.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminLogin
from nodues.models import User
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import random
import string
from flask_mail import Message
from nodues import mail

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    random_password = ''.join(random.choice(characters) for _ in range(length))
    return random_password


due_records = [
    {
        'enrollment_no': '007',
        'hostel_fees': 0,
        'tuition_fees': 0,
        'other_fees': 0,
        'library': 100
    },
    {
        'enrollment_no': '101',
        'hostel_fees': 0,
        'tuition_fees': 0,
        'other_fees': 100,
        'library': 0
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', due_records=due_records, title='Dashboard')


@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html', title='Admin-Home')

# Route to handle the search form submission
@app.route('/search_results', methods=['POST'])
def search_results():
    enrollment = request.form.get('enrollment')
    batch = request.form.get('batch')
    course = request.form.get('course')

    # Query the database based on the search criteria
    search_results = User.query.filter_by(enrollment_no=enrollment, batch=batch, course=course).all()

    return render_template('search_results.html', search_results=search_results)

# Route to handle the file upload
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        if 'excelFile' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        excel_file = request.files['excelFile']

        if excel_file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if excel_file and excel_file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(excel_file)

            # From the User model defined
            for index, row in df.iterrows():
                user = User(enrollment_no=row['Enrollment No'], username=row['Username'], email=row['Email'], course=row['Course'], batch=row['Batch'], address=row['Address'])
                # Add 'user' to the database
                db.session.add(user)
            db.session.commit()

            flash('File uploaded and data added to the database.', 'success')
            return redirect(url_for('admin_home'))
        
        flash('Invalid file format.', 'danger')
        
    return render_template('upload.html', title='Upload')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print(form.errors)
    if request.method == "POST":
        if form.validate_on_submit():
            # Generate a random password
            random_password = generate_random_password()

            hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, enrollment_no=form.enrollment_no.data, course=form.course.data, batch=form.batch.data, address=form.address.data)
            db.session.add(user)
            db.session.commit()

            # Send the random password to the user's email
            msg = Message("Your Registration Details", recipients=[form.email.data], sender="siddh12tanwar@gmail.com")
            msg.body = f"Hello {form.username.data},\n\nYour registration is successful!\n\nYour password is: {random_password}\n\nYou can now log in with this password and change it later."
            mail.send(msg)

            flash(f'Account created for {form.username.data}! Please check your email for the password.', 'success')

    return render_template('register.html', title='Register', form=form)

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = AdminLogin()
    form.email.data = 'admin@master.com'
    if form.validate:
        if request.method == 'POST':
            if form.email.data == 'admin@master.com' and form.password.data == 'password':
                return redirect(url_for('admin_home'))
            else:
                flash('Invalid credentials!', 'danger')
    return render_template('admin.html', title='Admin', form=form)



@app.route("/student_login", methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('student_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('student_login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.enrollment_no = form.enrollment_no.data
        current_user.course = form.course.data
        current_user.batch = form.batch.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.enrollment_no.data = current_user.enrollment_no
        form.course.data = current_user.course
        form.batch.data = current_user.batch
        form.address.data = current_user.address
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/faculty_login")
def faculty_login():
    return render_template('faculty_home.html')

@app.route("/alumini_login")
def alumini_login():
    return render_template('alumini_home.html')