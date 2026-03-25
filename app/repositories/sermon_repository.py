from app.models import db, SermonSummary
from datetime import date

class SermonRepository:
    def save(self, title: str, speaker: str, date_preached: str, summary: str) -> SermonSummary:
        """Create and save a new sermon summary."""
        sermon = SermonSummary(
            title=title,
            speaker=speaker,
            date_preached=date_preached,
            date_posted=str(date.today()),
            summary=summary
        )
        db.session.add(sermon)
        db.session.commit()
        return sermon

    def find_all(self) -> list:
        """Return all sermon summaries, newest first."""
        return SermonSummary.query.order_by(SermonSummary.id.desc()).all()

    def find_by_id(self, sermon_id: int):
        """Return a single sermon summary by ID."""
        return SermonSummary.query.get(sermon_id)

    def delete(self, sermon_id):
        sermon = self.find_by_id(sermon_id)
        if sermon:
            db.session.delete(sermon)
            db.session.commit()
            return True
        return False