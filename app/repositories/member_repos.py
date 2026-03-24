from app.models import db, Member

class MemberRepository:
    def save(self, member: Member) -> Member:
        db.session.add(member)
        db.session.commit()
        return member

    def find_by_id(self, member_id: int) -> Member:
        return Member.query.get(member_id)

    def find_by_name(self, name: str):
        return Member.query.filter(
            Member.name.ilike(f'%{name}%')
        ).all()

    def get_all(self):
        return Member.query.all()

    def update(self, member_id: int, data: dict) -> Member:
        member = self.find_by_id(member_id)
        if not member:
            raise ValueError(f"Member {member_id} not found")
        for key, value in data.items():
            if hasattr(member, key):
                setattr(member, key, value)
        db.session.commit()
        return member

    def delete(self, member_id: int) -> bool:
        member = self.find_by_id(member_id)
        if not member:
            raise ValueError(f"Member {member_id} not found")
        db.session.delete(member)
        db.session.commit()
        return True
