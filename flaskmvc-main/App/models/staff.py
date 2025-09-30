from App.database import db
from App.models.user import User

class Staff(User):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    staff_name = db.Column(db.String(100), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, username, password, name):
        # FIXED
        super().__init__(username, password, user_type='staff')
        self.staff_name = name

    def __repr__(self):
        return f"<Staff {self.staff_name}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'staff_name': self.staff_name,
            'user_type': self.user_type
        }