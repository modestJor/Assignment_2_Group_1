from app.models import db, Announcement
from datetime import date


class AnnouncementRepository:

    def save(self, title: str, content: str, posted_by: str) -> Announcement:
        """Create and save a new announcement."""
        announcement = Announcement(
            title=title,
            content=content,
            date_posted=str(date.today()),
            posted_by=posted_by
        )
        db.session.add(announcement)
        db.session.commit()
        return announcement

    def find_all(self) -> list:
        """Return all announcements, newest first."""
        return Announcement.query.order_by(Announcement.id.desc()).all()

    def find_by_id(self, announcement_id: int):
        """Return a single announcement by ID."""
        return Announcement.query.get(announcement_id)

    def delete(self, announcement_id: int) -> bool:
        """Delete an announcement by ID. Returns True if successful."""
        announcement = Announcement.query.get(announcement_id)
        if not announcement:
            return False
        db.session.delete(announcement)
        db.session.commit()
        return True