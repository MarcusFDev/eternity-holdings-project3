"""
This is the Eternity Holdings functionality file, run.py.
Contains but not limited to functions that:

-Allows Users to Create a account.
-Accesses and can edit Google Sheets as a database.
-Allows Users to Login to an account they created.
-Users can Log Out of an account.
-Allows users to Deposit & Withdraw funds into their account.
"""

from colorama import init, Fore, Style
import os
import datetime
import random
from money import Money

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Eternity Holdings')

ACCOUNTLIST = SHEET.worksheet('accountlist')

# Initialize Colorama to work with ANSI escape sequences
init()


def clear():
    """
    Clear function to clean-up the terminal window so the User has
    a better visual on the terminal content that is most relevant.
    """
    os.system("cls" if os.name == "nt" else "clear")


def update_sheet_data(first_name,
                      last_name,
                      date_of_birth,
                      nine_digit_num,
                      four_digit_num,
                      starting_bal,
                      worksheet):
    """
    Updates Google Sheet with user Inputed data.
    -Creates list of data to send to sheet.
    -Converts starting_bal value to a string.
    """
    # Converts values to shorter & approriate value names
    fname = first_name
    lname = last_name
    bdate = date_of_birth
    acc_num = nine_digit_num
    pin_num = four_digit_num
    # Converts Money value to string
    starting_balance = str(starting_bal)
    # Grabs the worksheet to send data to
    worksheet_to_update = SHEET.worksheet('accountlist')
    # Creates a list for the Values
    row_data = [fname, lname, acc_num, pin_num, bdate, starting_balance]
    # Updates worksheet with the new data
    worksheet_to_update.append_row(row_data)


def get_sheet_data(column_index):
    """
    Checks the Account sheet Data. Finds
    values found in Google sheet.
    Sends those values to where the function was called.
    """
    account_list_sheet = SHEET.worksheet('accountlist')

    column_values = account_list_sheet.col_values(column_index)
    # Collects all column values after the first row
    column_values = column_values[1:]
    # Returns the column data to where this function was called.
    return column_values


