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
import re
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
                      user_bal,
                      worksheet):
    """
    Updates Google Sheet with user Inputed data.

    -Creates list of data to send to sheet.
    -Converts user_bal value to a string.
    """
    # Converts values to shorter & approriate value names
    fname = first_name
    lname = last_name
    bdate = date_of_birth
    acc_num = nine_digit_num
    pin_num = four_digit_num
    # Converts Money value to string
    user_balance = str(user_bal)
    # Grabs the worksheet to send data to
    worksheet_to_update = SHEET.worksheet('accountlist')
    # Creates a list for the Values
    row_data = [fname, lname, acc_num, pin_num, bdate, user_balance]
    # Updates worksheet with the new data
    worksheet_to_update.append_row(row_data)


def get_sheet_data(column_index):
    """
    Checks the Account sheet Data. Finds values found in Google sheet.
    Sends those values to where the function was called.
    """
    account_list_sheet = SHEET.worksheet('accountlist')

    column_values = account_list_sheet.col_values(column_index)
    # Collects all column values after the first row
    column_values = column_values[1:]
    # Returns the column data to where this function was called.
    return column_values


def number_generator(first_name, last_name, date_of_birth):
    """
    Generates random 4 and 9 digit number.
    Calls 'get_sheet_data' function to collect data
    from Google Sheet. Coverts the data to integers.

    Checks generated numbers with sheet data to
    prevent duplicates, generates Account balance
    & calls 'update_sheet_data' function.

    Creates a empty user balance with Money().
    Returns values back to the function that called this one.
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

            user_bal = Money(amount='0.00', currency='EUR')
            update_sheet_data(first_name, last_name, date_of_birth,
                              nine_digit_num, four_digit_num,
                              user_bal, 'accountlist')

            return (nine_digit_num, four_digit_num, user_bal)


def acc_create_finished():
    """
    Account Creation Confirmed message.
    When called, prompts the user to input 'PROCEED' and
    uses 'validate_mode' function to check user input.

    - If Input is True, calls the 'start_menu' function.
    - If Input is False, the while loop repeats.
    """
    print(Fore.CYAN + "When you're ready, Please enter 'PROCEED' to return to"
                      " the Main Menu.\n")
    valid_mode_input = ["PROCEED"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + "Returning to Main Menu...")
                start_menu()


def acc_create_confirm(first_name, last_name, date_of_birth):
    """
    Account Detail confirmation.
    Prints the user inputs to the terminal & prompts the user to
    confirm their details before an account is made.

    - If user input is 'YES' the 'number_generator' & 'acc_create_finished'
      functions are called.
    - If user input is 'NO' the 'create_account' function is called.
    """

    print(Fore.YELLOW + "\nHere are your entered details:")
    print(Style.RESET_ALL + f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Date of Birth: {date_of_birth}")

    print(Fore.CYAN + "\nAre these details correct?"
                      " Please Confirm YES or NO")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.GREEN + f"Thank you {first_name} for your"
                                   " confirmation...\n")
                new_acc_values = number_generator(first_name, last_name,
                                                  date_of_birth)
                nine_digit_num, four_digit_num, user_bal = new_acc_values
                acc_num = nine_digit_num
                create_backup_setup(acc_num)

                print(Fore.GREEN + "Creating your new Account"
                                   " with Eternity Holdings...\n")
                print(Fore.YELLOW + "These are your Account details:\n")
                print(Style.RESET_ALL + f"First Name: {first_name}")
                print(f"Last Name: {last_name}")
                print(f"Date of Birth: {date_of_birth}")
                print("\nYour New Account Number:", nine_digit_num)
                print("Your New Account PIN Number:", four_digit_num)
                print(Fore.RED + "\nPlease take note of these details as"
                                 " you will need them to access your Account"
                                 " in Login.")
                acc_create_finished()
                break

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "No problem. Lets go back...")
                create_account()
                break


def update_backup_data(acc_num, user_location, user_email, user_recovery_pass):
    """
    Updates Google Sheet with Account Recovery Backup data.
    Converts the 'acc_num' to a string so it can be stripped to
    prevent data type errors.

    Locates the associated Account and passes the Backup data
    to the corresponding sheet cells. Returns to the function
    it was called by.
    """
    # Converts acc_num value into a string if not already.
    acc_num = str(acc_num)

    # Find the row index corresponding to the account number.
    all_rows = ACCOUNTLIST.get_all_values()
    acc_num_list = [row[2].strip() for row in all_rows]
    acc_num = acc_num.strip()
    account_for_backup = acc_num_list.index(acc_num) + 1

    # Update the specific cells in the identified row with the provided data.
    ACCOUNTLIST.update_cell(account_for_backup, 7, user_location)
    ACCOUNTLIST.update_cell(account_for_backup, 8, user_email)
    ACCOUNTLIST.update_cell(account_for_backup, 9, user_recovery_pass)

    print(Fore.GREEN + "Account Recovery Backup data updated...")
    return


def get_backup_data(user_location, user_email, user_recovery_pass):
    """
    Obtain Google Sheet data for Backup Recovery.
    """
    print(Fore.GREEN + "Obtaining Account Backup data...")

    ACCOUNTLIST = SHEET.worksheet('accountlist')
    # Gets the data from all sheet rows.
    all_rows = ACCOUNTLIST.get_all_values()

    # Determine the end index dynamically
    end_index = min(9, len(all_rows))

    for row in all_rows[1:end_index]:
        # Check if any cell in the row is empty.
        if any(cell == '' for cell in row):
            print(Fore.RED + "Data does not match any data found.")
            return False

        # Handle the row as a whole list
        sheet_user_location = row[6] if len(row) > 6 else ''
        sheet_user_email = row[7] if len(row) > 7 else ''
        sheet_user_recovery_pass = row[8] if len(row) > 8 else ''

        # Converts the passed data values to strings.
        # Checks if all the user input matches the data in the sheet.
        if (
            str(user_location) == sheet_user_location and
            str(user_email) == sheet_user_email and
            str(user_recovery_pass) == sheet_user_recovery_pass
        ):
            print("Match Found")
            return True

    # If no match found after checking all rows
    print(Fore.RED + "Data does not match any data found.")
    return False


def validate_email(email):
    """
    Email Validator for Account Recovery Backup.
    Uses Import re to detect a specific email pattern.

    - If the email value & the pattern match, returns True.
    - If they do not match, returns False.
    """
    # Pattern for validating email address.
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def create_backup_confirm(acc_num,
                          user_location,
                          user_email,
                          user_recovery_pass):
    """
    Account Backup Confirmation. Prints the user data to the terminal &
    prompts the user to enter 'YES' or 'NO'.

    - If user input is 'YES' it calls the 'update_backup_data' function &
      returns to the function which called it.
    - If user input is 'NO' the 'create_backup_setup' function is called &
      the while loop breaks.
    """
    print(Fore.YELLOW + "\nHere are your entered Account Backup details:")
    print(Style.RESET_ALL + f"Location: {user_location}")
    print(f"Email: {user_email}")
    print(f"Recovery Password: {user_recovery_pass}")

    print(Fore.CYAN + "\nAre these details correct?"
                      " Please Confirm YES or NO")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.GREEN + "Thank you for your confirmation...\n")
                update_backup_data(acc_num, user_location, user_email,
                                   user_recovery_pass)
                return

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "No problem. Lets go back...")
                create_backup_setup(acc_num)
                break


def create_backup_setup(acc_num):
    """
    Create Account Terminal Backup Setup.
    Prompts the user to Enter 'YES', 'NO' or 'WHY'.

    - If user input is 'YES' while loop breaks. Code outside loop proceeds.
    - If user input is 'NO' the code returns to the function that called
      this one.
    - If 'WHY' the code prints statements and repeats the while loop.

    Prompts the user with questions. Calls 'validate_email' on user email
    input. Calls 'create_backup_confirm' & returns to the function that called
    this one.
    """
    print(Fore.YELLOW + "Welcome to Account Creator.")
    print(Fore.CYAN + "You're at the Setup Account Backup Terminal\n")

    print(Style.RESET_ALL + "Do you want to set up your Account Recovery"
                            " Backup? Please Enter 'YES' or 'NO'\n")
    print(Fore.RED + "If your not sure what a Account Recovery Backup is"
                     " please enter 'WHY'.")

    valid_mode_input = ["YES", "NO", "WHY"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string.
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print("Thank you for choosing to Backup your Account")
                break
            elif mode_str == "NO":
                clear()
                print(Fore.RED + "You chose not to set up your Account"
                                 " Recovery Backup.")
                print(Fore.GREEN + "Returning back...")
                return

            elif mode_str == "WHY":
                print(Fore.YELLOW + "\nThe Account Recovery Backup asks you a"
                                    " few more specific questions.\n")
                print(Style.RESET_ALL +
                      "We collect this data so that in the event of you losing"
                      " access to your account, you may be able to regain"
                      " access again yourself without needing to contact"
                      " support.\n")
                continue

    print(Fore.YELLOW + "Account Recovery Backup process has begun...\n")

    print(Style.RESET_ALL + "What is your Country of Residence?\n")
    user_location = input(Fore.GREEN + "Enter here:\n").upper()

    print(Style.RESET_ALL + "What is your Email Address?")
    print(Fore.RED + "Please take note of format Example:"
                     " 'example@email.com'\n")

    while True:
        user_email = input(Fore.GREEN + "Enter here:\n")
        if validate_email(user_email):
            break
        else:
            print(Fore.RED + f"The Email {user_email} is not the correct"
                             " format. Please try again.")
            continue

    print(Style.RESET_ALL + "Create a Custom Recovery Password. It can be"
                            " whatever you want. We reccomend it is something"
                            " you will remember and is unique to you.\n")
    user_recovery_pass = input(Fore.GREEN + "Enter here:\n")

    clear()
    create_backup_confirm(acc_num, user_location, user_email,
                          user_recovery_pass)
    print(Fore.GREEN + "Your Account Recovery Backup has been successfully"
                       " updated!")
    return


def validate_dob(date_of_birth, first_name):
    """
    Validates user input for date.
    Checks user input to be over the Age of 18.

    - If the input is Valid and over 18 code returns true value.
    - If the input is Valid but under 18 code returns to start.
    - If the input is inValid, returns false value.
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
            start_menu()

    except ValueError:
        clear()
        print(Fore.RED + f"Sorry, your date input '{date_of_birth}'"
              " was incorrectly formatted.")
        return False


