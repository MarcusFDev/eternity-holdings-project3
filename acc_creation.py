"""
Account Creation Functions file.
Contains main functions that handle Account creation
and Account create backup & also including:

-A function to validate email address.
-A function that generates a random 9 digit account number.
"""

from utils import (clear, validate_mode, validate_email, get_sheet_data,
                   update_sheet_data, update_backup_data, acc_pin_generator)
from colorama import Fore, Style
import datetime
import random
from money import Money


def create_account(start_menu_func,
                   create_acc_func,
                   login_acc_func,
                   bank_hub_func,
                   acc_recovery_func,
                   acc_detail_func):
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
                print(Fore.RED + "Returning to Main Menu...\n")
                return start_menu_func(create_acc_func, login_acc_func,
                                       bank_hub_func, acc_recovery_func,
                                       acc_detail_func)

            elif mode_str == "PROCEED":
                clear()
                print(Fore.GREEN + "Proceeding to Account Creation...\n")

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
        if validate_dob(date_of_birth, first_name, start_menu_func,
                        create_acc_func, login_acc_func, bank_hub_func,
                        acc_recovery_func, acc_detail_func):
            clear()
            acc_create_confirm(first_name, last_name, date_of_birth,
                               start_menu_func, create_acc_func,
                               login_acc_func, bank_hub_func,
                               acc_recovery_func, acc_detail_func)
            break
        else:
            print(Fore.RED + "Please Try Again.\n")

    return start_menu_func(create_acc_func, login_acc_func, bank_hub_func)


def validate_dob(date_of_birth,
                 first_name,
                 start_menu_func,
                 create_acc_func,
                 login_acc_func,
                 bank_hub_func,
                 acc_recovery_func,
                 acc_detail_func):
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
            return start_menu_func(create_acc_func, login_acc_func,
                                   bank_hub_func, acc_recovery_func,
                                   acc_detail_func)

    except ValueError:
        clear()
        print(Fore.RED + f"Sorry, your date input '{date_of_birth}'"
              " was incorrectly formatted.")
        return False


def acc_create_confirm(first_name,
                       last_name,
                       date_of_birth,
                       start_menu_func,
                       create_acc_func,
                       login_acc_func,
                       bank_hub_func,
                       acc_recovery_func,
                       acc_detail_func):
    """
    Account Detail confirmation.
    Prints the user inputs to the terminal & prompts the user to
    confirm their details before an account is made.

    - If user input is 'YES' the 'acc_num_generator' & 'acc_create_finished'
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
                new_acc_values = acc_num_generator(first_name, last_name,
                                                   date_of_birth)
                generated_acc_num, generated_pin_num, user_bal = new_acc_values
                acc_num = generated_acc_num
                create_backup_setup(acc_num)

                print(Fore.GREEN + "Creating your new Account"
                                   " with Eternity Holdings...\n")
                print(Fore.YELLOW + "These are your Account details:\n")
                print(Style.RESET_ALL + f"First Name: {first_name}")
                print(f"Last Name: {last_name}")
                print(f"Date of Birth: {date_of_birth}")
                print("\nYour New Account Number:", generated_acc_num)
                print("Your New Account PIN Number:", generated_pin_num)
                print(Fore.RED + "\nPlease take note of these details as"
                                 " you will need them to access your Account"
                                 " in Login.")
                acc_create_finished(start_menu_func, create_acc_func,
                                    login_acc_func, bank_hub_func,
                                    acc_recovery_func, acc_detail_func)
                break

            elif mode_str == "NO":
                clear()
                print(Fore.RED + "No problem. Lets go back...")
                create_account(start_menu_func, create_acc_func,
                               login_acc_func, bank_hub_func,
                               acc_recovery_func, acc_detail_func)
                break


def acc_num_generator(first_name, last_name, date_of_birth):
    """
    Generates random 9 digit number to be used as a Account Number.
    Calls 'get_sheet_data' function to collect data from Google Sheet.
    Converts that data from strings to integers.

    Compares generated account number with sheet data to
    prevent duplicates. Calls 'four_digit_num' function then generates
    Account balance & calls 'update_sheet_data' function.

    Creates a empty user balance with Money().
    Returns values back to the function that called this one.
    """
    # Collects Sheet Data from Columns 3 and 4 & converts them to integers.
    exist_acc_num = [int(value) for value in get_sheet_data(3) if value]

    while True:
        # Generates a random 9 digit number.
        generated_acc_num = random.randint(100000000, 999999999)
        # Generates a random 4 digit number.
        generated_pin_num = acc_pin_generator()

        # Checks if generated num already exists in Google sheet.
        if (generated_acc_num not in exist_acc_num):

            user_bal = Money(amount='0.00', currency='EUR')
            update_sheet_data(first_name, last_name, date_of_birth,
                              generated_acc_num, generated_pin_num,
                              user_bal, 'accountlist')

            return (generated_acc_num, generated_pin_num, user_bal)


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

    print(Style.RESET_ALL + "Do you want to set up or change your Account"
                            " Recovery Backup?")
    print("Please Enter 'YES' or 'NO'.\n")
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
                print(Fore.RED + "You chose not to set up or change your"
                                 " Account Recovery Backup.")
                print(Fore.GREEN + "Returning back...\n")
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
    print(Fore.CYAN + "Watch out as it will be case sensitive!\n")
    user_recovery_pass = input(Fore.GREEN + "Enter here:\n")

    clear()
    create_backup_confirm(acc_num, user_location, user_email,
                          user_recovery_pass)
    return


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


def acc_create_finished(start_menu_func,
                        create_acc_func,
                        login_acc_func,
                        bank_hub_func,
                        acc_recovery_func,
                        acc_detail_func):
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
                return start_menu_func(create_acc_func, login_acc_func,
                                       bank_hub_func, acc_recovery_func,
                                       acc_detail_func)

            break

    return False
