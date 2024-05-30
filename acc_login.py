"""
Login Functions
"""

from utils import clear, validate_mode
from colorama import Fore, Style

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


def login_account(start_menu_func, create_acc_func, login_acc_func,
                  bank_hub_func, acc_recovery_func, acc_detail_func):
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
                print(Fore.RED + "Returning to Main Menu...\n")
                start_menu_func(create_acc_func, login_account, bank_hub_func,
                                acc_recovery_func, acc_detail_func)
                return

            elif mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + "Proceeding to Account Login...\n")
                break

    while True:
        print(Fore.YELLOW + "Welcome to Account Login.\n")
        print(Fore.CYAN + "You're now at the Account Login Terminal.")
        print(Fore.RED + "Note: Names are not case sensitive.\n")
        # Assigns a variable to each user input
        print(Style.RESET_ALL + "What is your First Name?")
        fname = input(Fore.GREEN + "Enter here:\n").upper()

        print(Style.RESET_ALL + "\nWhat is your Last Name?")
        lname = input(Fore.GREEN + "Enter here:\n").upper()

        print(Style.RESET_ALL + "\nWhat is your Account Number?")
        acc_num = input(Fore.GREEN + "Enter here:\n").upper()

        print(Style.RESET_ALL + "\nWhat is your Account Pin Number?")
        pin_num = input(Fore.GREEN + "Enter here:\n").upper()

        # Calls function and gives it the input values
        if login_acc_checker(fname, lname, acc_num, pin_num):
            clear()
            print(Fore.GREEN + "You have Successfully logged in.\n")
            bank_hub_func(fname, acc_num, create_acc_func, login_acc_func,
                          bank_hub_func, acc_recovery_func, acc_detail_func)
            break
        else:
            clear()
            print(Fore.RED + "Sorry your search does not match"
                  " any Account in our database.")
            print("Returning to Main Menu...\n")
            start_menu_func(create_acc_func, login_account, bank_hub_func,
                            acc_recovery_func, acc_detail_func)
            return


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