def create_account():
    """
    Create Account Terminal. Prompts users with an option to return
    to the Main menu. Collects DOB, First and Last Name data from user input.
    Calls validate_dob fuction.

    -If returns True code call confirm function.
    -If returns False while loop repeats.
    """
    print(Fore.YELLOW + "Welcome to the Account Creator.\n")

    print(Style.RESET_ALL + "If you wish to continue with Account Creation"
          " please enter 'PROCEED'.")
    print(Fore.RED + "To return to the Main Menu please Enter 'EXIT'.\n")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["EXIT", "PROCEED"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "EXIT":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Main Menu!")
                print("Sending to Main Menu...\n")
                start_menu()

            elif mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Account"
                                   " Creation!")
                print("Proceeding to Account Creation...\n")

                break

    print(Fore.YELLOW + "Welcome to Account Creator.\n")
    print(Fore.CYAN + "You're now at the Account Creation Terminal.\n")

    first_name = input(Style.RESET_ALL + "Please Enter First Name:\n").upper()

    last_name = input("Please Enter Last Name:\n").upper()

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


def login_user_bal(acc_num):
    """
    Checks current logged in Account's associated
    balance from Google Sheet and prints result to Terminal.
    """
    acc_num_list = get_sheet_data(3)
    acc_bal_list = get_sheet_data(6)

    logged_in_user = acc_num_list.index(acc_num)
    current_acc_bal = acc_bal_list[logged_in_user]

    print(Fore.YELLOW + "\nYour Account Balance is:", current_acc_bal)


