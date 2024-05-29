"""
Utility Functions
"""

import os
import re
import random
from colorama import init, Fore

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

# Initialize Colorama to work with ANSI escape sequences.
init()


def clear():
    """
    Clear function to clean-up the terminal window so the User has
    a better visual on the terminal content that is most relevant.
    """
    os.system("cls" if os.name == "nt" else "clear")


def validate_mode(mode_str, valid_options):
    """
    Checks if the value of mode_str is found in
    the valid_modes list.

    - If the value is found, it returns True.
    - If the value is not, it prints a statement and returns False.
    """
    # Checks if string equals to the respective values
    if mode_str in valid_options:
        return True
    else:
        print(Fore.RED + "Invalid option. Please enter a valid choice.")
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


def update_sheet_data(first_name,
                      last_name,
                      date_of_birth,
                      generated_acc_num,
                      generated_pin_num,
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
    acc_num = generated_acc_num
    pin_num = generated_pin_num
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

    print(Fore.GREEN + "Account Recovery Backup has been sucessfully updated!")
    return


def acc_pin_generator():
    """
    Generates a 4 digit number to be used as a Account Pin.
    Returns that value to the function that called this one.
    """
    # Generates a random 4 digit number.
    return random.randint(1000, 9999)
