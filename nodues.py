from flask import Flask, render_template, url_for
app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)