def update_acc_bal(user_amount, acc_num, add=True):
    """
    Updates the User Account Balance in Google Sheet.
    Gets logged in Accounts balance and converts
    the string value to a float, then takes the user amount.

    -If add=True the current balance & user input add.
    -If add=False the current balance & user input subtract.

    The value of that new number is returned back into the
    Google sheet string format and updated on the sheet.
    """
    try:
        # Find the row index corresponding to the account number.
        all_rows = ACCOUNTLIST.get_all_values()
        acc_num_list = [row[2].strip() for row in all_rows]
        acc_num = acc_num.strip()
        logged_in_user_index = acc_num_list.index(acc_num) + 1

        # Currency set to EUR
        currency = 'EUR'

        # Extract the numerical value from the string.
        current_acc_bal_str = all_rows[logged_in_user_index - 1][5]
        currency, amount_str = current_acc_bal_str.split()
        current_acc_bal = float(amount_str)

        # Convert amount_value to float for math equation.
        amount_value = float(user_amount.amount)

        # Determine whether to add or subtract based on the add parameter
        if add:
            new_acc_bal = current_acc_bal + amount_value
        else:
            new_acc_bal = current_acc_bal - amount_value

        # Format the new balance as a string with currency prefix
        new_acc_bal_str = f'{currency} {new_acc_bal:.2f}'

        ACCOUNTLIST.update_cell(logged_in_user_index, 6, new_acc_bal_str)

        print(Fore.GREEN + "Updating Account balance...")

    except ValueError:
        print(Fore.RED + "Error: Account number not found or invalid input.")


