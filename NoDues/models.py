from NoDues import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    enrollment_no = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    batch = db.Column(db.String(4), nullable=False)
    address = db.Column(db.Text)
    # dues = db.relationship('Nodue', backref='student', lazy=True)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def get_id(self):
        return str(self.enrollment_no)

    def __repr__(self):
        return f"User('{self.name}','{self.enroll_no}','{self.email}','{self.course}','{self.batch}','{self.address}')"


class Nodue(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.enrollment_no'), unique=True, nullable=False)
    library = db.Column(db.String(10), nullable=False)
    hostel_fess = db.Column(db.String(10), nullable=False)
    tuition_fee = db.Column(db.String(10), nullable=False)
    membership_fee = db.Column(db.String(10), nullable=False)
    other_fees = db.Column(db.String(10), nullable=False)
    miscellaneous = db.Column(db.String(10), nullable=False)
    exam = db.Column(db.String(10), nullable=False)
    # Add the user relationship to the Nodue model for one-one mapping
    # user = db.relationship('User', backref='nodue', uselist=False)

    def __repr__(self):
        return f"Nodue('{self.user_id}', '{self.library}', '{self.exam}', '{self.tuition_fee}', '{self.Hostel_fess}', '{self.membership_fee}', '{self.miscellaneous}', '{self.other_fees})"
