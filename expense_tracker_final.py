"""
File name: expense_tracker_final.py
-----------------------------------
This program works as a console-based Expense tracker application, allowing a User to:
1) set up an account with a Username/ Password - one-time sign up process and thereafter, login and access Home screen
2) Create, Edit or Delete Expense Entries for a given Date
3) User must categorize their Expense entries, as per in-built Expense categories menu
4) View historical Expense entries over a Date range
5) Expense Summary reports - by category, by date, etc.
6) User can additionally reset their login password, after repetitive unsuccessful Login attempts.
"""

# VERSION V1.0
# coded by - 'Kunal', for Code in Place 2024 final project submission

import pandas as pd             # for DataFrames
import re                       # to check for valid email expressions
import os                       # to check for file size, empty or nom-empty, etc.
import sys                      # used in password masking helper function
import msvcrt                   # used getch() in password masking
import json                     # to read/write dictionary into text files and vice versa (User Profiles)
import time                     # for time.sleep()
from datetime import datetime   # to retrieve current date / time
from datetime import timedelta  # to increment/decrement Date by N number of days
from tabulate import tabulate   # for tablular data display and formatting

# define File path constants for easy access to reading/writing files in database
FILE_PATH_USERS = "user_profiles_data.txt"  # txt file with User profiles in JSON format (dictionary)
FILE_PATH_TXN = "user_expenses_data.txt"  # csv format file with Expense Txn records for ALl Users


# data file saved as .txt to retain Date formatting when reading and writing Txn Dates.


def display_header(username=None):
    # Display a common header for the application, passing in username as the argument
    # this argument is used to retrieve User's name to display welcome msg.
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("  EXPENSE TRACKER APPLICATION, ver. V1.0  ")
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    # populate current date and time
    curr_date = datetime.today().strftime('%Y-%m-%d')
    curr_time = datetime.today().strftime('%H:%M')

    # show user's Name on dashboard
    if username is None:
        name = "User"
    else:
        name = fetch_user_name(username)

    # print welcome msg to user and display current system date/time
    print("\nWelcome,", name + "!", "\t Today is:", curr_date, "\tClock:", curr_time)


def clear_terminal():
    # clear the console terminal
    if "nt" in os.name:  # Windows systems are "nt"
        cls = "cls"
    else:
        cls = "clear"

    os.system(cls)


def menu_options_user_login():
    # Display User Login options menu on the landing page of the app.

    print(" ---------- ")
    print(" USER LOGIN ")
    print(" ---------- ")

    # create a Dictionary: 'keys' as menu option texts, 'values' as corresponding action to perform
    op_1 = "Existing User Login"
    op_2 = "New User Signup"

    menu_dict = {op_1: ["Press '1' and Enter"],
                 op_2: ["Press '2' and Enter"]
                 }
    # display menu dict. in tabular format
    print(tabulate(menu_dict, headers="keys"))


def menu_options_user_dashboard():
    # Display tabular view of Menu Options for the user Dashboard home screen
    print("")
    print(" --------- ")
    print(" MAIN MENU ")
    print(" --------- ")

    # create a Dictionary: 'keys' as menu option texts, 'values' as corresponding action to perform
    op_1 = "Create New Expense Entry"
    op_2 = "View Last 10 Entries"
    op_3 = "View Entries By Txn Date Range"
    op_4 = "Edit/Delete Expense Entry"
    op_5 = "View Expense Report"
    op_6 = "Logout / Exit"

    menu_dict = {op_1: ["Press '1' and Enter"],
                 op_2: ["Press '2' and Enter"],
                 op_3: ["Press '3' and Enter"],
                 op_4: ["Press '4' and Enter"],
                 op_5: ["Press '5' and Enter"],
                 op_6: ["Press '6' and Enter"]
                 }
    # display menu dict. in tabular format
    print(tabulate(menu_dict, headers="keys"))