def acc_deposit(fname, acc_num):
    """
    Account Deposit Terminal. Prompts user to input
    'EXIT' or a numerical value to deposit to their account.

    -If 'EXIT' the while loop ends returning to HUB.
    -If not, try loop attempts to convert value using Money().
    -If it cannot a ValueError triggers & loop begins again.
    -If it can it calls update user balance function.
    """
    clear()
    print(Fore.YELLOW + "Welcome to Eternity Holdings deposit terminal")
    print(Fore.CYAN + "From here you can deposit funds into your Eternity"
                      " Holdings Account. See below for your current balance.")

    while True:
        login_user_bal(acc_num)

        print(Style.RESET_ALL + "\nTo return to the HUB please Enter 'EXIT'.")
        print("Please Enter how much you wish to deposit below:")
        print(Fore.RED + "\nReminder to use the correct format. Example:"
                         " 2, 13.15, etc")
        mode_str = input(Fore.GREEN + "Enter Here:\n").upper()

        if mode_str == "EXIT":
            clear()
            print(Fore.GREEN + "Returning to HUB...\n")
            logged_in_hub(fname, acc_num)
            return

        try:
            user_amount = Money(mode_str, 'EUR')
            update_acc_bal(user_amount, acc_num, add=True)

            clear()
            print(Fore.GREEN + f"{user_amount} has been deposited into"
                               " your account.")

        except ValueError:
            clear()
            print(Fore.RED + f"The Input of {mode_str} is"
                             " incorrect. Remember to use the correct"
                             " format!")


def acc_withdrawal(fname, acc_num):
    """
    Account Withdraw Terminal. Prompts user to input
    'EXIT' or a numerical value to withdraw from their account.

    -If 'EXIT' the while loop ends returning to HUB.
    -If not, try loop attempts to convert value using Money().
    -If it cannot a ValueError triggers & loop begins again.
    -If it can it calls update user balance function.
    """
    clear()
    print(Fore.YELLOW + "Welcome to Eternity Holdings withdraw terminal")
    print(Fore.CYAN + "From here you can withdraw funds out of your Eternity"
                      " Holdings Account. See below for your current balance.")

    while True:
        login_user_bal(acc_num)

        print(Style.RESET_ALL + "\nTo return to the HUB please Enter 'EXIT'.")
        print("Please Enter how much you wish to withdraw below:")
        print(Fore.RED + "\nReminder to use the correct format. Example:"
                         " 2, 13.15, etc")
        mode_str = input(Fore.GREEN + "Enter Here:\n").upper()

        if mode_str == "EXIT":
            clear()
            print(Fore.GREEN + "Returning to HUB...\n")
            logged_in_hub(fname, acc_num)
            return

        try:
            user_amount = Money(mode_str, 'EUR')
            update_acc_bal(user_amount, acc_num, add=False)

            clear()
            print(Fore.GREEN + f"{user_amount} has been withdrawn out of"
                               " your account.")

        except ValueError:
            clear()
            print(Fore.RED + f"The Input of {mode_str} is"
                             " incorrect. Remember to use the correct"
                             " format!")


