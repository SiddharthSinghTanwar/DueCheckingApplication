import os
import secrets
from io import BytesIO
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, send_file
from nodues import app, db, bcrypt
from nodues.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminLogin, FacultyLogin, ForgotForm, ChangePassword, FacultyRegister, AlumniLogin, AlumniRegister, Posts
from nodues.models import User, DuesEntry, Receipt, Alumni, Notices
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import random
import string
from email.message import EmailMessage
import ssl
import smtplib
from sqlalchemy.exc import OperationalError

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
email_sender = 'noduesproject05@gmail.com'
email_password = 'ndwpzpeefjmzmpjk'
context = ssl.create_default_context()

# notices = {'updates': [], 'events': [], 'jobs': []}

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits
    random_password = ''.join(random.choice(characters) for _ in range(length))
    return random_password

@app.route("/", methods=['GET','POST'])
@app.route("/home", methods=['GET','POST'])
def home():
    updates = Notices.query.filter_by(type='update').all()
    jobs = Notices.query.filter_by(type='job').all()
    events = Notices.query.filter_by(type='event').all()
    return render_template('home.html', updates=updates, jobs=jobs, events=events)

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
            
            em = EmailMessage()
            em['From'] = email_sender
            # Send the random password to the user's email
            email_receiver = form.email.data
            em['To'] = email_receiver
            em['Subject'] = 'Registration details'
            body= f"Hello {form.username.data},\n\nYour registration is successful!\n\nYour password is: {random_password}\n\nYou can now log in with this password and change it later."
            em.set_content(body)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            flash(f'Account created for {form.username.data}! Please check your email for the password.', 'success')
            return redirect(url_for('admin_home'))

        else:
            if 'csvFile' not in request.files:
                flash('No file part', 'danger')
                return redirect(url_for('register'))

            csv_file = request.files['csvFile']

            if csv_file.filename == '':
                flash('No selected file', 'danger')

            if csv_file and csv_file.filename.endswith(('.csv')):
                df = pd.read_csv(csv_file)

                # From the User model defined
                for index, row in df.iterrows():
                    random_password = generate_random_password()

                    hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
                    user = User(enrollment_no=row['Enrollment No'], username=row['Username'], email=row['Email'], password=hashed_password, course=row['Course'], batch=row['Batch'], address=row['Address'])
                    # Add 'user' to the database
                    db.session.add(user)
                    db.session.commit()

                    # Send the random password to the user's email
                    em = EmailMessage()
                    em['From'] = email_sender
                    email_receiver = row['Email']
                    em['To'] = email_receiver
                    em['Subject'] = 'Registration details'
                    body= f"Hello {row['Username']},\n\nYour registration is successful!\n\nYour password is: {random_password}\n\nYou can now log in with this password and change it later."
                    em.set_content(body)
                    
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())

                flash('File uploaded and data added to the database.', 'success')
                return redirect(url_for('admin_home'))
            
            flash('Invalid file format.', 'danger')
        
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

@app.route("/admin_home")
def admin_home():
    # Query users who have applied for no dues
    users = User.query.filter_by(no_dues_applied=True).all()
    return render_template('admin_home.html', title='Admin-Home',users=users)

@app.route("/posts", methods=['GET', 'POST'])
def posts():
    form = Posts()
    if form.validate_on_submit():
        if request.method == 'POST':
            # Get data from the form
            post_type = form.type.data
            content = form.content.data

            # Create a new post
            new_post = Notices(type=post_type, content=content)

            try:
                # Add the new post to the database
                db.session.add(new_post)
                db.session.commit()

                flash('Post created successfully', 'success')
            except Exception as e:
                flash('An error occurred while creating the post', 'danger')

            # Redirect to a page that displays posts, or customize as needed
            return redirect(url_for('posts'))
    return render_template('posts.html', form=form)

@app.route('/download_payment_details/<user_id>', methods=['GET'])
# @login_required  # Add admin role check here
def download_payment_details(user_id):
    # Check if the logged-in user has admin privileges (role-based access control).
    # if current_user.role != 'admin':
    #     flash('You do not have permission to access this page.', 'danger')
    #     return redirect(url_for('index'))

    file = Receipt.query.filter_by(user_id=user_id).first()
    return send_file(BytesIO(file.data), download_name=file.filename, as_attachment=True )
    # payment_details_path = user.payment_details

    # # Check if the file exists before trying to send it.
    # if os.path.isfile(payment_details_path):
    #     return send_file(payment_details_path, as_attachment=True)
    # else:
    #     flash('Payment details not found for this user.', 'danger')
    #     return redirect(url_for('admin_home'))

