Im sorry i deleted all ur stuff here, they were actually pretty helpful to get my bearings:

Employer Cmds:

  create                   Create an employer
  create_internship        Create an internship
  list_internships         List all internships
  list_shortlists          List all shortlisted students for an internship
  show_internship_details  Show detailed information about an internship
  update_status            Update the status of a shortlist entry

Staff Cmds:
  list_all_shortlists  List all shortlist entries
  list_employers       List all employers with their details
  list_internships     List all internships
  list_users           List all users
  shortlist_student    Add a new student to the shortlist

Student Cmds:
    view_shortlist  View shortlisted internships for a student

U can type --help for any of the usertypes to have this appear in console

typical walkthrough to show functionality is:

flask employer create_internship <internship name> <employer id>  ID for this input is 'bob' cuz i forogt to change it
flask staff shortlist_student <internship id> <student username>  id is based on number of internships created, starting at 1
flask staff shortlist_student (theres 2 students to shortlist)
flask employer update_status <shortlistid> <status(accepted / rejected)> <empid> shortlist id is based on order of added students, empid=1  
flask student view_shortlist <student username> 

Idk if i was supposed to have all of that be in the init or not so i just had 4 users created during init instead
i didnt use AI for anything other than some small testing samples though i believed i've deleted all AI related code
the other cmds arent useful for functionality but i just added them while testing since i was losing my mind 