def acc_logout_confirm(fname, acc_num):
    """
    Log Out Confirmation. Prompts users to input 'YES' or 'NO'.
    uses the Validate Mode function to check user input.

    - If 'YES' the user will return to the Main Menu, logging out.
    - If 'NO' the user will return back to the HUB.
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
                start_menu()

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "Returning back...\n")
                logged_in_hub(fname, acc_num)


def logged_in_hub(fname, acc_num):
    """
    The Main HUB Terminal. Prompts users to enter where
    they wish to go. Calls the Validate Mode function to
    check user input.

    - If input 'DEPOSIT' is detected. Calls the 'acc_deposit' function.
    - If input 'WITHDRAW' is detected. Calls the 'acc_withdrawal' function.
    - If input 'BALANCE' is detected. Calls 'login_user_bal' function.
    - If input 'LOGOUT' is detected. Calls 'acc_logout_confirm' function.
    """
    print(Fore.YELLOW + f"\nWelcome {fname} you are now"
                        " at the Eternity Holdings HUB.")
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
                acc_deposit(fname, acc_num)

            elif mode_str == "WITHDRAW":
                clear()
                print("Going to the Withdraw terminal!\n")
                acc_withdrawal(fname, acc_num)

            elif mode_str == "BALANCE":
                clear()
                print(Fore.CYAN + f"Hello {fname} see below for your balance:")
                login_user_bal(acc_num)
                logged_in_hub(fname, acc_num)

            elif mode_str == "LOGOUT":
                clear()
                acc_logout_confirm(fname, acc_num)

            else:
                print(f"The Input of {mode_str} is incorrect.")


def login_account():
    """
    Login Account Terminal. Prompts users with an option to return
    to the Main menu. Collects User input for their Account.
    In the if statement it calls the locate_acc function,
    to compare user input with stored data.

    - If True the loop breaks and calls logged_in_menu.
    - If False it returns user to the start.
    """
    print(Fore.YELLOW + "Welcome to Account Login.\n")
    print(Style.RESET_ALL + "If you wish to continue with Account Login"
          " please enter 'PROCEED'.")
    print(Fore.RED + "To return to the Main Menu please Enter 'EXIT'.\n")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["EXIT", "PROCEED"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "EXIT":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Main Menu!")
                print("Sending to Main Menu...\n")
                start_menu()

            elif mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Account"
                                   " Login!")
                print("Proceeding to Account Login...\n")

                break

    while True:
        print(Fore.CYAN + "You're now at the Account Login Terminal.\n")
        # Assigns a variable to each user input
        fname = input(Style.RESET_ALL + "Please Enter First Name:\n").upper()
        lname = input("Please Enter Last Name:\n").upper()
        acc_num = input("Please Enter Account Number:\n")
        pin_num = input("Please Enter the Account Pin number:\n")

        # Calls function and gives it the input values
        if login_acc_checker(fname, lname, acc_num, pin_num):
            clear()
            print(Fore.GREEN + "You have Successfully logged in.\n")
            logged_in_hub(fname, acc_num)
            break
        else:
            clear()
            print(Fore.RED + "Sorry your search does not match"
                  " any Account in our database.")
            print("Returning to Main Menu...\n")
            start_menu()


def login_acc_checker(fname, lname, acc_num, pin_num):
    """
    Login Account Checker for the 'login_account' function.
    Extracts corresponding data from worksheet.
    Creates a list of the data. Compares the data with user input.

    - If the values match, returns True.
    - If not they do not, returns False.
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


