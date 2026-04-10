from app.models import db, Ministry

class MinistryRepository:
    def save(self, name, description, leader_name, leader_contact) -> Ministry:
        ministry = Ministry(
            name=name,
            description=description,
            leader_name=leader_name,
            leader_contact=leader_contact
        )
        db.session.add(ministry)
        db.session.commit()
        return ministry

    def find_all(self) -> list:
        """Return all ministries."""
        return Ministry.query.order_by(Ministry.id.desc()).all()

    def find_by_id(self, ministry_id: int):
        """Return a single ministry by ID."""
        return Ministry.query.get(ministry_id)

    def delete(self, ministry_id):
        ministry = self.find_by_id(ministry_id)
        if ministry:
            db.session.delete(ministry)
            db.session.commit()
            return True
        return False