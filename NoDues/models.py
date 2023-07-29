from nodues import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enrollment_no = db.Column(db.String(10), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    batch = db.Column(db.String(4), nullable=False)
    address = db.Column(db.Text)
    dues = db.relationship('Dues', backref='user', uselist=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.enrollment_no}', '{self.course}', '{self.batch}', '{self.address}')"

class Dues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostel_fees = db.Column(db.String(20), unique=True, nullable=True)
    tuition_fees = db.Column(db.String(20), unique=True, nullable=True)
    other_fees = db.Column(db.String(20), unique=True, nullable=True)
    library = db.Column(db.String(20), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.hostel}', '{self.tuition_fees}', '{self.other_fees}', '{self.library}', '{self.user_id}')"