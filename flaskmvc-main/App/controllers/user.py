from App.models import User
from App.database import db

def create_user(username, password, user_type, **kwargs): #i had to update this so the other usertypes morph correctly like some scifi shit
    user = None
    if user_type == 'student':
        from App.models.student import Student
        user = Student(username, password, 
                      kwargs.get('name', username),
                      kwargs.get('email'),
                      kwargs.get('age'))
    elif user_type == 'staff':
        from App.models.staff import Staff
        user = Staff(username, password, kwargs.get('name', username))
    elif user_type == 'employer':
        from App.models.employer import Employer
        user = Employer(username, password,
                       kwargs.get('name', username),
                       kwargs.get('company'),
                       kwargs.get('industry'))
    else:
        from App.models.user import User
        user = User(username, password, user_type)
    
    if user:
        db.session.add(user)
        db.session.commit()
    return user

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