@app.route('/approve_users', methods=['POST'])
# @login_required  # Add admin role check here
def approve_users():
    data = request.get_json()
    user_ids = data.get('user_ids', [])

    try:
        for user_id in user_ids:
            user = User.query.get(user_id)
            user.status = True
            user.no_dues_applied = False
            db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route("/student_login", methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('student_home'))
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

@app.route("/student_home", methods=['GET', 'POST'])
def student_home():
    # Retrieve the current user
    student = current_user  # Assuming you have a way to get the current user
    if student.status:
        return render_template('no_due_approved.html', student=student)
    due_entry = DuesEntry.query.filter_by(user_id=student.id).first()

     # Get the uploaded file
    if request.method == "POST":
        uploaded_file = request.files['paymentFile']
            
        if uploaded_file:
            # Process the file
            filename = uploaded_file.filename
            upload = Receipt(user_id=student.id, filename=filename, data=uploaded_file.read())
            db.session.add(upload)
        
            # Update the user's payment_details with the file path or filename
            current_user.payment_details = filename  # Update the payment_details field in the database

            db.session.commit()  # Commit the changes

            flash('Receipt uploaded successfully', 'success')
    
    return render_template('student_home.html', student=student, due_entry=due_entry)



from flask import request, jsonify

@app.route('/apply_for_no_dues', methods=['POST'])
@login_required
def apply_for_no_dues():
    # Get the current student
    student = current_user

    # Create a new DuesEntry record
    dues_entry = DuesEntry(
        user_id=current_user.id,
        library_check = 'Applied',
        hostel_fee_check = 'Applied',
        other_fee_check = 'Applied',
        tution_fee_check = 'Applied',
        comments="Applied"
    )

    try:
        # Add the DuesEntry to the database
        # Update the no_dues_applied field to True
        db.session.add(dues_entry)
        db.session.commit()

        student.no_dues_applied = True
        db.session.commit()

        # Query and retrieve dues information as needed
        # dues_info = {
        #     'hostel_fees': student.dues_entries.hostel_fees,
        #     'tuition_fees': student.dues_entries.tuition_fees,
        #     'library_fees': student.dues_entries.library,
        #     'other_fees': student.dues_entries.other_fees,
        #     # Add other dues fields here
        # }

        # Now, load the updated DuesEntry
        student_dues_entry = DuesEntry.query.filter_by(user_id=student.id).first()

        return jsonify({'success': True, 'student_dues_entry': student_dues_entry})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'message': 'Error applying for no dues'})


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

