from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from App.models.user import User #816040069 Jonathan Dass

class Shortlist(db.Model):
    __tablename__ = 'shortlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)
    added_by_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # New field to track who added the entry

    #remember to add the connstraints so evetythign stops breaking
    __table_args__ = (db.UniqueConstraint('student_id', 'internship_id', name='unique_student_internship'),)

    def __init__(self, student_id, internship_id, title="Shortlist Entry", description=None, status="pending"):
        self.student_id = student_id
        self.internship_id = internship_id
        self.title = title
        self.description = description
        self.status = status

    def __repr__(self):
        return f"<Shortlist {self.title}>"

    def get_json(self):
        data = super().get_json()
        data.update({
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'student_id': self.student_id,
            'internship_id': self.internship_id
        })
        return data