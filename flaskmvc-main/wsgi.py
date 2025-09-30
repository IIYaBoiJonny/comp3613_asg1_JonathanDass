from flask_jwt_extended import current_user #816040069 Jonathan Dass
import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.controllers.internshipController import create_internship, get_all_internships
from App.controllers.shortlistController import add_to_shortlist, update_shortlist_status, get_shortlists_by_student, get_shortlists_by_internship
from App.controllers.user import get_user_by_username
from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 
employer_cli = AppGroup('employer', help='Employer object commands')
student_cli = AppGroup('student', help='Student object commands')
staff_cli = AppGroup('staff', help='Staff object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.argument("user_type", default="user")
def create_user_command(username, password, user_type):
    create_user(username, password, user_type)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


#employer commands
@employer_cli.command("create", help="Create an employer")
@click.argument("username")
@click.argument("password")
@click.argument("name")
@click.option("--company", default=None, help="Company name")
@click.option("--industry", default=None, help="Industry")
def create_employer_command(username, password, name, company, industry):
    result = create_user(username, password, 'employer', name=name, company=company, industry=industry)
    if result:
        print(f'Employer "{name}" created successfully!')
    else:
        print(f'Failed to create employer "{name}".')

@employer_cli.command("create_internship", help="Create an internship")
@click.argument("title")
@click.argument("description")
@click.argument("name")
def create_internship_command(title, description, name):
    result = create_internship(title, description, name)
    if result:
        print(f'Internship "{title}" created successfully!')
    else:
        print(f'Failed to create internship. Make sure employer "{name}" exists.')

@employer_cli.command("update_status", help="Update the status of a shortlist entry")
@click.argument("shortlist_id", type=int)
@click.argument("status")
@click.argument("employer_id", type=int)
def update_shortlist_status_command(shortlist_id, status, employer_id):
    result, message = update_shortlist_status(shortlist_id, status, employer_id)
    if result:
        print(f"Success: {message}")
    else:
        print(f"Error: {message}")

@employer_cli.command("list_internships", help = "List all internships")
def list_internships_command():
    internships = get_all_internships()
    for internship in internships:
        print(f'Internship {internship.id}: {internship.title}')
    if not internships:
        print("No internships found.")

@employer_cli.command("list_shortlists", help="List all shortlisted students for an internship")
@click.argument("internship_id", type=int)
def list_shortlisted_students_command(internship_id):
    shortlists = get_shortlists_by_internship(internship_id)
    if shortlists:
        print(f"Shortlisted students for internship {internship_id}:")
        for entry in shortlists:
            print(f'  Shortlist Entry {entry.id}: Student {entry.student.username} - Status: {entry.status}')
    else:
        print(f"No shortlisted students found for internship {internship_id}.")

@employer_cli.command("show_internship_details", help="Show detailed information about an internship")
@click.argument("internship_id", type=int)
def show_internship_details_command(internship_id):
    from App.controllers.internshipController import get_internship
    internship = get_internship(internship_id)
    if internship:
        print(f"Internship {internship.id}: {internship.title}")
        print(f"  Description: {internship.description}")
        print(f"  Employer ID: {internship.employer_id}")
        print(f"  Employer: {internship.employer.employer_name if internship.employer else 'Unknown'}")
    else:
        print(f"No internship found with ID {internship_id}")

#student commands
@student_cli.command("view_shortlist", help="View shortlisted internships for a student")
@click.argument("student_name", type=str)
def view_shortlist_command(student_name):
    student = get_user_by_username(student_name)
    if not student:
        print(f"Error: No student found with name '{student_name}'")
        return

    shortlists = get_shortlists_by_student(student.id)
    if shortlists:
        for entry in shortlists:
            print(f'Shortlist Entry {entry.id}: Internship {entry.internship.title} - Status: {entry.status}')
    else:
        print("No shortlisted internships found.")

#staff commands
@staff_cli.command("list_internships", help = "List all internships")
def list_internships_for_students_command():
    internships = get_all_internships()
    for internship in internships:
        print(f'Internship {internship.id}: {internship.title}, Employer ID: {internship.employer_id}')
    if not internships:
        print("No internships found.")

@staff_cli.command("list_users", help="List all users")
def list_all_users_command():
    users = get_all_users()
    if users:
        print("All users:")
        for user in users:
            print(f'  User {user.id}: {user.username} (Type: {user.user_type})')
    else:
        print("No users found.")

@staff_cli.command("list_employers", help="List all employers with their details")
def list_employers_command():
    from App.models.employer import Employer
    employers = db.session.scalars(db.select(Employer)).all()
    if employers:
        print("All employers:")
        for employer in employers:
            print(f'  Employer {employer.id}: {employer.employer_name} (Username: {employer.username}, Company: {employer.company})')
    else:
        print("No employers found.")

@staff_cli.command("shortlist_student", help="Add a new student to the shortlist")
@click.argument("student_username", type=str)
@click.argument("internship_id", type=int)
def shortlist_student_command(student_username, internship_id):
    student = get_user_by_username(student_username)
    if not student:
        print(f"Error: No student found with username '{student_username}'")
        return
    
    if student.user_type != 'student':
        print(f"Error: User '{student_username}' is not a student")
        return

    result = add_to_shortlist(student.id, internship_id)
    if result:
        print(f'Student {student_username} shortlisted for internship {internship_id}.')
    else:
        print(f'Failed to shortlist student {student_username} for internship {internship_id}.')

@staff_cli.command("list_all_shortlists", help="List all shortlist entries")
def list_all_shortlists_command():
    from App.controllers.shortlistController import get_all_shortlists
    shortlists = get_all_shortlists()
    if shortlists:
        print("All Shortlist Entries:")
        for entry in shortlists:
            print(f'  Entry {entry.id}: Student ID {entry.student_id} → Internship ID {entry.internship_id} (Status: {entry.status})')
    else:
        print("No shortlist entries found.")

app.cli.add_command(test)
app.cli.add_command(employer_cli)
app.cli.add_command(student_cli)
app.cli.add_command(staff_cli)
app.cli.add_command(user_cli)
