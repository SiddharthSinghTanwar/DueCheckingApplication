from flask import render_template, url_for, flash, redirect, request
from nodues import app, db, bcrypt
from nodues.forms import RegistrationForm, LoginForm, UpdateAccountForm
from nodues.models import User
from flask_login import login_user, current_user, logout_user, login_required


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

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print(form.errors)
    if request.method == "POST":
        if form.validate_on_submit():
            print("Validated")
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, enrollment_no=form.enrollment_no.data, course=form.course.data, batch=form.batch.data, address=form.address.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
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
