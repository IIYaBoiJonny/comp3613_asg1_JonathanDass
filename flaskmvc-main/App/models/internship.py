from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User
from App.models.student import Student
from App.models.employer import Employer  #816040069 Jonathan Dass

class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with shortlists
    shortlisted_students = db.relationship('Shortlist', backref='internship', lazy=True, foreign_keys='Shortlist.internship_id')

    def __init__(self, title, description=None, employer_id=None):
        self.title = title
        self.description = description
        self.employer_id = employer_id

    def __repr__(self):
        return f"<Internship {self.title}>"

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'employer_id': self.employer_id
        }