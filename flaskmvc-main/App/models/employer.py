from App.database import db
from App.models.user import User #816040069 Jonathan Dass

class Employer(User):
    __tablename__ = 'employers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    employer_name = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)

    internships = db.relationship('Internship', backref='employer', lazy=True, foreign_keys='Internship.employer_id')

    __mapper_args__ = {
        'polymorphic_identity': 'employer',
    }

    def __init__(self, username, password, name, company=None, industry=None):
        super().__init__(username, password, user_type='employer')
        self.employer_name = name
        self.company = company
        self.industry = industry

    def __repr__(self):
        return f"<Employer {self.employer_name}>"

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'employer_name': self.employer_name,
            'company': self.company,
            'industry': self.industry,
            'user_type': self.user_type
        }