def number_generator(first_name, last_name, date_of_birth, column_values):
    """
    Generates random 4 and 9 digit number.
    Calls get_sheet_data function to collect data
    from Google Sheet. Coverts the data to integers.

    Checks generated numbers with sheet data to
    prevent duplicates, generates Account balance
    & Calls update_sheet function.
    """
    # Collects Sheet Data from Columns 3 and 4 & converts them to integers.
    exist_acc_num = [int(value) for value in get_sheet_data(3) if value]
    exist_pin_num = [int(value) for value in get_sheet_data(4) if value]

    while True:
        # Generates a random 9 digit number.
        nine_digit_num = random.randint(100000000, 999999999)
        # Generates a random 4 digit number.
        four_digit_num = random.randint(1000, 9999)

        # Checks if generated num already exists in Google sheet.
        if (nine_digit_num not in exist_acc_num) and \
           (four_digit_num not in exist_pin_num):
            print(Fore.GREEN + "Creating your new Account"
                               " with Eternity Holdings...")
            print(Fore.YELLOW + "These are your Account details:\n")
            print(Style.RESET_ALL + f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Date of Birth: {date_of_birth}")
            print("\nYour New Account Number:", nine_digit_num)
            print("Your New Account PIN Number:", four_digit_num)
            print(Fore.RED + "\nPlease take note of these details as"
                             " you will need them to access your Account"
                             " in Login.")

            starting_bal = Money(amount='0.00', currency='EUR')
            update_sheet_data(first_name, last_name, date_of_birth,
                              nine_digit_num, four_digit_num,
                              starting_bal, 'accountlist')
            break


def acc_create_finished():
    """
    After the Account details are printed to the terminal
    """
    print(Fore.YELLOW + "When you're ready,"
          " Please enter 'PROCEED' to return to the Main Menu.\n")
    valid_mode_input = ["PROCEED"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "PROCEED":
                print(Fore.GREEN + "Returning to Main Menu...")
                clear()
                login_or_create()


def acc_create_confirm(first_name, last_name, date_of_birth):
    """
    Allows the user to confirm their First & Last name
    and their DOB. Giving the user the option to return if
    they made a mistake.
    """

    print(Fore.YELLOW + "\nHere are your entered details:")
    print(Style.RESET_ALL + f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Date of Birth: {date_of_birth}")

    print(Fore.YELLOW + "\nAre these details correct?"
                        " Please Confirm YES or NO")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.CYAN + f"Thank you {first_name} for your"
                                  " confirmation.\n")
                number_generator(first_name, last_name, date_of_birth)
                acc_create_finished()

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "No problem. Lets go back...")
                create_account()

            break


def create_account():
    """
    Collects DOB, First and Last Name data from user input.
    Calls validate_dob fuction if True code breaks, if false
    while loop restarts.
    """
    print(Fore.YELLOW + "Welcome to the Account Creator.")
    print(Fore.CYAN + "You're now at the Account Creation Terminal.\n")

    first_name = input(Style.RESET_ALL + "Please Enter First Name:\n")

    last_name = input("Please Enter Last Name:\n")

    print(Fore.RED + "NOTICE: You must be 18+ to Create an Account\n")

    while True:
        date_of_birth = input(Style.RESET_ALL + "Please Enter Date of Birth in"
                              " the format (YYYY-MM-DD):\n")
        # Calls Date of Birth Validation function
        if validate_dob(date_of_birth, first_name):
            clear()
            acc_create_confirm(first_name, last_name, date_of_birth)
            break
        else:
            print(Fore.RED + "Please Try Again.\n")


def validate_dob(date_of_birth, first_name):
    """
    Validates user input for date.
    Checks user input to be over the Age of 18,
    -If the input is Valid and over 18 code returns true value.
    -If the input is Valid but under 18 code returns to start.
    -If the input is inValid, returns false value.
    """
    try:
        # Formats User Date Input
        birth_date = datetime.datetime.strptime(date_of_birth,
                                                "%Y-%m-%d").date()
        # Collects Current Date
        current_date = datetime.date.today()
        # Calculates Age by subtracting User Input with Current Date
        age = current_date.year - birth_date.year - (
            (current_date.month, current_date.day) <
            (birth_date.month, birth_date.day))
        # Checks if Age is greater or equal to 18
        if age >= 18:
            return True
        else:
            clear()
            print(Fore.RED + f"Sorry {first_name}, you must be 18 or older"
                  " to create an account with us.\n")
            login_or_create()

    except ValueError:
        clear()
        print(Fore.RED + f"Sorry, your date input '{date_of_birth}'"
              " was incorrectly formatted.")
        return False


def login_user_bal(acc_num):
    """
    Checks current logged in accounts
    balance from Google Sheet and prints
    result to Terminal.
    """
    acc_num_list = get_sheet_data(3)
    acc_bal_list = get_sheet_data(6)

    logged_in_user = acc_num_list.index(acc_num)
    current_acc_bal = acc_bal_list[logged_in_user]

    print(Fore.GREEN + "Your Account Balance is:", current_acc_bal)


def acc_depo_term(fname, acc_num):
    """
    Account Deposit Terminal.
    """
    clear()
    print(Fore.YELLOW + "Welcome to Eternity Holdings deposit terminal")
    login_user_bal(acc_num)

    print(Fore.RED + f"Sorry {fname} this feature is unfinished!"
                     " Returning to HUB...\n")
    logged_in_hub(fname, acc_num)


def acc_withdraw_term(fname, acc_num):
    """
    Account Withdraw Terminal.
    """
    clear()
    print(Fore.YELLOW + "Welcome to Eternity Holdings withdraw terminal")
    print(Fore.RED + f"Sorry {fname} this feature is unfinished!"
                     " Returning to HUB...\n")
    logged_in_hub(fname, acc_num)


def acc_logout_confirm(fname, acc_num):
    """
    Allows the user to return if they
    did not want to logout
    """
    print(Fore.YELLOW + f"{fname} are you sure you want to Log Out?\n")
    print(Style.RESET_ALL + "Please Enter 'YES' or 'NO'")
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.GREEN + "Remember to spend Responsibly"
                                   " & Have an amazing day.")
                print(Fore.RED + "You are safely being logged out.\n")
                login_or_create()

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "Returning back...\n")
                logged_in_hub(fname, acc_num)