def acc_recovery_questions():
    """
    Account recovery Questions.
    """
    print(Style.RESET_ALL + "What is your Country of Residence?\n")
    user_location = input(Fore.GREEN + "Enter here:\n").upper()

    print(Style.RESET_ALL + "What is your Email Address?")
    print(Fore.RED + "Please take note of format Example:'example@email.com'")

    while True:
        user_email = input(Fore.GREEN + "\nEnter here:\n")
        if validate_email(user_email):
            break
        else:
            print(Fore.RED + f"The Email {user_email} is not the correct"
                             " format. Please try again.")
            continue

    print(Style.RESET_ALL + "What is your Account Recovery password?\n")
    user_recovery_pass = input(Fore.GREEN + "Enter here:\n")

    if get_backup_data(user_location, user_email, user_recovery_pass):
        return
    else:
        print(Fore.RED + "The details you have entered do not match"
                         " the details recorded in our database.\n")
        print(Style.RESET_ALL + "Please Enter 'RETRY' to try again.")
        print("Or Enter 'FORGOT' if you do not know these Recovery"
              " details.")

        valid_mode_input = ["RETRY", "FORGOT"]
        while True:
            mode_str = input(Fore.GREEN + "Enter here:\n").upper()

            # Calls Mode Validation to check for correct input string
            if validate_mode(mode_str, valid_mode_input):
                if mode_str == "RETRY":
                    clear()
                    print(Fore.GREEN + "No problem. Loading Questions...\n")
                    acc_recovery_questions()

                elif mode_str == "FORGOT":
                    clear()
                    forgot_acc_recovery()


def acc_recovery():
    """
    Account Recovery Terminal.
    """
    print(Fore.YELLOW + "Welcome to Account Recovery.\n")
    print(Style.RESET_ALL + "If you have lost your Account Number or Pin Code"
          " please enter 'PROCEED'.")
    print(Fore.RED + "To return to the Main Menu please Enter 'EXIT'.\n")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["EXIT", "PROCEED"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "EXIT":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Main Menu!")
                print("Sending to Main Menu...\n")
                start_menu()

            elif mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to Account"
                                   " Recovery!")
                print("Sending to Account recovery...\n")

                break

    print(Fore.CYAN + "You're now at the Account Recovery Terminal.\n")
    print(Fore.YELLOW + "Do you have your backup information with you?"
                        " Example: Email, Country of Residence,"
                        " Custom Password")

    print(Style.RESET_ALL + "Please Enter 'YES' or 'NO' to continue.\n")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.CYAN + "Great News we can continue to recover your"
                                  " Eternity Holdings Account!")
                print(Fore.GREEN + "Proceeding...\n")
                break

            elif mode_str == "NO":
                clear()
                forgot_acc_recovery()

    acc_recovery_questions()
    print("At the end of the code...")


def start_menu():
    """
    Start Menu Terminal. Prompts users to enter where
    they wish to go. Calls the Validate Mode function to
    check user input.

    - If input 'CREATE' is detected. Calls the 'create_account' function.
    - If input 'LOGIN' is detected. Calls the 'login_account' function.
    - If input 'RECOVER' is detected. Calls the 'acc_recovery' function.
    """
    print(Fore.YELLOW + "Eternity Holdings the #1 App"
          " to automate your banking needs!\n")
    print("Welcome to the Main Menu.")
    print(Fore.CYAN + "You're now at the Create & Login Terminal.\n")
    print(Style.RESET_ALL + "To proceed with your banking experience,"
          " please choose 'CREATE', 'LOGIN', 'RECOVER'.")

    # Creates a list of expected strings for validate function
    valid_mode_input = ["CREATE", "LOGIN", "RECOVER"]

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

            elif mode_str == "RECOVER":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} your Account!")
                print("Sending to Account Recovery...\n")
                acc_recovery()

            break


def validate_mode(mode_str, valid_mode_input):
    """
    Checks if the value of mode_str is found in
    the valid_modes list.

    - If the value is found, it returns True.
    - If the value is not, it prints a statement and returns False.
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
    start_menu()


if __name__ == "__main__":
    main()
