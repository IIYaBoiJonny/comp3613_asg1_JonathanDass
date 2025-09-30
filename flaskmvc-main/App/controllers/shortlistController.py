from App.database import db
from App.models.shortlist import Shortlist

def create_shortlist(student_id, internship_id): #dunno if i did this right but it works :D
    new_shortlist = Shortlist(student_id=student_id, internship_id=internship_id)
    db.session.add(new_shortlist)
    db.session.commit()
    return new_shortlist

def get_shortlist(id):
    return db.session.get(Shortlist, id)

def get_all_shortlists():
    return db.session.scalars(db.select(Shortlist)).all()

def get_shortlists_by_internship(internship_id):
    return db.session.scalars(db.select(Shortlist).filter_by(internship_id=internship_id)).all()

def add_to_shortlist(student_id, internship_id):
    # Check if this student is already shortlisted for this internship
    existing_entry = db.session.scalar(db.select(Shortlist).filter_by(student_id=student_id, internship_id=internship_id))
    if existing_entry:
        return None
    
    new_entry = Shortlist(student_id=student_id, internship_id=internship_id)
    db.session.add(new_entry)
    try:
        db.session.commit()
        return new_entry
    except Exception as e:
        db.session.rollback()
        return None

def remove_from_shortlist(student_id, internship_id):
    entry = db.session.scalar(db.select(Shortlist).filter_by(student_id=student_id, internship_id=internship_id))
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return True
    return False

def delete_shortlist(id):
    shortlist = get_shortlist(id)
    if shortlist:
        db.session.delete(shortlist)
        db.session.commit()
        return True
    return None

def update_shortlist_status(shortlist_id, status, employer_id):
        try:
            # Convert employer_id to int if it's a string
            if isinstance(employer_id, str):
                try:
                    employer_id = int(employer_id)
                except ValueError:
                    return False, f"Invalid employer_id format: {employer_id}"
            
            shortlist = db.session.get(Shortlist, shortlist_id)
            if not shortlist:
                return False, "Shortlist entry not found"
            
            # Verify employer owns this internship
            if shortlist.internship.employer_id != employer_id:
                return False, f"Invalid employer ID. Internship belongs to employer {shortlist.internship.employer_id}, but you provided {employer_id}"
            
            shortlist.status = status
            db.session.commit()
            return True, f"Status updated to {status}"
        except Exception as e:
            return False, f"Error: {str(e)}"

def get_shortlists_by_student(student_id):
    return db.session.scalars(db.select(Shortlist).filter_by(student_id=student_id)).all()