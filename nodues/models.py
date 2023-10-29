from nodues import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_no = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    course = db.Column(db.String(20), nullable=True)
    batch = db.Column(db.String(4), nullable=True)
    address = db.Column(db.Text)
    placement = db.Column(db.String(20), nullable=True)
    payment_details = db.Column(db.String(120), nullable=True, default='default.jpg')
    no_dues_applied = db.Column(db.Boolean, default=False)
    dues_entries = db.relationship('DuesEntry', backref='user')
    department = db.Column(db.String(20), nullable=True)
    receipt_file = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='student')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.enrollment_no}', '{self.course}', '{self.batch}', '{self.address}')"

class DuesEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    hostel_fees = db.Column(db.Integer, nullable=True)
    hostel_fee_check = db.Column(db.String(20), nullable=True)
    tuition_fees = db.Column(db.Integer, nullable=True)
    tution_fee_check = db.Column(db.String(20), nullable=True)
    other_fees = db.Column(db.Integer, nullable=True)
    other_fee_check = db.Column(db.String(20), nullable=True)
    library = db.Column(db.Integer, nullable=True)
    library_check = db.Column(db.String(20), nullable=True)
    comments = db.Column(db.Text)

    def __repr__(self):
        return f"DuesEntry(user_id='{self.user_id}', faculty_id='{self.faculty_id}')"

# class Faculty(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(20), unique=True, nullable=False)
#     name = db.Column(db.String(120), unique=True, nullable=False)
#     department = db.Column(db.String(20), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     dues_entries = db.relationship('DuesEntry', backref='faculty')

#     def __repr__(self):
#         return f"Faculty(name='{self.name}', department='{self.department}')"
    
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(20), nullable=False)
    # Add other fields as needed, e.g., upload date, description, etc.

class Alumini(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