def menu_options_txn_category():
    # Display Txn Category menu options for New Expense entry
    # return: menu_dict

    # create a Dictionary: 'keys' as menu option texts, 'values' as corresponding Categories
    menu_dict = {"1": "Child Care",
                 "2": "Fuel/ Petrol",
                 "3": "Groceries",
                 "4": "Health Care/ Medical",
                 "5": "Housing",
                 "6": "Insurance",
                 "7": "Memberships/ Subscriptions",
                 "8": "Other Debt Payments",
                 "9": "Personal/ Household",
                 "10": "Travel/ Transportation",
                 "11": "Utilities (Electricity/Water/Gas)"
                 }

    # print menu to user
    # split display in half for clear formatted view (use dictionary length)
    # initialize index to 0
    index = 0
    for key, value in menu_dict.items():
        print(key, value, sep=" -> ", end=" \t ")
        index += 1
        if index > (len(menu_dict) // 2):
            print("")
            index = 0  # reset index to 0, to avoid repetitive printing of blank lines

    # return Txn Category menu options dict.
    return menu_dict


def menu_options_modify_txn():
    # Display menu options to the user to Edit / Delete an Expense Entry
    # create a Dictionary: 'keys' as menu option texts, 'values' as corresponding action to perform
    op_1 = "Edit Txn Date"
    op_2 = "Edit Txn Amount"
    op_3 = "Edit Txn Category"
    op_4 = "Edit Merchant Name"
    op_5 = "Edit Txn Country"
    op_6 = "Delete Expense Txn"

    menu_dict = {op_1: ["Press '1'"],
                 op_2: ["Press '2'"],
                 op_3: ["Press '3'"],
                 op_4: ["Press '4'"],
                 op_5: ["Press '5'"],
                 op_6: ["Press '6'"]
                 }
    # display menu dict. in tabular format
    print(tabulate(menu_dict, headers="keys"))


def menu_options_expense_summary():
    # Display menu options to the user to View Expense Summary reports

    # create a Dictionary: 'keys' as menu option texts, 'values' as corresponding action to perform
    op_1 = "View Summary for Current Month"
    op_2 = "View Summary for Previous Month"
    op_3 = "View Summary by Date Range"
    op_4 = "View Graphical Summary of Expenses"

    menu_dict = {op_1: ["Press '1' and Enter"],
                 op_2: ["Press '2' and Enter"],
                 op_3: ["Press '3' and Enter"],
                 op_4: ["Press '4' and Enter"]
                 }
    # display menu dict. in tabular format
    print(tabulate(menu_dict, headers="keys"))


def valid_username(username):
    """
    validate username entered by the user and return True if valid, else False
    check for:
    1) username is not blank,
    2) at least 2 chars long,
    3) starts with an alphabet,
    4) no blank spaces in between
    5) verify Username already doesn't exist in User Profiles db
    """

    if len(username) == 0:
        print("Username cannot be blank. Please try again.\n")
        return False
    elif len(username) < 2:
        print("Username is too short. It must be minimum 2 chars long. Please try again.\n")
        return False
    elif not username[0].isalpha():
        print("Username must begin with an alphabet. Please try again.\n")
        return False
    elif " " in username:
        print("Username cannot have blank spaces in between characters. Please try again.\n")
        return False
    elif verify_username(username):  # call helper function to check if username already registered
        print("Username already exists! Please try with another username.\n")
        return False
    else:
        return True


def valid_password(passwd):
    # validate password entered by the user and return True if valid, else False
    # check for: not blank, is at least 3 chars long

    if len(passwd) == 0:
        print("Password cannot be blank. Please try again. \n")
        return False
    elif len(passwd) < 3:
        print("Password is too short. It must be minimum 3 chars long. Please try again.")
        return False
    else:
        return True


def valid_name(name):
    # validate user input for Name and return True if valid, else False
    # check for: not blank, is at least 2 chars long, is alphabets only

    if len(name) == 0:
        print("Name cannot be blank. Please try again.")
        return False

    elif len(name) < 2:
        print("Name is too short. It must be minimum 2 chars long. Please try again.")
        return False

    elif " " not in name and not (name.isalpha()):
        print("Name must be alphabets only. Please try again.")
        return False
    else:
        return True


def format_name(name):
    # formats the name by removing excessive blank spaces in between first and last names

    # if user enters one or more blank spaces in between texts, like first name and last name
    # Ex - J D
    full_name = name.split()  # split the text into sub-strings, removing blank space
    name = ""  # initialize name variable to blank string
    for text in full_name:
        name += text + " "

    return name.strip()


def valid_email_signup(email):
    """
    Validate user input for Email entry at the time of New User signup.
    Check for -
    1) regular email expression
    2) email already present in user profiles, that is, a User already exists with that email
    :param email: string type
    :return: True if email input is valid, else False
    """

    # check for regular email expression
    # Make a regular expression for validating an Email
    # Note: source code obtained from "https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/"
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    # pass the regular expression and the email string into the fullmatch() method
    if re.fullmatch(regex, email):
        if verify_email(email):  # check if email already exists in user profiles database
            print("Email already registered. Please try again.")
            return False
        else:
            return True
    else:
        print("Invalid Email\n")
        return False


def valid_country(country):
    # validate user input for this Optional field, and return True if valid, else False
    # Note: blank entry is accepted for this optional field, and will be replaced with "none_given"
    if country == "":
        return True
    elif not country.isalpha():
        print("Invalid entry. Country name can be alphabets only.\n")
        return False
    else:
        return True


def valid_txn_date(date_input):
    """
    validate user input for correct Date as per format 'yyyy-mm-dd'
    :param date_input: string type
    :return: True, if date input is valid, else False
    """
    # Note: source code for this functionality has been taken from:
    # https://discuss.python.org/t/best-way-to-validate-an-entered-date/49406
    # courtesy of user: Clint Hepner
    try:
        datetime.strptime(date_input, '%Y-%m-%d')
        return True
    except ValueError:
        print("Invalid date. Please follow correct 'yyyy-mm-dd' format, and try again\n")
        return False


def user_signup():
    """
    Sets up a New User for the app.
    Collects all relevant data for setting up a user profile.
    Validation helper functions are called for each data field input.
    After sign up is complete, new user is created in the database with a helper function,
    and program flow moves to user Dashboard display.
    """
    # ---------------
    # NEW USER SIGNUP
    # ---------------
    # mandatory fields - username, password, name, email
    # optional fields - country

    clear_terminal()
    display_header()

    print("--- New User SIgn Up --- \n")

    # prompt user to enter a username that matches a given criteria
    print("Please note:")
    print("-> username must be minimum 2 characters long\n-> must begin with an alphabet\n-> cannot have blank spaces")
    username = input("Please enter a username: ").strip()
    # validate username with a helper function, and keep prompting user to enter a valid username
    while not valid_username(username):
        username = input("Please enter a username: ").strip()

    # prompt user to enter a password that matches the given criteria
    print("")
    print("Please note:\n-> password must be minimum 3 characters long")
    passwd = input("Please enter a password: ").strip()
    # validate password
    while not valid_password(passwd):
        print("")
        passwd = input("Please enter a password: ").strip()

    print("\nGreat! You now have a username / password. Let's get your Name and Email, and you're all set!\n")

    # prompt user to enter their Name that matches a given Criteria
    print("Please note:\n-> Name must be minimum 2 characters long\n-> must be alphabets only")
    name = input("Please enter your Name: ").strip()

    # validate Name input
    while not valid_name(name):
        print("")
        name = input("Please enter your Name: ").strip()

    # format name if required, for a valid name input
    # this helper function will remove excess blank spaces between name texts
    if " " in name:
        name = format_name(name)

    # prompt user to enter their Email that matches a given Criteria
    print("")
    print("Please share a valid Email. Don't worry, we won't spam your inbox!")
    email = input("Please enter your Email: ").strip()
    # validate Email input
    while not valid_email_signup(email):
        email = input("Please enter your Email: ").strip()

    # prompt user to enter their Country - this is an Optional field
    print("")
    print("Hey", name, "!", "We'd love to know what country you're from!")

    print("\nTo skip, please press Enter. Please do not input any special characters. ")
    country = input("Please enter your Country: ").strip()
    # validate Country input
    while not valid_country(country):
        print("")
        country = input("Please enter your Country: ").strip()

    # if country is blank, update country to reflect "none_given" in user profile.
    if country == "":
        country = "none_given"

    print("\nAwesome! You are all set.")
    input("Press ENTER and Head straight to Dashboard...")

    # save new user data to a list
    new_user = [username, passwd, name, email, country]

    # create user entry in Users DB
    create_user_in_db(new_user)

    # display User dashboard
    display_main_menu(username)


def create_user_in_db(new_user):
    """
    Creates a new user profile entry in the database for this application.
    User profiles database is a text file, for now.
    :param new_user: list type, holds all the user data collected in the user_signup()
    """
    # ---------------------------
    # CREATE NEW USER IN DATABASE
    # ---------------------------

    # handles case - empty file, non-empty file
    # handles exception - file not found at filepath
    try:
        file_size = os.path.getsize(FILE_PATH_USERS)

        # file is empty
        if file_size == 0:

            # create user_profiles_dict
            user_profiles_dict = {"username": [],
                                  "password": [],
                                  "name": [],
                                  "email": [],
                                  "country": []
                                  }

            # populate New User data to user profiles dict
            index = 0
            for key in user_profiles_dict.keys():
                user_profiles_dict[key].append(new_user[index])
                index += 1

            # open filepath and write dictionary data to file
            with open(FILE_PATH_USERS, "w") as file:
                json.dump(user_profiles_dict, file)

        # file is Not empty
        else:
            with open(FILE_PATH_USERS, "r") as file:  # open file
                user_profiles_dict = json.load(file)  # load data from file into dictionary

                # populate new user data to user profiles dict
                index = 0
                for key in user_profiles_dict.keys():
                    user_profiles_dict[key].append(new_user[index])
                    index += 1

            with open(FILE_PATH_USERS, "w") as file:  # open file again
                json.dump(user_profiles_dict, file)  # write updated dictionary to file

    # File not found: log the error, create new file and upload user profiles data
    except FileNotFoundError as e:
        error = [e.strerror, e.filename, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]

        with open("error_logs.txt", "a") as logfile:
            for data in error:
                logfile.write(f"{data}\n")

        # create user_profiles_dict
        user_profiles_dict = {"username": [],
                              "password": [],
                              "name": [],
                              "email": [],
                              "country": []
                              }

        # populate New User data to user profiles dict
        index = 0
        for key in user_profiles_dict.keys():
            user_profiles_dict[key].append(new_user[index])
            index += 1

        # open filepath and write dictionary data to file
        with open(FILE_PATH_USERS, "w") as file:
            json.dump(user_profiles_dict, file)


def fetch_user_profiles():
    """
    Fetch All User profiles from database - and load data in a dictionary.
    This can now be used in other helper functions to:
    1) fetch user-specific data
    2) fetch column-field specific data
    :return: user profiles dictionary
    """

    try:
        with open(FILE_PATH_USERS, "r") as file:  # open user profiles database
            user_profiles_dict = json.load(file)  # load data into a dict

        return user_profiles_dict  # return user profiles dict to helper function

    except FileNotFoundError as e:
        error = [e.strerror, e.filename, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
        print("Sorry! There seems to be some error locating your data. Try again in some time.")

        # log error
        with open("error_logs.txt", "a") as logfile:
            for data in error:
                logfile.write(f"{data}\n")


def fetch_user_name(username):
    # fetch user's name from user profiles database, for given username

    # load user profiles
    user_profiles_dict = fetch_user_profiles()

    # find index of username in the usernames list
    index = user_profiles_dict["username"].index(username)

    # find 'name' for the given username
    name = user_profiles_dict["name"][index]
    return name


def verify_username(username):
    """
    Verify if given username exists in user profiles database.
    Username verification is done during -
    1) New User sign up - to see if a username already exists, and prevent duplicates
    -------------------
    2) Existing user Login - authenticate username
    -------------------
    :param username: string type - to look for match in user profiles db
    :return: True if username found in db, else False
    """
    # load user profiles
    user_profiles_dict = fetch_user_profiles()

    # populate usernames from user profiles dict
    users = user_profiles_dict["username"]

    # search for given username
    if username in users:
        return True
    else:
        return False


def verify_email(email):
    """
    fetch user's email from database, from given argument.
    :param email: string type - to look for match in user profiles db
    :return: True if email found in db, else False
    """
    # load user profiles
    user_profiles_dict = fetch_user_profiles()

    # populate emails from user profiles dict
    emails = user_profiles_dict["email"]

    # search for given email in emails list
    if email in emails:
        return True
    else:
        return False


def reset_password(email):
    """
    Allows user to reset their password, after Email verification
    :param email: string type - verified
    """

    # load user profiles
    user_profiles_dict = fetch_user_profiles()

    # find index of user's email in the emails list
    index = user_profiles_dict["email"].index(email)

    # find username and display it to the user
    username = user_profiles_dict["username"][index]
    print("Your username is: ", username)

    # prompt user to enter a password that matches the given criteria
    print("Please note:\n-> password must be minimum 3 characters long")
    passwd = input("Please enter New password: ").strip()
    # validate password
    while not valid_password(passwd):
        print("")
        passwd = input("Please enter New password: ").strip()

    # update user's password in the user profiles data
    user_profiles_dict["password"][index] = passwd

    with open(FILE_PATH_USERS, "w") as file:
        json.dump(user_profiles_dict, file)


def reset_user_login():
    """
    resets user login/password by setting up a system generated password for the user.
    """
    clear_terminal()
    display_header()

    print("You can Reset your password by entering your Email as registered during Sign up.\n")
    email = input("Please enter your email: ")

    if verify_email(email):
        reset_password(email)  # email authenticated, reset user password for this email
        print("\n Your password has been updated!")
        input("Please press Enter to proceed to Login home page...")
        main()
    else:
        print("\n Email not found! We do Not have a user registered with this email")
        input("Please press Enter to go back to Login home page...")
        main()


def fetch_user_expenses(username):
    """
    Fetch Expense Txns from database (csv file) for the give User - and load data into a pandas DateFrame
    This can now be used in other helper functions to:
    1) fetch specific Expense txns
    2) fetch column-field specific data
    :return: dataframe type - user_expenses_df
    """

    try:
        # read csv file and load it into a dataframe
        user_expenses_df = pd.read_csv(FILE_PATH_TXN)

        # subset rows with Txn entries for given username only
        user_expenses_df = user_expenses_df[user_expenses_df["Username"] == username]

        return user_expenses_df

    # csv file not found. Log error details.
    except Exception:
        print("Sorry! There seems to be some error locating your data. Try again in some time.\n")
        return None


def fetch_last_10_txns(username):
    """
    Fetch last 10 Expense txn entries for the given user
    :param username: to fetch Txns for the given username
    """
    # populate All Expense Txns for this user Only.
    user_expenses_df = fetch_user_expenses(username)

    # if there was No Exception reading into data file
    if user_expenses_df is not None:
        # get row index of last entry in the dataframe
        last_index = user_expenses_df.shape[0]

        # check for Number of rows returned, to determine further program flow:
        if last_index == 0:  # if there are 0 rows returned, user has No Txn Entries in database
            print("\n\tYou have 0 Txn Entries in our record! ")

        elif last_index > 10:  # use row indexing to filter last 10 txn entries
            display_last_10_txns(user_expenses_df[last_index - 10:])

        else:  # create a copy of the dataframe
            display_last_10_txns(user_expenses_df[:])

    # prompt user to input menu option to continue program control flow
    input("\nPress Enter to go back to Main Menu ->  ")
    # navigate to Dashboard home screen
    display_main_menu(username)


def display_last_10_txns(last_10_txn_df):
    """
     Display last 10 Expense txn entries for the given user
    :param last_10_txn_df: DataFrame with last 10 txns for the user
    """
    # show a summary (important fields) of last 10 txn entries
    summary_txn_fields = ["Txn_Date", "Txn_Amount", "MerchantName"]
    # sort Display by Txn_Date, most recent to earlier
    last_10_summary_df = last_10_txn_df[summary_txn_fields].sort_values("Txn_Date", ascending=False)

    # print(last_10_summary_df.to_string(index=False))
    print(tabulate(last_10_summary_df,
                   floatfmt=(None, '.2f', None),  # to retain decimal formating of Txn_Amount field
                   headers="keys",
                   showindex=False))

    print("\nPlease Note:")
    print("Last 10 Expense entries are displayed in order of most recent to last, and in Summary view.")
    print("To view Historical Txns by Date Range and Detailed View, go to Main Menu.")


def display_txns_by_daterange(username, daterange_expenses_df, modify_txn):
    """
    Displays Expense Txn entries in given Date Range for this user
    Additionally, displays a row number for each record if modify_txn is set to True
    For Modify Txn mode, this function will prompt user to enter a valid row number to select a row for modification
    params: username - for passing username reference to other helper functions
            daterange_expenses_df - holds Date specific Txns in dataframe,
            modify_txn - Boolean value, set to True if display Txn entries in Edit mode, else False.

    """
    # show All column fields (except Username)
    # subset a new dataframe, daterange_df
    expense_txn_fields = ["Txn_Date", "Txn_Amount", "Txn_Category", "MerchantName", "Txn_Country"]
    daterange_df = daterange_expenses_df[expense_txn_fields]

    print("")
    # print(daterange_expenses_df.to_string(index=False))

    if modify_txn:  # Display Expense entries by Row Number for easy selection and modification
        row_num = 1
        # iterate dataframe and create a New column - "modify_row"
        # to identify particular record to modify
        for label, row in daterange_df.iterrows():
            daterange_df.loc[label, "modify_row"] = row_num
            row_num += 1
        # Note: we are assigning a row number for display purposes only, and this doesn't change the original Row Index
        print(tabulate(daterange_df,
                       floatfmt=(None, '.2f', None, None, None),
                       headers="keys",
                       showindex=False))

        # call helper function to select and modify an Expense Txn
        print("\nPlease enter a Row Number to modify: ")
        print("To go back to Main Menu, just press Enter...")

        # prompt user to input menu option to continue program control flow
        user_choice = input("\nEnter your choice here: ").strip()
        if user_choice == "":
            # navigate to Main menu
            display_main_menu(username)
        else:  # check if user input is a valid Row Number, or user has pressed Enter
            # convert dataframe to nested dictionary
            daterange_expenses_dict = daterange_df.to_dict()
            # create a list of row numbers populated
            row_nums_list = []
            for values in daterange_expenses_dict["modify_row"].values():
                row_nums_list.append(str(int(values)))
            # prompt user to enter a valid row number for selection
            while user_choice not in row_nums_list:
                if user_choice == "":
                    break
                user_choice = input("Invalid input. Please enter a valid Row Number to modify: ").strip()
            # while loop breaks, user has entered a blank, or a valid row number
            if user_choice == "":
                # navigate user to Main menu
                display_main_menu(username)
            else:
                row_num = float(user_choice)
                modify_txns_by_daterange(username, daterange_expenses_dict, row_num)

    else:  # display Expense entries in View Only mode
        print(tabulate(daterange_df,
                       floatfmt=(None, '.2f', None, None, None),  # to retain decimal formating of Txn_Amount field
                       headers="keys",
                       showindex=False))

        input("\nPress Enter to go back to Main Menu... ")
        # navigate user to Main menu
        display_main_menu(username)


def fetch_txns_by_daterange(username, modify_txn=False):
    """
    Fetch Expense Txn entries for the given Date Range for this user
    params: username - to fetch Expense Txn entries for this user,
            modify_txn - Boolean value, set to True if Txn entries to display in Edit mode, else False.
    """
    # input Start Date from user
    input_msg = "\nPlease enter Start Date in 'yyyy-mm-dd' format, or Press Enter for today's date: "
    start_date = input(input_msg).strip()

    # Validate user input for Start Date, or assign current system Date
    # -----------------------------------------------------------------
    if start_date == "":
        start_date = datetime.today().strftime('%Y-%m-%d')  # assign current system date
        print(start_date)  # display Date output to user
    else:
        while not valid_txn_date(start_date):  # validate input for Date
            start_date = input(input_msg).strip()

    # input End Date from user
    input_msg = "\nPlease enter End Date in 'yyyy-mm-dd' format, or Press Enter for today's date: "
    end_date = input(input_msg).strip()

    # Validate user input for End Date, or assign current system Date
    # ---------------------------------------------------------------
    if end_date == "":
        end_date = datetime.today().strftime('%Y-%m-%d')  # assign current system date
        print(end_date)  # display Date output to user
    else:
        while not valid_txn_date(end_date):  # validate input for Date
            end_date = input(input_msg).strip()

    # Start Date cannot be Greater than End Date
    # display error msg, and prompt user how they want to proceed
    if start_date > end_date:
        print("\n\tStart Date cannot be greater than End Date.")
        print("\nPress Enter to continue...\nPress '1' and Enter to go back to Main Menu:  ")
        user_choice = input("\nEnter your choice here: ")

        if user_choice == '1':
            display_main_menu(username)  # abort, and go back to Main Menu...
        else:
            fetch_txns_by_daterange(username, modify_txn)  # call function recursively, user wants to continue...
    else:
        # populate All Expense Txns for this user Only.
        user_expenses_df = fetch_user_expenses(username)

        # Subset Expense Txns for specified Date Range from above dataframe
        daterange_expenses_df = user_expenses_df[(user_expenses_df["Txn_Date"] >= start_date) &
                                                 (user_expenses_df["Txn_Date"] <= end_date)]

        # If No Txns are present in given Date Range for this user
        if daterange_expenses_df.shape[0] == 0:
            print("\n\tYou have 0 Txns for the given Date Range!")
            input("\nPress Enter to go back to Main Menu... ")
            display_main_menu(username)

        else:
            # Display Txn entries to the user for given date range
            display_txns_by_daterange(username, daterange_expenses_df, modify_txn)


def modify_txns_by_daterange(username, daterange_expenses_dict, row_num):
    """
    Allow given user to Modify / Delete historical Expense txns, one txn at a time
    Prompts user to specify a date range to pull Txns to modify
    :params username: to fetch and modify Expense Txn entries for this user
            daterange_expense_df: to modify Expense Txn from given dictionary
            row_num: row number selected by the user to modify record
    """
    row_index = None

    # iterate the nested dictionary to find the given row number
    for key, values in daterange_expenses_dict["modify_row"].items():
        if row_num == values:
            row_index = key

    # this row index identifies the Expense Txn entry user has selected to modify
    # and corresponds to actual row index number in the Expenses database for this Txn record
    # print the Expense Txn record to the user and prompt for modification
    print("Expense Entry selected for modification: \n")
    for key, values in daterange_expenses_dict.items():
        if row_index in values and key != "modify_row":
            print(key, ":", daterange_expenses_dict[key][row_index])

    # display Expense Entry modification choices to user
    print("")
    menu_options_modify_txn()

    # prompt user to enter a valid option from the menu
    input_msg = "\nPlease enter 'Entry modification' choice here: "
    user_choice = input(input_msg).strip()

    while user_choice not in ["1", "2", "3", "4", "5", "6"]:
        user_choice = input("Invalid input. " + input_msg).strip()

    if user_choice == "1":  # EDIT TXN_DATE (mandatory field)
        txn_date = input_expense_txn_date()
        # update Txn_Date in Expense record
        daterange_expenses_dict["Txn_Date"][row_index] = txn_date

    elif user_choice == "2":  # EDIT TXN_AMOUNT (mandatory field)
        txn_amount = input_expense_txn_amount()
        # update Txn_Amount in Expense record
        daterange_expenses_dict["Txn_Amount"][row_index] = txn_amount

    elif user_choice == "3":  # EDIT TXN_CATEGORY (mandatory field)
        txn_cat = input_expense_txn_category()
        # update Expense Txn record
        daterange_expenses_dict["Txn_Category"][row_index] = txn_cat

    elif user_choice == "4":  # EDIT MERCHANT NAME (optional field)
        merchant_name = input_expense_txn_merchant_name()
        # update Expense Txn record
        daterange_expenses_dict["MerchantName"][row_index] = merchant_name

    elif user_choice == "5":  # EDIT TXN_COUNTRY (optional field)
        txn_country = input_expense_txn_country()
        # update Expense Txn record
        daterange_expenses_dict["Txn_Country"][row_index] = txn_country

    elif user_choice == "6":  # DELETE Expense Txn in database
        input_msg_del = "\nPress Enter to confirm Deletion...\nor, press any other key and Enter go to Main Menu: "
        submit = input(input_msg_del).strip()
        if submit == "":
            # call helper function to Delete Expense Txn in database, for given Row Index num
            remove_expense_entry_from_file(row_index)
            print("\nExpense entry successfully deleted from records...")
            time.sleep(1)  # purely for user experience, to see the Success msg.

        # navigate user to Main Menu
        display_main_menu(username)

    if user_choice != "6":
        # print the Updated Expense Txn record to the user and prompt for confirmation
        print("\nUpdated Expense Txn Entry:\n")
        for key, values in daterange_expenses_dict.items():
            if row_index in values and key != "modify_row":
                print(key + ":", daterange_expenses_dict[key][row_index])

        submit = input("\nPress Enter to confirm and Submit.\nor Press '1' and Enter to Edit more fields: ").strip()
        if submit == "1":
            # start over for further Editing of Expense entry
            modify_txns_by_daterange(username, daterange_expenses_dict, row_num)
        else:
            # construct a new Expense Txn entry list to save to database
            # add 'username' argument as the first element of this list
            expense_entry_list = [username]
            # iterate the nested dictionary passed as argument to this function, to retrieve the values for Txn fields
            for key, values in daterange_expenses_dict.items():
                if row_index in values and key != "modify_row":
                    expense_entry_list.append(daterange_expenses_dict[key][row_index])

            # call helper function to save the new Expense Entry in database
            update_expense_entry_in_file(expense_entry_list, row_index)

            # print success msg to user and navigate to User Dashboard home screen - Main menu
            print("\nExpense entry successfully saved in records...")
            time.sleep(1)  # purely for user experience, to see the Success msg.

            display_main_menu(username)


def remove_expense_entry_from_file(row_index):
    """
    Deletes an Expense Txn record from the data file at the given Row Index number
    param: row_index - int - to delete Txn record at this index in data file.
    """
    # read csv data file and load it into a dataframe
    user_expenses_df = pd.read_csv(FILE_PATH_TXN)

    # DELETE Expense Txn record at given Row Index
    user_expenses_df = user_expenses_df[user_expenses_df.index != row_index]

    # Write the updated Expense Entries dataframe to data file
    user_expenses_df.to_csv(FILE_PATH_TXN, mode="w", index=False)


def update_expense_entry_in_file(expense_entry_list, row_index):
    """
    Updates Expense Txn record in data file, as per the arguments received.
    params: expense_entry_list: Updated Expense Txn record stored as a List type.
            row_index: row index number of this Expense Txn record in data file for update.
    """
    # read csv data file and load it into a dataframe
    user_expenses_df = pd.read_csv(FILE_PATH_TXN)

    # construct an Expense Txn dict. from given List
    expense_txn_dict = {"Username": [],
                        "Txn_Date": [],
                        "Txn_Amount": [],
                        "Txn_Category": [],
                        "MerchantName": [],
                        "Txn_Country": []}
    item_index = 0
    for key in expense_txn_dict.keys():
        expense_txn_dict[key] = expense_entry_list[item_index]
        item_index += 1

    # update Expense Txn record at given Row Index number in the dataframe
    for key, values in expense_txn_dict.items():
        user_expenses_df.loc[row_index, key] = values

    # Sort the dataframe by Txn_Date so that final Txn entries in the data file appear in order of Txn Date
    user_expenses_df = user_expenses_df.sort_values("Txn_Date")

    # Write the sorted Expense Entries df to database
    user_expenses_df.to_csv(FILE_PATH_TXN, mode="w", index=False)


def save_expense_entry_to_file(expense_entry_list):
    """
    Save the Expense Entry to file/ database
    :param expense_entry_list: holds values for all column fields of the 'user_expenses_data' data file.
    """

    # create a DataFrame object from this Expense record List
    # note: enclosing Expense List argument within [] to make compatible for dataframe.
    expense_df = pd.DataFrame([expense_entry_list])

    try:
        # Write the new Expense Entry to database in 'Append' mode
        expense_df.to_csv(FILE_PATH_TXN, mode="a", index=False, header=False)
    except Exception:
        print("\nThere was an error appending the new Expense Txn record to data file. Please try again.")

    # read Updated csv file and load it into a dataframe
    user_expenses_df = pd.read_csv(FILE_PATH_TXN)

    # Sort the dataframe by Txn_Date so that final Txn entries in the data file appear in order of Txn Date
    user_expenses_df = user_expenses_df.sort_values("Txn_Date")

    # Write the sorted Expense Entries df to database
    user_expenses_df.to_csv(FILE_PATH_TXN, mode="w", index=False)


def create_new_expense_entry(username):
    """
    Create a new Expense entry in the database for the given user.
    'Uses Expenses' database is a csv file.
    Display a preview of the Expense entry before final submission, and
    confirm entry submission status - entry saved or display error msg.
    :param username:
    """
    # Input Expense Txn Entry data fields from user, one field at a time, validating each field's input

    # TXN_DATE (mandatory field)
    # -------------------------
    txn_date = input_expense_txn_date()
    print("")

    # TXN_AMOUNT (mandatory)
    # ----------------------
    txn_amount = input_expense_txn_amount()
    print("")

    # TXN_CATEGORY (mandatory)
    # ------------------------
    txn_cat = input_expense_txn_category()
    print("")

    # MERCHANT NAME (optional field)
    # ------------------------------
    merchant_name = input_expense_txn_merchant_name()
    print("")

    # TXN_COUNTRY (optional field)
    # ----------------------------
    txn_country = input_expense_txn_country()

    # Now that all column fields have been collected, construct Expense entry record as a List
    expense_entry_list = [txn_date, txn_amount, txn_cat, merchant_name, txn_country]

    # preview Expense Entry details to user before final submission to database
    # username is excluded for now
    print("\nExpense entry details:")
    headers_list = ["Txn_Date", "Txn_Amount", "Txn_Category", "MerchantName", "Txn_Country"]
    print(tabulate([expense_entry_list], headers=headers_list))

    # now, add username to Expense entry list at index 0, so Expense data can be updated correctly
    expense_entry_list.insert(0, username)

    submit = input("\nPress Enter to confirm Submission, or press '1' and Enter to start over: ").strip()
    if submit == "1":
        create_new_expense_entry(username)
    else:
        # call helper function to save the new Expense Entry in database
        save_expense_entry_to_file(expense_entry_list)

        # print success msg to user and navigate to User Dashboard home screen
        print("Expense entry successfully saved in records...")
        time.sleep(1)  # purely for user experience, to see the Success msg.

        display_main_menu(username)


def input_expense_txn_date():
    """
    Prompts user to enter a valid Txn_Date for the Expense entry
    This is a mandatory data field.
    return: validated txn_date value
    """
    # display accepted date format to the user, or the option to use current system date
    input_msg = ">>>> Txn Date: \nPlease enter in 'yyyy-mm-dd' format, or Press Enter to input Today's date"
    date_input = input(input_msg + "\nEnter Txn Date here: ").strip()
    if date_input == "":
        txn_date = datetime.today().strftime('%Y-%m-%d')  # assign current system date
    else:
        while not valid_txn_date(date_input):  # validate input for Date
            date_input = input(input_msg + "\nEnter Txn Date here: ").strip()

        txn_date = date_input  # update txn_date to validated user input for Date

    print("Txn Date as entered is:", txn_date)
    return txn_date


def input_expense_txn_amount():
    """
    Prompts user to enter a valid Txn Amount for the Expense entry.
    This is a mandatory data field.
    return: validated Txn_Amount value
    """
    input_msg = ">>>> Txn Amount: \nPlease enter a number"
    txn_amount = None  # initialize txn_amount to None
    while txn_amount is None:
        try:
            amt_input = input(input_msg + "\nEnter Txn Amount here: ").strip()
            txn_amount = float(amt_input)
        except ValueError:
            print("Invalid input. Please enter a number")

    return txn_amount


def input_expense_txn_category():
    """
    Prompts user to enter a valid Txn Category from a given list of categories.
    This is a mandatory data field.
    return: validated Txn_Category value
    """
    print(">>>> Txn Category: \nPlease enter an option from below Categories menu")

    # load and display Categories menu options
    # this helper functions returns a dict type of menu options
    cat_menu_dict = menu_options_txn_category()

    cat_input = input("\n\nEnter Category choice here: ").strip()

    # prompt user to enter a valid category option
    while cat_input not in cat_menu_dict:
        # prompt user to input a valid category option
        print("Invalid input. Please enter a valid Category option from the menu.")
        cat_input = input("\nEnter Category choice here: ").strip()

    # category option input by the user is validated
    # assign value to txn_cat variable
    txn_cat = cat_menu_dict[cat_input]

    return txn_cat


def input_expense_txn_merchant_name():
    """
    Prompts user to enter a valid Merchant Name for the Expense entry.
    This is an optional data field, and can be left Blank.
    return: validated Merchant Name or "none_given" if intended to be left blank.
    """
    input_msg = ">>>> Merchant Name: \nThis is an optional field, you may leave blank and press Enter"
    merchant_name = input(input_msg + "\nEnter Merchant Name here: ").strip()
    if merchant_name == "":
        merchant_name = "none_given"  # update value to indicate Not Available, for a blank input

    return merchant_name


def input_expense_txn_country():
    """
    Prompts user to enter a valid Txn Country name for the Expense entry.
    This is an optional data field, and can be left Blank.
    return: validated Country name or "none_given" if intended to be left blank.
    """
    input_msg = ">>>> Txn Country Name: \nThis is an optional field, you may leave blank and press Enter"
    txn_country = input(input_msg + "\nEnter Txn Country name here: ").strip()
    # validate user input for blank and non-blank values
    # Note: blank will be accepted for this optional field
    while not valid_country(txn_country):
        txn_country = input(input_msg + "\nEnter Txn Country name here: ").strip()

    if txn_country == "":  # update blank input to show "none_given" in database
        txn_country = "none_given"

    return txn_country


def display_expense_summary_daterange(username, start_date, end_date):
    """
    Displays Expense summary to the user for the current month
    param:  username - to load All Expense Txns for the given user, and all Column fields
            date_range - tuple type (start_date, end_date) - to retrieve Expense Txns within given date range
    """
    # load ALl expense txns for this user
    user_expenses_df = fetch_user_expenses(username)

    # check if function call is for previous month's summary
    if start_date is None:
        # re-structure Start Date
        # -----------------------
        month = int(datetime.today().strftime('%m'))  # get month from current date
        prev_month = str(month - 1)
        prev_month = "0" + prev_month
        year = datetime.today().strftime('%Y')  # get year from current date
        start_date = year + "-" + prev_month + "-01"  # note: day will always be "01" in this case

    # subset DataFrame for given date range (Note: End Date is Not inclusive)
    daterange_expenses_df = user_expenses_df[(user_expenses_df["Txn_Date"] >= start_date) &
                                             (user_expenses_df["Txn_Date"] <= end_date)]

    # check if there is at least 1 Expense record in database for this user
    # for the given date range
    if daterange_expenses_df.shape[0] == 0:
        print("\n\t You have 0 Txns for this Time Period. Please press Enter to go back to main menu... ")

    else:  # display Expense Summary
        print("\nExpense Summary for the Period: ", start_date, "to", end_date)

        # generate pivot table summarizing Total Txn Amount, and Max
        expense_pivot = daterange_expenses_df.pivot_table(
            values="Txn_Amount",
            index="Txn_Category",
            aggfunc=["count", "sum", "mean", "max"])  # in-built pandas functions passed as string literals,

        # expense_pivot["sum"] refers to the column field as returned from aggregate function sum() above.
        # Add a column that displays Txn amounts total for categories as a Proportion (%age) of Total Expenditure
        expense_pivot["%age_of_total"] = (expense_pivot["sum"] / expense_pivot["sum"].sum()) * 100

        print("")
        headers_list = ["Txn_Category", "Total Txns.", "Total Txn_Amount",
                        "Average Txn_Amount", "Maximum Txn_Amount", "Percent Proportion of Total"]

        print(tabulate(expense_pivot, headers=headers_list, floatfmt=(None, '.0f', '.2f', '.2f', '.2f', '.1f')))

        # calculate Sum total of Expenses across all categories, for the given date range
        total_expense = round(daterange_expenses_df["Txn_Amount"].sum(), 2)
        print("\nTotal Expenditure for the Period: ", total_expense)
        print("--------------------------------------------")


def generate_expense_reports(username):
    """
    Display Expense summary reports for the given user.
    Additionally, user can select a type of summary report to show, from a set menu option.
    param: username - to access Expense Txns for the given user
    """
    print("\t-----------------------")
    print("\tExpense Summary Reports")
    print("\t-----------------------")

    # display summary report options to choose from
    menu_options_expense_summary()

    # Group data by Txn Category, and show sum for Txn_Amount
    # also sort this data by value in descending order
    input_msg = "\nPlease enter your choice for Summary Report, or just press Enter to go back to Main Menu: "
    user_choice = input(input_msg).strip()
    while user_choice not in ("1", "2", "3", "4"):
        if user_choice == "":
            break
        user_choice = input("\nInvalid input. Please enter a valid Summary Report choice: ").strip()

    if user_choice == "":
        # navigate user to Main Menu / User Dashboard Home screen
        display_main_menu(username)

    # user selected a valid menu option for Summary reports
    else:
        if user_choice == "1":
            # display Expense Summary for Current month
            # -----------------------------------------
            # start date is day 1 of curr month
            start_date = datetime.today().strftime('%Y-%m-01')

            # end date is current date + 1 day,
            # because helper func. sub-sets data from database Up To End Date (End Date not included)
            # Note: datetime.timedelta(days) -> increments given date by N days.
            end_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

            # call helper function to display Expense Summary report for the given date range
            display_expense_summary_daterange(username, start_date, end_date)

        elif user_choice == "2":
            # display Expense Summary for Previous month
            # -----------------------------------------
            # set start date to None
            # this will be constructed in the helper function from current system date
            start_date = None

            # End Date will be 'N' days before current system date
            # where 'N' is day of current date.
            days_curr_date = int(datetime.today().strftime('%d'))
            end_date = (datetime.today() - timedelta(days=days_curr_date)).strftime("%Y-%m-%d")

            # call helper function to display Expense Summary report for the given date range
            display_expense_summary_daterange(username, start_date, end_date)

        elif user_choice == "3":
            # display Expense Summary for specified Date Range
            # ------------------------------------------------
            # input Start Date from user
            print("\nEnter Start Date for Txn")
            start_date = input_expense_txn_date()
            # input End Date from user
            print("\nEnter End Date for Txn")
            end_date = input_expense_txn_date()

            # Start Date cannot be Greater than End Date
            # display error msg
            if start_date > end_date:
                print("\n\tStart Date cannot be greater than End Date.")
            else:
                # call helper function to display Expense Summary report for the given date range
                display_expense_summary_daterange(username, start_date, end_date)

        elif user_choice == "4":
            # display Graphical Visualization of Expense Summary
            # ------------------------------------------------
            print("\nThis functionality is currently under maintenance...check back soon!")

        input("\nPress Enter to go back to Summary Report menu...")
        # clear our console and display App header
        clear_terminal()
        display_header(username)
        generate_expense_reports(username)  # call function recursively


def valid_login(username, passwd):
    """
    Loads user profiles from database and checks if username/password combination is a match.
    :param username: string type - as input by the user
    :param passwd: string type - as input by the user
    """
    # -------------------------------
    # VALIDATE USER LOGIN CREDENTIALS
    # -------------------------------

    # access user profiles data file to validate username/password
    try:
        with open(FILE_PATH_USERS) as file:
            user_profiles_dict = json.load(file)

        # check if given username is present in the users list
        if username in user_profiles_dict["username"]:
            # find index of username in list, so we can retrieve corresponding password from passwords list
            index = user_profiles_dict["username"].index(username)
            # check is password is a match
            if user_profiles_dict["password"][index] == passwd:
                print("Successful login!!")
                return True
            else:
                print("Password is incorrect. Please try again.\n")
                return False
        # username not found in database
        else:
            print("Username is incorrect. Please try again.\n")
            return False

    except FileNotFoundError as e:
        error = [e.strerror, e.filename, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
        print("Sorry! There seems to be some error locating your data. Try again in some time.")

        # log error
        with open("error_logs.txt", "a") as logfile:
            for data in error:
                logfile.write(f"{data}\n")


def secure_password_input(prompt=""):
    """
    prompts user for a Password (against a given prompt) and Masks the user input with an asterisk, '*'
    param: prompt - str type - prompt message to show to user, default is a blank prompt.
    return: password string as input by the user
    """
    pwd_str = ""
    proxy_string = [" "] * 20
    while True:
        sys.stdout.write('\x0D' + prompt + "".join(proxy_string))
        c = msvcrt.getch()
        if c == b'\r':
            break
        elif c == b'\x08':
            pwd_str = pwd_str[:-1]
            proxy_string[len(pwd_str)] = " "
        else:
            proxy_string[len(pwd_str)] = "*"
            pwd_str += c.decode()

    sys.stdout.write('\n')
    return pwd_str


def user_login():
    """
    Landing page of the app.
    User must log in or create new user account to access app features.
    Allows user to access dashboard by entering their username/password, OR
    Allows a New user to set up their account, and log in to dashboard.
    """
    # display Login menu options to user on the app. home screen
    # Existing user login / New User signup
    menu_options_user_login()

    print("")
    # input user choice
    user_choice = input("Enter your choice here: ").strip()

    # validate user choice input
    while user_choice != "1" and user_choice != "2":
        user_choice = input("Invalid choice. Please press either '1' or '2': ")

    # decide further course of program flow, depending on '1' or '2'

    # --------------------------
    # '1' -> Existing user login
    # --------------------------
    if user_choice == '1':
        print("")
        print("--- User Dashboard Login --- \n")
        username = input("Enter username: ").strip()
        # prompt if username input is blank
        while username == "":
            print("Username cannot be blank. Please enter again\n")
            username = input("Enter username: ").strip()

        # passwd = input("Enter password: ").strip()
        passwd = secure_password_input("Enter password: ")

        turn = 3
        # authenticate user login and allow 3 more attempts
        while not valid_login(username, passwd):
            # user has exceeded maximum login attempts. Reset user credentials
            # allow user to either Reset login credentials, or exit to Login home page.
            if turn == 0:
                print("You have exceed maximum attempts for login!\n")
                print("Please press 'Y' and Enter to Reset your login credentials..")
                print("Please press 'N' and Enter to Exit to app Login")
                choice = input().strip().lower()
                if choice == "y":  # turn = 0, break while loop and reset login
                    turn = -1
                    break
                else:
                    turn = -2  # set turn = -1, break, and navigate to main()
                    break

            if turn == 1:  # user has 1 last attempt to login
                print("This is your final login attempt. You will need to reset your password after this.\n")

            else:  # prompt user to try again with login credentials
                print(f"You have {turn} more attempts.\n")

            username = input("Enter username: ").strip()
            # passwd = input("Enter password: ").strip()
            passwd = secure_password_input("Enter password: ")
            turn -= 1  # Note: turn will equal 0 if user successfully authenticates on 3rd attempt.

        # while loop breaks when user login is authenticated or user exceeds max login attempts
        if turn == -1:  # user intends to reset login credentials
            reset_user_login()
        elif turn == -2:  # user intends to exit to Login home page
            main()
        else:
            # user has successfully validated login
            # take user to Home screen / Dashboard
            display_main_menu(username)

    # ------------------------------
    # '2' -> New User account set up
    # ------------------------------
    else:
        user_signup()


def display_main_menu(username):
    """
    Display user Dashboard. This function works as a Home screen for the user.
    User can now navigate the Main menu and perform tasks.
    :param username: to access user's data from the database files
    """
    # clear our console and display App header
    clear_terminal()
    display_header(username)

    # display Menu Options for User Dashboard home screen
    menu_options_user_dashboard()

    # input user choice
    print("")
    user_choice = input("Enter your choice here: ").strip()

    # validate user choice input for menu options
    while user_choice not in ("1", "2", "3", "4", "5", "6"):
        print("\nYou entered an invalid option.")
        user_choice = input("Please enter a valid Menu option: ").strip()

    # control program flow as per user choice
    if user_choice == "1":  # New Expense Entry
        # clear our console and display App header
        clear_terminal()
        display_header(username)

        print("\t------------------")
        print("\tNew Expense Entry")
        print("\t------------------")
        # redirect to helper function to create a new expense entry
        create_new_expense_entry(username)

    elif user_choice == "2":  # View Last 10 Entries
        # clear our console and display App header
        clear_terminal()
        display_header(username)

        print("\t-----------------------")
        print("\tLast 10 Expense Entries")
        print("\t-----------------------")
        print("")
        # redirect to helper function to display last 10 expense entries
        fetch_last_10_txns(username)

    elif user_choice == "3":  # View Entries By Txn Date Range
        # clear our console and display App header
        clear_terminal()
        display_header(username)

        print("\t---------------------------------")
        print("\tExpense Entries By Txn Date Range")
        print("\t---------------------------------")
        # redirect to helper function to display Txn Entries by Date Range
        fetch_txns_by_daterange(username, modify_txn=False)

    elif user_choice == "4":  # Edit/Delete Previous Expense Entry
        # clear our console and display App header
        clear_terminal()
        display_header(username)

        print("\t---------------------------------")
        print("\tModify Previous Expense Txns")
        print("\t---------------------------------")
        # redirect to helper function to display Txn Entries by Date Range
        fetch_txns_by_daterange(username, modify_txn=True)

    elif user_choice == "5":  # View Expense Report
        # clear our console and display App header
        clear_terminal()
        display_header(username)

        # redirect to helper function to display expense summary reports
        generate_expense_reports(username)

    elif user_choice == "6":  # Log Out / Exit
        print("Logging off...")
        time.sleep(1)
        main()


def main():
    # Main Execution Function of the program
    clear_terminal()
    display_header()  # display App name, version,

    user_login()  # Login home screen


if __name__ == "__main__":
    main()
