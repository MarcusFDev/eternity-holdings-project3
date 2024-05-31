"""
Utility Functions file.
Contains utility functions commonly reused across many files:

-Clear function for terminal readability.
-Validate functions to check user inputs.
-Functions to check & update the database.
-Account 4 digit Pin generator function.
"""

import os
import re
import random
from colorama import init, Fore, Style

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


def validate_input(user_prompt):
    """
    Prints message and checks that the user input is not empty.
    Repeats until a non-empty user input has been entered.
    """
    while True:
        user_input = input(user_prompt).upper()
        if user_input:
            return user_input
        else:
            print(Fore.RED + "This Input cannot be empty. Please try again.\n"
                  + Style.RESET_ALL)


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


def get_backup_data(user_location,
                    user_email,
                    user_recovery_pass,
                    acc_detail_func):
    """
    Obtain Google Sheet data for Backup Recovery.
    Collects data of rows 1-9 specifically. Checks for empty
    sheet cells and returns False if found.

    Otherwise targets data from rows 7-9. Converts the passed
    user inputs into strings and compares the data from the sheet.

    When match is found grabs the associated account number and calls
    'acc_detail_func' function passing it the account number.
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
            print(Fore.RED + "Empty cell found in row, skipping row.")
            continue

        # Handle the row as a whole list
        sheet_user_location = row[6] if len(row) > 6 else ''
        sheet_user_email = row[7] if len(row) > 7 else ''
        sheet_user_recovery_pass = row[8] if len(row) > 8 else ''
        backup_acc_num = row[2] if len(row) > 2 else ''

        # Converts the passed data values to strings.
        # Checks if all the user input matches the data in the sheet.
        if (
            str(user_location).strip() == sheet_user_location.strip() and
            str(user_email).strip().lower() == sheet_user_email.strip().lower()
            and
            str(user_recovery_pass).strip() == sheet_user_recovery_pass.strip()
        ):
            print(Fore.GREEN + "Account Found.")
            acc_detail_func(backup_acc_num)
            return True

    # If no match found after checking all rows
    print(Fore.RED + "Data does not match any Account found.")
    return False


def acc_pin_generator():
    """
    Generates a 4 digit number to be used as a Account Pin.
    Returns that value to the function that called this one.
    """
    # Generates a random 4 digit number.
    return random.randint(1000, 9999)
