from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import UpdateLogin, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ea77a2c1cff84971c247e008b1a749fd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    enrollment_no = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    batch = db.Column(db.String(4), nullable=False)
    address = db.Column(db.Text)
    hostel_fees = db.Column(db.String(20), unique=True, nullable=False)
    tuition_fees = db.Column(db.String(20), unique=True, nullable=False)
    other_fees = db.Column(db.String(20), unique=True, nullable=False)
    library = db.Column(db.String(20), unique=True, nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.course}', '{self.batch}', '{self.address}')"


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

@app.route("/updatelogin", methods=['GET', 'POST'])
def updatelogin():
    form = UpdateLogin()
    if form.validate_on_submit():
        flash(f'Account updated for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('updatelogin.html', title='Update Login', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)