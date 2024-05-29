"""
This is the Eternity Holdings functionality file, run.py.
Contains but not limited to functions that:

-Allows Users to Create a account.
-Accesses and can edit Google Sheets as a database.
-Allows Users to Login to an account they created.
-Users can Log Out of an account.
-Allows users to Deposit & Withdraw funds into their account.
"""

from acc_creation import create_account, create_backup_setup
from utils import (clear, validate_mode, get_sheet_data,
                   acc_pin_generator, validate_email)
from colorama import init, Fore, Style
import pprint
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

# Initialize Colorama to work with ANSI escape sequences.
init()

# Manual Money Conversion Rates.
CONVERSION_RATES = {
    "EUR": 1.0,  # Euro
    "USD": 1.19,  # United States Dollar
    "JPY": 130.76,  # Japanese Yen
    "GBP": 0.87,  # British Pound Sterling
    "AUD": 1.55,  # Austrailian Dollar
    "CAD": 1.48,  # Canadian Dollar
    "CHF": 1.10,  # Swiss Franc
    "CNY": 7.75,  # Chinese Yuan
    "INR": 89.09,  # Indian Rupee
    "RUB": 92.86,  # Russian Ruple
    "BRL": 6.64,  # Brazilian Real
    "NOK": 10.45  # Norwegian Krone
}

CURRENCY_NAMES = {
    "EUR": "European Euro",
    "USD": "United States Dollar",
    "JPY": "Japanese Yen",
    "GBP": "British Pound Sterling",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "RUB": "Russian Ruble",
    "BRL": "Brazilian Real",
    "NOK": "Norwegian Krone"
}


