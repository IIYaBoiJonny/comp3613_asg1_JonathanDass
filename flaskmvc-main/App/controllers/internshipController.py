from App.database import db
from App.models.internship import Internship
from App.models.employer import Employer

def create_internship(title, description, employer_name): #also not sure if i did this right but it works :D
    # First, find the employer
    employer = db.session.execute(db.select(Employer).filter_by(employer_name=employer_name)).scalar_one_or_none()
    if not employer:
        print(f"Error: No employer found with name '{employer_name}'")
        return None
    
    # Create internship with valid employer_id
    new_internship = Internship(title=title, description=description, employer_id=employer.id)
    db.session.add(new_internship)  
    db.session.commit()
    return new_internship

def get_internship(id):
    return db.session.get(Internship, id)

def get_all_internships():
    return db.session.scalars(db.select(Internship)).all()

def update_internship(id, title=None, description=None):
    internship = get_internship(id)
    if internship:
        if title:
            internship.title = title
        if description:
            internship.description = description
        # internship is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

def delete_internship(id):
    internship = get_internship(id)
    if internship:
        db.session.delete(internship)
        db.session.commit()
        return True
    return None

def get_internships_by_employer(employer_id):
    result = db.session.execute(db.select(Internship).filter_by(employer_id=employer_id))
    return result.scalars().all()