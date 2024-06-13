# final_project_CIP2024
Expense Tracker - console based Python application - Final Project for Code in Place 2024

EXPENSE TRACKER APPLICATION, Ver V1.0, 2024/06/14
_________________________________________________

Developer name: Kunal

NOTE: For a Demo run of this application, Please use below:

User Credentials
----------------
username: kkk

password: kkk123

_________________________________________________

A Note of Gratitude:
-------------------
My sincere Thank You to the entire team of Code_in_Place_2024!

Chris, Mehran, TJ, Juliette, Patricia, Cameron, Brahm and others - you guys are an Inspiration.
You helped me push my boundaries of Learning...
This is my first attempt with Application dev, and there could be "bugs" -
program flow issues, file reading issues with concurrent access to data files.
I have tried to handle the Exceptions where possible to the best of my knowledge!

----------------------------------------------------------------------------------------
Word of Caution :)
Please follow the Input Instructions as closely as possible to avoid program flow issues


Top-level Functionalities:
--------------------------
1) Setup User profile, one-time process
2) Login to User Dashboard
3) Create, Modify, Delete - Expense Entries
4) View Last 10 or Historical (Date Range wise) Expense Entries
5) View Expense Summary Reports - current, previous month, Date range

Back-End:
---------
1) "user_profiles_data.txt" - saves User profiles data in JSON format (dictionary)
2) "error_logs.txt" - saves Error logs generated during file reading/writing, as (tuples)
3) "user_expenses_data.txt" - saves Expense Txn records for All Users in CSV format


Program Flow:
--------------

Application Home Screen ->
  User Login:
  
  Existing Users Login ->
  Enter username, password, OR, reset password with Email 

  New User Login ->
  Create username, password, provide Email, Name, Country

Login failed ->
Incorrect Username/Password -> Resert password with Email
	
Login successful ->

	USER DASHBOARD / HOME SCREEN 
		-> Main Menu Options 
			-> Create New Expense Entry
				-> Confirm and Save to database
				-> Cancel, and Start over

			-> View Last 10 Entries
			
			-> View Expense entries by Date Range

			-> Edit Expense Entry 
				-> Select field to modify -> Repeat for other fields 
				-> Delete entry
			
			-> View Expense Summary Reports
				-> Select Summary report type 

			-> Logout




***********************************************************************************

