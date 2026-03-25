from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
 
class Ministry(db.Model):
    __tablename__ = 'ministry'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    leader_name = db.Column(db.String(100))
    leader_contact = db.Column(db.String(100))
    members = db.relationship('Member', backref='ministry', lazy=True)
 
    def get_details(self):
        return {
            'id': self.id, 'name': self.name,
            'description': self.description,
            'leader': self.leader_name
        }
 
 
class Member(db.Model):
    __tablename__ = 'member'
    id  = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(150))
    dob = db.Column(db.String(20))
    address = db.Column(db.String(200))
    status = db.Column(db.String(50), default='Active')
    ministry_id  = db.Column(db.Integer, db.ForeignKey('ministry.id'))
 
    def validate(self):
        """Returns True if required fields are present."""
        return bool(self.name and self.contact_info)
 
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name,
            'contact_info': self.contact_info, 'dob': self.dob,
            'address': self.address, 'status': self.status,
            'ministry_id': self.ministry_id
        }
 
 
class ChurchAdmin(db.Model):
    __tablename__ = 'church_admin'
    id = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    access_level = db.Column(db.String(50), default='admin')

class Announcement(db.Model):
    __tablename__ = 'announcement'
 
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(150), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String(30))
    posted_by  = db.Column(db.String(100))
 
    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'content':     self.content,
            'date_posted': self.date_posted,
            'posted_by':   self.posted_by
        }

class SermonSummary(db.Model):
    __tablename__ = 'sermon_summary'
 
    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(150), nullable=False)
    summary    = db.Column(db.Text, nullable=False)
    date_preached      = db.Column(db.String(30))
    date_posted = db.Column(db.String(30))
    speaker   = db.Column(db.String(100))