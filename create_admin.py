# create_admin.py
from apps import app
from app.models import db, ChurchAdmin
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    existing = ChurchAdmin.query.filter_by(username='admin').first()
    
    if existing:
        print('Admin already exists, skipping.')
    else:
        admin = ChurchAdmin(
            username='admin',
            email='admin@cogop.com',
            password_hash=generate_password_hash('admin123'),
            access_level='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin created! Username: admin | Password: admin123')