def get_backup_data(user_location, user_email, user_recovery_pass):
    """
    Obtain Google Sheet data for Backup Recovery.
    Collects data of rows 1-9 specifically. Checks for empty
    sheet cells and returns False if found.

    Otherwise targets data from rows 7-9. Converts the passed
    user inputs into strings and compares the data from the sheet.

    When match is found grabs the asscoiated account number and calls
    'all_acc_detail' function passings it the account number.
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
            print(Fore.RED + "Data does not match any Account found.")
            return False

        # Handle the row as a whole list
        sheet_user_location = row[6] if len(row) > 6 else ''
        sheet_user_email = row[7] if len(row) > 7 else ''
        sheet_user_recovery_pass = row[8] if len(row) > 8 else ''

        backup_acc_num = row[2] if len(row) > 2 else ''

        # Converts the passed data values to strings.
        # Checks if all the user input matches the data in the sheet.
        if (
            str(user_location) == sheet_user_location and
            str(user_email) == sheet_user_email and
            str(user_recovery_pass) == sheet_user_recovery_pass
        ):
            print("Account Found.")
            all_acc_detail(backup_acc_num)
            return True

    # If no match found after checking all rows
    print(Fore.RED + "Data does not match any Account found.")
    return False


def login_user_bal(acc_num):
    """
    Checks current logged in Account's associated
    balance from Google Sheet and prints result to Terminal.
    """
    acc_num_list = get_sheet_data(3)
    acc_bal_list = get_sheet_data(6)

    logged_in_user = acc_num_list.index(acc_num)
    current_acc_bal = acc_bal_list[logged_in_user]

    print(Fore.YELLOW + f"Your Account Balance is: {current_acc_bal}.\n")


def update_acc_bal(user_amount, acc_num, currency, add=True):
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
        # Check if the user input is positive. (Filters negative numbers)
        if user_amount.amount < 0:
            clear()
            print(Fore.RED + "Invalid input. Amount must be the correct"
                             " format.\n")
            return

        # Find the row index corresponding to the account number.
        all_rows = ACCOUNTLIST.get_all_values()
        acc_num_list = [row[2].strip() for row in all_rows]
        acc_num = acc_num.strip()
        logged_in_user_index = acc_num_list.index(acc_num) + 1

        # Extract the numerical value from the string.
        current_acc_bal_str = all_rows[logged_in_user_index - 1][5]
        currency, amount_str = current_acc_bal_str.split()
        current_acc_bal = float(amount_str)

        # Convert amount_value to float for math equation.
        amount_value = float(user_amount.amount)

        # Determine whether to add or subtract based on the add parameter.
        if add:
            new_acc_bal = current_acc_bal + amount_value
            if new_acc_bal > 100000:
                excess_amount = new_acc_bal - 100000
                new_acc_bal = 100000
                clear()
                print(Fore.RED + "Your deposit exceeded the maximum"
                                 " account balance limit.")
                print(f"An excess of {currency} {excess_amount:.2f}"
                      " could not be deposited.\n")
            else:
                clear()
                print(Fore.GREEN + "Updating Account balance...")
                print(f"{user_amount} has been deposited into your account.\n")
        else:
            new_acc_bal = current_acc_bal - amount_value
            if new_acc_bal < 0:
                excess_amount = amount_value - current_acc_bal
                new_acc_bal = 0
                clear()
                print(Fore.RED + "Your withdrawal exceeded the funds"
                                 " located in this account.")
                print(f"The sum of {currency} {excess_amount:.2f}"
                      " could not be withdrawn.\n")
            else:
                clear()
                print(Fore.GREEN + "Updating Account balance...")
                print(f"{user_amount} has been withdrawn out of your account."
                      "\n")

        # Format the new balance as a string with currency prefix.
        new_acc_bal_str = f'{currency} {new_acc_bal:.2f}'

        ACCOUNTLIST.update_cell(logged_in_user_index, 6, new_acc_bal_str)

    except ValueError:
        print(Fore.RED + "Error: Account number not found or invalid input.\n")


def acc_deposit(fname, acc_num):
    """
    Account Deposit Terminal. Prompts user to input
    'EXIT' or a numerical value to deposit to their account.

    - If 'EXIT' the while loop ends returning to HUB.
    - Grabs Account currency using 'check_acc_currency()'.
    - The loop attempts to convert value using 'Money()'.
    - If it cannot a ValueError triggers & loop begins again.
    - If it can it calls update user balance function.
    """
    clear()

    while True:
        print(Fore.YELLOW + "Welcome to Eternity Holdings deposit terminal")
        print(Fore.CYAN + "From here you can deposit funds into your Eternity"
                          " Holdings Account. See below for your current"
                          " balance.")
        login_user_bal(acc_num)

        print(Style.RESET_ALL + "\nTo return to the HUB please Enter 'EXIT'.")
        print("Please Enter how much you wish to deposit below:")
        print(Fore.RED + "\nReminder to use the correct format. Example:"
                         " 2, 13.15, etc")
        mode_str = input(Fore.GREEN + "Enter Here:\n").upper()

        if mode_str == "EXIT":
            clear()
            print(Fore.GREEN + "Returning to HUB...\n")
            bank_hub(fname, acc_num)
            return

        try:
            currency = check_acc_currency(acc_num)
            clear()
            user_amount = Money(mode_str, currency)
            update_acc_bal(user_amount, acc_num, currency, add=True)
            continue

        except ValueError:
            clear()
            print(Fore.RED + f"The Input of {mode_str} is"
                             " incorrect. Remember to use the correct"
                             " format!\n")


def acc_withdrawal(fname, acc_num):
    """
    Account Withdraw Terminal. Prompts user to input
    'EXIT' or a numerical value to withdraw from their account.

    - If 'EXIT' the while loop ends returning to HUB.
    - Grabs Account currency using 'check_acc_currency()'.
    - The loop attempts to convert value using Money().
    - If it cannot a ValueError triggers & loop begins again.
    - If it can it calls update user balance function.
    """
    clear()

    while True:
        print(Fore.YELLOW + "Welcome to Eternity Holdings withdraw terminal")
        print(Fore.CYAN + "From here you can withdraw funds out of your"
                          " Eternity Holdings Account. See below for your"
                          " current balance.")
        login_user_bal(acc_num)

        print(Style.RESET_ALL + "\nTo return to the HUB please Enter 'EXIT'.")
        print("Please Enter how much you wish to withdraw below:")
        print(Fore.RED + "\nReminder to use the correct format. Example:"
                         " 2, 13.15, etc")
        mode_str = input(Fore.GREEN + "Enter Here:\n").upper()

        if mode_str == "EXIT":
            print(Fore.GREEN + "Returning to HUB...\n")
            bank_hub(fname, acc_num)
            return

        try:
            currency = check_acc_currency(acc_num)
            clear()
            user_amount = Money(mode_str, currency)
            update_acc_bal(user_amount, acc_num, currency, add=False)
            continue

        except ValueError:
            clear()
            print(Fore.RED + f"The Input of {mode_str} is incorrect. Remember"
                             " to use the correct format!")


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
                bank_hub(fname, acc_num)


def acc_change_pin(acc_num):
    """
    Account Change Pin terminal.
    Prompts the user with the option to return to function that
    called this one. If 'YES' the function code continues.

    Finds the associated account details with the acc_num value.
    Calls the 'acc_pin_generator' function and grabs the returned value.
    Updates the New Pin on the sheet for the corresponding acc_num.

    Prints the new Account Pin to terminal and prompts the user the option
    to Exit.
    """
    print(Fore.YELLOW + "Welcome to the Account Pin Change terminal.")
    print(Fore.CYAN + "Are you sure you want to Request a Pin change?\n")
    print(Style.RESET_ALL + "Please Enter 'YES' or 'NO'.")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["YES", "NO"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "YES":
                clear()
                print(Fore.GREEN + "You chose to change your Account Pin!")
                break

            elif mode_str == "NO":
                clear()
                print(Fore.GREEN + "No problem, returning to Options Menu..."
                                   "\n")
                return

    # Find the row index corresponding to the account number.
    all_rows = ACCOUNTLIST.get_all_values()
    acc_num_list = [row[2].strip() for row in all_rows]
    acc_num = acc_num.strip()
    logged_in_user_index = acc_num_list.index(acc_num) + 1

    new_pin_num = acc_pin_generator()
    print(Fore.GREEN + "Changing your Account Pin...\n")
    ACCOUNTLIST.update_cell(logged_in_user_index, 4, new_pin_num)

    print(Fore.YELLOW + "Your New Account Pin is:", new_pin_num)
    print(Fore.RED + "Reminder: Please keep record of your new pin as you will"
                     " need it to log back in.\n")

    print(Fore.CYAN + "When you're ready, Please enter 'EXIT' to return to"
                      " the More Options.\n")
    valid_mode_input = ["EXIT"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls validate_mode to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "EXIT":
                clear()
                print(Fore.GREEN + "Returning to Options Menu...")
                return


def acc_options(fname, acc_num):
    """
    Account More Options terminal.
    Prints statements to the terminal and prompts the user to input
    where they want to proceed to.

    - If user input of 'RECOVERY' is detected, 'all_acc_detail' &
      'create_backup_setup' functions are called.
    - If user input of 'CHANGE PIN' is detected, 'acc_change_pin' function is
      called.
    - If 'RETURN' is detected, 'logged_in_hub' function is called.
    """
    clear()
    backup_acc_num = acc_num

    # Creates a list of expected strings for validate function
    valid_mode_input = ["RECOVERY", "CHANGE PIN", "RETURN"]

    while True:
        print(Fore.YELLOW + f"Welcome {fname} here are More Options to choose"
                            " from.")
        print(Fore.CYAN + "Please Enter one of the following:\n")

        print(Style.RESET_ALL + "Enter 'RECOVERY' to check & update or if you"
                                " have not already; create you Account"
                                " Recovery Backup.")

        print("Enter 'CHANGE PIN' to request a account pin number change.")

        print("Enter 'RETURN' to go back to the Main HUB Terminal.\n")
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()

        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "RECOVERY":
                clear()
                all_acc_detail(backup_acc_num)
                print("Going to the Account Recovery Backup terminal!\n")
                create_backup_setup(acc_num)

            elif mode_str == "CHANGE PIN":
                clear()
                print("Going to the Account Pin Change terminal!\n")
                acc_change_pin(acc_num)

            elif mode_str == "RETURN":
                clear()
                print("Returning back to the HUB...\n")
                bank_hub(fname, acc_num)


def check_acc_currency(acc_num):
    """
    Checks Account Currency. Grabs sheet data for
    all Account Numbers and balances. Then takes 'acc_num'
    and finds associated balance.

    Compares account balance with 'CURRENCY_NAMES' dictionary.
    Finds associated currency, prints statement.
    Returns the value 'currency'.
    """
    acc_num_list = get_sheet_data(3)
    acc_bal_list = get_sheet_data(6)

    logged_in_user = acc_num_list.index(acc_num)
    current_acc_bal = acc_bal_list[logged_in_user]

    # Extract currency code from current account balance string.
    current_currency = current_acc_bal.split()[0]

    # Iterate over the currency_names dictionary to find the currency.
    for currency, full_name in CURRENCY_NAMES.items():
        if currency == current_currency:
            print(Style.RESET_ALL + f"{currency} the {full_name}.")
            return currency

    print(Fore.RED + "An Error has occurred finding Account Currency type.")


def currency_converter(requested_convert, acc_num):
    """
    Currency Converter. Grabs the acc_num and associated
    balance to that account. Splits the currency with the bal.
    Compares the currency with the 'requested_convert' value.

    - If Equal, no conversion needed.
    - If Current balance is EUR, multiples the bal with the requested_convert.
    - If requested_convert is EUR, it divides the conversion rate with acc bal.
    - If neither currencies are EUR, converts the current acc currency back to
      EUR then multiplies that value with the 'requested_convert'.

    Formats the new currency & updates the Google Sheet.
    """
    acc_num_list = get_sheet_data(3)
    acc_bal_list = get_sheet_data(6)

    try:
        logged_in_user = acc_num_list.index(acc_num)
    except ValueError:
        clear()
        print(Fore.RED + f"Account number {acc_num} not found in the list.")
        return

    before_convert_bal_str = acc_bal_list[logged_in_user]

    currency, amount_str = before_convert_bal_str.split()
    before_acc_bal = float(amount_str)

    if currency == requested_convert:
        # If the requested currency is the same as the current currency,
        # no need to perform conversion
        new_acc_bal = before_acc_bal
    elif currency == "EUR":
        # Converts the balance from Euro to the requested currency.
        new_acc_bal = before_acc_bal * CONVERSION_RATES[requested_convert]
    elif requested_convert == "EUR":
        # Converts the balance from the current currency to Euro.
        new_acc_bal = before_acc_bal / CONVERSION_RATES[currency]
    else:
        # Converts the balance from one non-Euro currency to another.
        # First converts to Euro, then to the requested currency.
        euro_equivalent = before_acc_bal / CONVERSION_RATES[currency]
        new_acc_bal = euro_equivalent * CONVERSION_RATES[requested_convert]

    current_acc_bal = Money(new_acc_bal, requested_convert)

    formatted_bal = f"{requested_convert} {current_acc_bal.amount:.2f}"

    try:
        ACCOUNTLIST.update_cell(logged_in_user + 2, 6, formatted_bal)
        clear()
        print("Your Account Balance has been updated to"
              f" {requested_convert}.\n")
        return
    except Exception as e:
        clear()
        print(Fore.RED + f"An error occurred while updating the cell: {e}")
        return


def currency_convert_menu(fname, acc_num):
    """
    Currency Convert Menu. Wrapped in a While True loop. Prompts users with a
    user input accepting 3 options.

    - If 'EXIT' is detected, returns to the HUB menu.
    - if 'LIST' is detected, uses 'pprint()' to display the 'CONVERSION_NAMES'
      dictionary.
    - If neither of those are detected a 'try' block continues.

    Renames 'mode_str' value to 'requested_convert', calls 'currency_convert'
    function passing it the value. If successful loop breaks to the start.
    """
    while True:
        print(Fore.YELLOW + f"Welcome {fname} to Eternity Holdings Currency"
                            " Conversion terminal.\n")
        print(Fore.CYAN + "Your Account's Default Currency is set to:")
        check_acc_currency(acc_num)

        print(Style.RESET_ALL + "\nPlease Enter which Currency to convert to.")
        print("Or Enter 'LIST' to see supported currencies.\n")

        print(Fore.RED + "Note: You must Enter in the correct format.")
        print(Fore.CYAN + "Example: 'EUR', 'GBP', 'USD'.\n")

        print(Style.RESET_ALL + "To return to the HUB please Enter 'EXIT'"
                                ".\n")
        while True:
            mode_str = input(Fore.GREEN + "Enter here:\n").upper()

            if mode_str == "EXIT":
                clear()
                print(Fore.GREEN + "Returning to HUB...\n")
                bank_hub(fname, acc_num)

            elif mode_str == "LIST":
                print(Fore.YELLOW + "\nThis is the list of currency currently"
                                    " supported:")
                print(Style.RESET_ALL)
                pprint.pprint(CURRENCY_NAMES)
                print(Fore.CYAN + "\nWhich one do you require?\n")
                print(Fore.RED + "If you changed your mind please Enter"
                                 " 'EXIT'.")
                continue

            try:
                requested_convert = mode_str
                currency_converter(requested_convert, acc_num)
                break
            except ValueError:
                print(Fore.RED + "Invalid input. Please try again.")
                continue

            except Exception as e:
                print(Fore.RED + f"The input: {str(e)} is incorrect.")
                continue


def bank_hub(fname, acc_num):
    """
    The Main HUB Terminal. Prompts users to enter where
    they wish to go. Calls the Validate Mode function to
    check user input.

    - If 'DEPOSIT' is detected. Calls the 'acc_deposit' function.
    - If 'WITHDRAW' is detected. Calls the 'acc_withdrawal' function.
    - If 'BALANCE' is detected. Calls 'login_user_bal' function.
    - If 'CONVERSION' is detected. Calls 'currency_convert_menu' function.
    - If 'MORE OPTIONS' is detected. Calls 'acc_options' function.
    - If 'LOG OUT' is detected. Calls 'acc_logout_confirm' function.
    """
    print(Fore.YELLOW + f"Welcome {fname} you are now"
                        " at the Eternity Holdings HUB.")
    print(Fore.CYAN + "From here you have access to all our services."
          " See below for our current available options:\n")

    print(Style.RESET_ALL + "Enter 'DEPOSIT' to go to"
                            " the Deposit funds terminal.")
    print("Enter 'WITHDRAW' to go to the Withdraw funds terminal.")
    print("Enter 'BALANCE' to check your current account balance.")
    print("Enter 'CONVERSION' to change your Account Currency.\n")

    print("Or Enter 'MORE OPTIONS' to load more options.")
    print("To Log Out of this Account Enter 'LOG OUT'.\n")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["DEPOSIT", "WITHDRAW", "BALANCE", "MORE OPTIONS",
                        "CONVERSION", "LOG OUT"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()

        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "DEPOSIT":
                clear()
                print("Going to the Deposit terminal...\n")
                acc_deposit(fname, acc_num)

            elif mode_str == "WITHDRAW":
                clear()
                print("Going to the Withdraw terminal...\n")
                acc_withdrawal(fname, acc_num)

            elif mode_str == "BALANCE":
                clear()
                print(Fore.CYAN + f"Hello {fname} see below for your balance:")
                login_user_bal(acc_num)
                bank_hub(fname, acc_num)

            elif mode_str == "CONVERSION":
                clear()
                print("Going to the Conversion terminal...\n")
                currency_convert_menu(fname, acc_num)

            elif mode_str == "MORE OPTIONS":
                clear()
                print("Loading More Options...")
                acc_options(fname, acc_num)

            elif mode_str == "LOG OUT":
                clear()
                acc_logout_confirm(fname, acc_num)


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
                print(Fore.RED + "Returning to Main Menu...\n")
                start_menu()

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
            bank_hub(fname, acc_num)
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


def forgot_acc_recovery():
    """
    This function is called by 'acc_recovery_questions' and
    'acc_recovery'. Prints statements to terminal.
    Prompts the user to Enter 'RETURN' utilizing the 'validate_mode'
    function.

    - If user input is True, 'start_menu' function is called.
    """
    print(Fore.RED + "We're Sorry but without your backup information we"
                     " cannot help you in the Account Recovery Terminal.\n")
    print(Fore.CYAN + "Please Contact Customer Support at"
                      " marcusf.dev@gmail.com\n")

    print(Style.RESET_ALL + "When you're ready please Enter 'RETURN' to"
                            " return to the Main Menu.")

    valid_mode_input = ["RETURN"]
    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()

        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "RETURN":
                clear()
                print(Fore.GREEN + "Returning to the Main menu...\n")
                start_menu()


def all_acc_detail(backup_acc_num):
    """
    When 'all_acc_detail' is called, it collects all Google Sheet
    data and compares the sheet account number with passed value
    of 'backup_acc_num'.

    Once Account is found, gets the associated data in that row.
    Prints that data to the terminal and returns to the function call.
    """
    ACCOUNTLIST = SHEET.worksheet('accountlist')
    # Gets the data from all sheet rows.
    all_rows = ACCOUNTLIST.get_all_values()
    # Iterate through all rows
    for row in all_rows:
        # Check all rows account number matches the provided backup_acc_num
        if len(row) > 2 and row[2] == backup_acc_num:
            # Print the data from columns 1 to 9 in the matched row
            print(Fore.CYAN + "Here are your Account details:\n")
            print(Style.RESET_ALL + "First Name:", row[0])
            print("Last Name:", row[1])
            print("Account Number:", row[2])
            print("Pin Number:", row[3])
            print("Date of Birth:", row[4])
            print(Fore.CYAN + "\nYour Account recovery Backup details:\n")
            print(Style.RESET_ALL + "Location:", row[6])
            print("Email Address:", row[7])
            print("Recovery Password:", row[8])
            return


def acc_recovery_questions():
    """
    Account Recovery Backup Questions. When called the user is prompt with
    questions. Uses 'validate_email' to obtain a correct email format.
    Calls 'get_backup_data' function passing it user values.

    - If that function returns True, this returns to the function call.
    - If False, function code continues:

    Prompts user with a question.

    - If user input is 'RETRY' code wraps back to start of questions.
    - If 'FORGOT' the 'forgot_acc_recovery' function is called.
    """
    while True:
        print(Style.RESET_ALL + "What is your Country of Residence?\n")
        user_location = input(Fore.GREEN + "Enter here:\n").upper()

        print(Style.RESET_ALL + "What is your Email Address?")
        print(Fore.RED + "Please take note of format Example:'example@email."
                         "com'")

        while True:
            user_email = input(Fore.GREEN + "\nEnter here:\n")
            if validate_email(user_email):
                break
            else:
                print(Fore.RED + f"The Email {user_email} is not the correct"
                                 " format. Please try again.")
                continue

        print(Style.RESET_ALL + "What is your Account Recovery password?\n")
        print(Fore.RED + "Reminder: This was case sensitive!\n")
        user_recovery_pass = input(Fore.GREEN + "Enter here:\n")

        clear()

        if get_backup_data(user_location, user_email, user_recovery_pass):
            return
        else:
            print(Fore.RED + "The details you have entered do not match"
                             " the details recorded in our database.\n")
            print(Fore.CYAN + "Are you sure you entered them correctly?\n")
            print(Style.RESET_ALL + "Please Enter 'RETRY' to try again.")
            print("Or Enter 'FORGOT' if you do not know these Recovery"
                  " details.")

            valid_mode_input = ["RETRY", "FORGOT"]
            mode_str = input(Fore.GREEN + "Enter here:\n").upper()

            if validate_mode(mode_str, valid_mode_input):
                if mode_str == "RETRY":
                    clear()
                    print(Fore.GREEN + "No problem. Loading Questions...\n")
                    continue
                elif mode_str == "FORGOT":
                    clear()
                    forgot_acc_recovery()


def acc_recovery():
    """
    Account Recovery Terminal. Prompts users with an option to return
    to the Main menu. Then prompts users with a question.

    - If 'YES' while loop breaks. Function code proceeds.
    - If 'NO' the 'forgot_acc_recovery' function is called.

    Calls the 'acc_recovery_questions' function. Prints statements to
    terminal and prompts users to enter 'PROCEED' using 'validate_mode'
    function call. Once True, calls the 'start_menu' function.
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

    print(Fore.YELLOW + "\nWe reccomend changing your Custom Password reguarly"
                        " for an extra layer of protection.")
    print(Fore.RED + "If you believe your Account is at risk of being"
                     " compromised, please Login & request a pin change.")
    print("Otherwise contact support at: 'marcusf.dev@gmail.com'\n")

    print(Style.RESET_ALL + "When you're ready please Enter 'RETURN' to leave"
                            " to the main menu.")
    # Creates a list of expected strings for validate function
    valid_mode_input = ["RETURN"]

    while True:
        mode_str = input(Fore.GREEN + "Enter here:\n").upper()
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str, valid_mode_input):
            if mode_str == "RETURN":
                clear()
                print(Fore.GREEN + "Returning to Main Menu...\n")
                start_menu()


def start_menu(create_acc_func):
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
          " please:\n")
    print("Enter 'CREATE' to Create an Account.")
    print("Enter 'LOGIN' to Login to an existing Account.")
    print("Enter 'RECOVER' if you've lost access to a Account.\n")

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
                create_acc_func(start_menu, create_acc_func)

            elif mode_str == "LOGIN":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} to an Account!")
                print("Sending to Account Login...\n")
                # login_account()
                print(Fore.RED + "Feature not compatible with this version"
                                 " of code. Ending Programme.")

            elif mode_str == "RECOVER":
                clear()
                print(Fore.GREEN + f"You chose to {mode_str} your Account!")
                print("Sending to Account Recovery...\n")
                # acc_recovery()
                print(Fore.RED + "Feature not compatible with this version"
                                 " of code. Ending Programme.")

            break


def main():
    """
    Run all program functions.
    """
    clear()
    start_menu(create_account)


if __name__ == "__main__":
    main()
