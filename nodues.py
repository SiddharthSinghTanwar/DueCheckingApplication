from flask import Flask, render_template, url_for, flash, redirect
from forms import UpdateLogin, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ea77a2c1cff84971c247e008b1a749fd'

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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('updatelogin.html', title='Register', form=form)


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