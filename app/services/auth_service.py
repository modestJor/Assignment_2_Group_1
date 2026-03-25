from werkzeug.security import check_password_hash, generate_password_hash
from app.models import ChurchAdmin
 
class AuthService:
    def verify_credentials(self, username: str, password: str) -> ChurchAdmin:
        admin = ChurchAdmin.query.filter_by(username=username).first()
        if not admin or not check_password_hash(admin.password_hash, password):
            raise ValueError("Invalid login credentials")
        return admin
 
    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)
