from app.models import db, VolunteerActivity, VolunteerSignup
from datetime import date

class VolunteerRepository:
    def save_activity(self, title: str, description: str, date_str: str, location: str, max_volunteers: int) -> VolunteerActivity:
        """Create and save a new volunteer activity."""
        activity = VolunteerActivity(
            title=title,
            description=description,
            date=date_str,
            location=location,
            max_volunteers=max_volunteers
        )
        db.session.add(activity)
        db.session.commit()
        return activity

    def find_all_activities(self) -> list:
        """Return all volunteer activities, newest first."""
        return VolunteerActivity.query.order_by(VolunteerActivity.date).all()

    def find_activity_by_id(self, activity_id: int):
        """Return a single volunteer activity by ID."""
        return VolunteerActivity.query.get(activity_id)

    def delete_activity(self, activity_id):
        activity = self.find_activity_by_id(activity_id)
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return True
        return False

    def signup_for_activity(self, activity_id: int, volunteer_name: str, contact_info: str) -> VolunteerSignup:
        """Sign up a volunteer for an activity."""
        signup = VolunteerSignup(
            activity_id=activity_id,
            volunteer_name=volunteer_name,
            contact_info=contact_info,
            signup_date=str(date.today())
        )
        db.session.add(signup)
        db.session.commit()
        return signup
    
    def unregister_from_activity(self, activity_id: int, volunteer_name: str) -> bool:
        signup = VolunteerSignup.query.filter_by(activity_id=activity_id, volunteer_name=volunteer_name).first()
        if signup:
            db.session.delete(signup)
            db.session.commit()
            return True
        return False