@app.route("/faculty_login", methods=['GET', 'POST'])
def faculty_login():
    form = FacultyLogin()
    # if request.method == 'POST':
    if form.validate_on_submit():
        faculty = User.query.filter_by(username=form.name.data).first()
        if faculty and bcrypt.check_password_hash(faculty.password, form.password.data):
            login_user(faculty)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('faculty_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('faculty_login.html', title='Faculty Login', form=form)

@app.route('/faculty_home', methods=['GET', 'POST'])
@login_required
def faculty_home():
    
    # Check if the current user is a faculty member.
    if current_user.role != 'faculty':
        # Redirect to the appropriate page for non-faculty users.
        return redirect(url_for('faculty_login'))

    # If it's a GET request, retrieve students who have applied for no dues.
    users = User.query.filter_by(no_dues_applied=True).all()
    due_entries = []
    for user in users:
        due_entries.append(DuesEntry.query.filter_by(user_id=user.id).first())

    if request.method == 'POST':
        # Process the form submission
        for selected_user in users:
            enrollment_no = selected_user.enrollment_no
            dues = request.form.get(f'dues_{enrollment_no}')

            # Update the dues entry for the corresponding faculty's department.
            dues_entry = DuesEntry.query.filter_by(user_id=selected_user.id).first()

            if current_user.department == 'library':
                dues_entry.library = dues_entry.library + int(dues)
                dues_entry.library_check = 'ammended'
            elif current_user.department == 'hostel':
                dues_entry.hostel_fees = dues
            elif current_user.department == 'tuition':
                dues_entry.tuition_fees = dues
            elif current_user.department == 'other_fees':
                dues_entry.other_fees = dues

                # Commit the changes to the database.
            db.session.commit()
            
        # Redirect or display a success message
        
        return redirect(url_for('faculty_home'))
    
    return render_template('faculty_home.html', students=users, dept=current_user.department, due_entries=due_entries)
    
@app.route("/register_faculty", methods=['GET', 'POST'])
def register_faculty():
    form = FacultyRegister()
    print(form.errors)
    if request.method == "POST":
        if form.validate_on_submit():
            # Generate a random password
            random_password = generate_random_password()

            hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
            faculty = User(enrollment_no = form.enrollment_no.data, username=form.name.data, email=form.email.data, password=hashed_password, department=form.department.data, role='faculty')
            db.session.add(faculty)
            db.session.commit()
            
            em = EmailMessage()
            em['From'] = email_sender
            # Send the random password to the user's email
            email_receiver = form.email.data
            em['To'] = email_receiver
            em['Subject'] = 'Registration details'
            body= f"Hello {form.name.data},\n\nYour registration is successful!\n\nYour password is: {random_password}\n\nYou can now log in with this password and change it later."
            em.set_content(body)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            flash(f'Account created for {form.name.data}! Please check your email for the password.', 'success')
            return redirect(url_for('admin_home'))
    return render_template('register_faculty.html', form=form)

@app.route('/approve_dues/<int:user_id>/<string:dept>', methods=['POST'])
@login_required
def approve_dues(user_id, dept):
    selected_user = User.query.get(user_id)

    dues_entry = DuesEntry.query.filter_by(user_id=user_id).first()

    if dept == 'library':
        selected_user.dues_entries.library = 'Approved'
        dues_entry.library = 0
        dues_entry.library_check = 'Approved'
        selected_user.dues_entries.library = 'Approved'
    elif current_user.department == 'hostel':
        dues_entry.hostel_fees = 0
    elif current_user.department == 'tuition':
        dues_entry.tuition_fees = 0
    elif current_user.department == 'other_fees':
        dues_entry.other_fees = 0

    # Commit the changes to the database
    db.session.commit()
    
    return redirect(url_for('faculty_home'))


@app.route("/alumni_home")
def alumni_home():
    return render_template('alumni_home.html')

@app.route("/alumni_login", methods=['GET', 'POST'])
def alumni_login():
    form = AlumniLogin()
    # if request.method == 'POST':
    if form.validate_on_submit():
        alum = Alumni.query.filter_by(username=form.name.data).first()
        if alum and bcrypt.check_password_hash(alum.password, form.password.data):
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('alumni_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('alumni_login.html', title='Alumni Login', form=form)

@app.route("/register_alumni", methods=['GET', 'POST'])
def register_alumni():
    form = AlumniRegister()
    print(form.errors)
    if request.method == "POST":
        if form.validate_on_submit():
            # Generate a random password
            random_password = generate_random_password()

            hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
            alumni = Alumni(username=form.name.data, email=form.email.data, password=hashed_password, course=form.course.data, address=form.address.data, organization=form.organization.data)
            db.session.add(alumni)
            db.session.commit()
            
            em = EmailMessage()
            em['From'] = email_sender
            # Send the random password to the user's email
            email_receiver = form.email.data
            em['To'] = email_receiver
            em['Subject'] = 'Registration details'
            body= f"Hello {form.name.data},\n\nYour registration is successful!\n\nYour password is: {random_password}\n\nYou can now log in with this password and change it later."
            em.set_content(body)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            flash(f'Account created for {form.name.data}! Please check your email for the password.', 'success')
            return redirect(url_for('admin_home'))
    return render_template('register_alumni.html', form=form)

@app.route("/error_page")
def error_page():
    return render_template('somethings_wrong.html')

@app.route("/change_password")
def change_password():
    form = ChangePassword()
    if request.method == 'POST':
        new_password = form.new_password.data
        if current_user.password == form.old_password.data:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            em = EmailMessage()
            em['From'] = email_sender
            # Send the random password to the user's email
            email_receiver = current_user.email
            em['To'] = email_receiver
            em['Subject'] = 'Password Reset'
            body= f"Hello,\n\nYour password is changed to: {new_password}\n\nYou can now log in with this password."
            em.set_content(body)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            flash('Your account has been updated', 'success')
            return redirect(url_for('student_home'))
        flash('Unsuccessful', 'danger')
    return render_template('change_password.html', form=form)

@app.route("/forgot_password")
def forgot_password():
    form = ForgotForm()
    if form.validate_on_submit():
        try:
            random_password = generate_random_password()
            hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
            user = User.query.filter_by(email=form.email.data).first()
            user.password = hashed_password
            db.session.commit()
            em = EmailMessage()
            em['From'] = email_sender
            # Send the random password to the user's email
            email_receiver = form.email.data
            em['To'] = email_receiver
            em['Subject'] = 'Password Reset'
            body= f"Hello,\n\nYour password is changed to: {random_password}\n\nYou can now log in with this password and change it later."
            em.set_content(body)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            flash(f'Account updated for {user.username}! Please check your email for the password.', 'success')
            return redirect(url_for('home'))
        except OperationalError as e:
            flash('An error occurred.', 'danger')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html', form=form)