def logged_in_hub(fname, acc_num):
    """
    The Eternity Holding's main HUB
    """
    print(Fore.YELLOW + f"\nWelcome {fname} you are now"
                        " at the Eternity Bank HUB.")
    print(Fore.CYAN + "From here you have access to all our services."
          " See below for our current available options:\n")

    print(Style.RESET_ALL + "Enter 'DEPOSIT' to go to"
                            "the Deposit funds terminal.")
    print("Enter 'WITHDRAW' to go to the Withdraw funds terminal.")
    print("Enter 'BALANCE' to check your current account balance.")
    print("Enter 'LOGOUT' to go back to the Main Menu.\n")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["DEPOSIT", "WITHDRAW", "BALANCE", "LOGOUT"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()

        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "DEPOSIT":
                clear()
                print("Going to the Deposit terminal!\n")
                acc_depo_term(fname, acc_num)

            elif mode_str == "WITHDRAW":
                clear()
                print("Going to the Withdraw terminal!\n")
                acc_withdraw_term(fname)

            elif mode_str == "BALANCE":
                clear()
                print(Fore.CYAN + f"Hello {fname} see below for your balance:")
                login_user_bal(acc_num)
                logged_in_hub(fname, acc_num)

            elif mode_str == "LOGOUT":
                clear()
                acc_logout_confirm(fname)

            else:
                print(f"The Input of {mode_str} is incorrect.")


def login_account():
    """
    Collects User input for their Account.
    In the if statement it calls the locate_acc function,
    to compare user input with stored data.

    -If True the loop breaks and calls logged_in_menu.
    -If False it returns user to the start.
    """
    print(Fore.YELLOW + "Welcome to the Account Login.")
    print(Fore.CYAN + "You're now at the Account Login Terminal.\n")

    while True:
        # Assigns a variable to each user input
        fname = input(Style.RESET_ALL + "Please Enter First Name:\n")
        lname = input("Please Enter Last Name:\n")
        acc_num = input("Please Enter Account Number:\n")
        pin_num = input("Please Enter the Account Pin number:\n")

        # Calls function and gives it the input values
        if locate_acc(fname, lname, acc_num, pin_num):
            clear()
            print(Fore.GREEN + "You have Successfully logged in.\n")
            logged_in_hub(fname, acc_num)
            break
        else:
            clear()
            print(Fore.RED + "Sorry your search does not match"
                  " any Account in our database.")
            print("Returning to Main menu...\n")
            login_or_create()


def locate_acc(fname, lname, acc_num, pin_num):
    """
    Extracts corresponding data from worksheet.
    Creates a list of the data. Compares the data,
    with user input.
    - If the values match, returns True.
    - If not, returns False.
    """
    account_list_sheet = SHEET.worksheet('accountlist')
    # Collects all row data
    all_rows = account_list_sheet.get_all_values()
    # Iterate over each row in the sheet excluding the title row
    for row in all_rows[1:]:
        # Extract each data from the row in order
        sheet_fname, sheet_lname, sheet_acc_num, sheet_pin_num = row[:4]

        # Check if all the user input matches the data in the sheet
        if (
            fname == sheet_fname and
            lname == sheet_lname and
            acc_num == sheet_acc_num and
            pin_num == sheet_pin_num
        ):

            return True

    return False


def login_or_create():
    """
    Gets User string input.
    Run a while loop to collect a valid string from user
    via the terminal, which must be the correct value of
    'Create' or 'Login'. The loop will repeat until input is valid.
    """
    print(Fore.YELLOW + "Welcome to the Main Menu.")
    print(Fore.CYAN + "You're now at the Create & Login Terminal.\n")
    print(Style.RESET_ALL + "To proceed with your banking experience,"
          " please choose 'CREATE' or 'LOGIN'.")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["CREATE", "LOGIN"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "CREATE":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} an Account!")
                print("Sending to Account Creator...\n")
                create_account()

            elif mode_str == "LOGIN":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to an Account!")
                print("Sending to Account Login...\n")
                login_account()

            break


def validate_mode(mode_str, valid_mode_input):
    """
    Checks if the value of mode_str is found in
    the valid_modes list.
    -If the value is found, it returns True.
    -If the value is not, it prints a statement and returns False.
    """
    # Checks if string equals to the respective values
    if mode_str in valid_mode_input:
        return True
    else:
        print(Fore.RED + f"Wrong User input of '{mode_str}' detected,"
              "this is incorrect. Please try again.")
        return False


def main():
    """
    Run all program functions.
    """
    login_or_create()


if __name__ == "__main__":
    print(Fore.YELLOW + "\nEternity Holdings the #1 App"
          " to automate your banking needs!\n")
    main()
