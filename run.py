# from nodues import create_app, db
# app = create_app()
from nodues import app, db

# If you need to create the database tables, you can do it here
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

