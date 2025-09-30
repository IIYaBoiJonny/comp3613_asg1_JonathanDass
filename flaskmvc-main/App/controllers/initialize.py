from App.models import *
from .user import create_user
from App.database import db


def initialize(): #just intitalize with 4users to test logic but u should be ablet o make more usieres without breaking
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'employer', name='Bob', company='BobCo', industry='Tech')
    create_user('alice', 'alicepass', 'student', name='Alice', email='alice@example.com', age=21)
    create_user('robert', 'robertpass', 'student', name='Robert', email='robert@example.com', age=22)
    create_user('eve', 'evepass', 'staff', name='Eve')
