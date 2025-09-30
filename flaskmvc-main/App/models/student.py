from App.database import db
from App.models.user import User #816040069 Jonathan Dass

class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    student_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)

    # Relationship
    shortlisted_internships = db.relationship('Shortlist', backref='student', lazy=True, foreign_keys='Shortlist.student_id')

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, name, email=None, age=None):
        super().__init__(username, password, user_type='student')
        self.student_name = name
        self.email = email
        self.age = age

    def __repr__(self):
        return f"<Student {self.student_name}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'student_name': self.student_name,
            'email': self.email,
            'age': self.age,
            'user_type': self.user_type
        }