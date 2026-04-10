from flask import Flask
from app.models import db
from app.routes.auth_routes import auth_bp
from app.routes.member_routes import member_bp
from app.routes.main_routes import main_bp
from app.routes.announcement_routes import announcement_bp
from app.routes.sermon_routes import sermon_bp
from app.routes.volunteer_routes import volunteer_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cogop.db'
app.config['SECRET_KEY'] = 'cogop-secret-key-2026'

db.init_app(app)

app.register_blueprint(auth_bp,   url_prefix='/auth')
app.register_blueprint(member_bp, url_prefix='/members')
app.register_blueprint(announcement_bp, url_prefix='/announcements')
app.register_blueprint(sermon_bp, url_prefix="/sermons")
app.register_blueprint(volunteer_bp, url_prefix="/volunteers")
app.register_blueprint(main_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)