from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from nodues.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    enrollment_no = StringField('Enrollment No',
                        validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    course = StringField('Course',
                        validators=[DataRequired()])
    batch = StringField('Batch', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_enrollment_no(self, enrollment_no):
        user = User.query.filter_by(enrollment_no=enrollment_no.data).first()
        if user:
            raise ValidationError('That enrollment_no is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLogin(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class FacultyLogin(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class FacultyRegister(FlaskForm):
    enrollment_no = StringField('Enrollment No',
                        validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name  = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AlumniLogin(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AlumniRegister(FlaskForm):
    name  = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course = StringField('Course', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    enrollment_no = StringField('Enrollment No',
                        validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    course = StringField('Course',
                        validators=[DataRequired()])
    batch = StringField('Batch', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already taken.')
            
class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_old_password(self, password):
        user = User.query.filter_by(email=password.data).first()
        if user:
            raise ValidationError('Email already taken.')

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class Posts(FlaskForm):
    type = SelectField('Type', choices=[('update', 'Update'), ('event', 'Event'), ('job', 'Job Posting')], validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

