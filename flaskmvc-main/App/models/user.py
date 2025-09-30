from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db #816040069 Jonathan Dass

class User(db.Model): #i made all the models of usertype polymorphic for simple inheritance and stuff like that
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type
    }

    def __init__(self, username, password, user_type='user'):
        self.username = username
        self.user_type = user_type
        self.set_password(password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)