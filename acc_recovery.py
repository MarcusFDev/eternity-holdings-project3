"""
Account Recovery Function file.
Contains functions relating to account recovery to
locate lost details.

-Funtion that prompts users with backup questions.
-Function that provides users with advice if backup data
 is lost.
"""
from utils import (clear, validate_mode, validate_email, get_backup_data,
                   validate_input)
from colorama import Fore, Style


def acc_recovery(start_menu,
                 create_acc_func,
                 login_acc_func,
                 bank_hub_func,
                 acc_recovery_func,
                 acc_detail_func):
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
                start_menu(create_acc_func, login_acc_func, bank_hub_func,
                           acc_recovery_func, acc_detail_func)

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
                forgot_acc_recovery(start_menu, create_acc_func,
                                    login_acc_func, bank_hub_func,
                                    acc_recovery_func, acc_detail_func)

    acc_recovery_questions(start_menu, create_acc_func, login_acc_func,
                           bank_hub_func, acc_recovery_func, acc_detail_func)

    print(Fore.YELLOW + "\nWe recommend changing your Custom Password reguarly"
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
                start_menu(create_acc_func, login_acc_func, bank_hub_func,
                           acc_recovery_func, acc_detail_func)


def acc_recovery_questions(start_menu,
                           create_acc_func,
                           login_acc_func,
                           bank_hub_func,
                           acc_recovery_func,
                           acc_detail_func):
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
        user_location = validate_input(Fore.GREEN + "Enter here:\n").upper()

        print(Style.RESET_ALL + "What is your Email Address?")
        print(Fore.RED + "Please take note of format Example:'example@email."
                         "com'")

        while True:
            user_email = validate_input(Fore.GREEN + "\nEnter here:\n")
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

        if get_backup_data(user_location, user_email, user_recovery_pass,
                           acc_detail_func):
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
                    forgot_acc_recovery(start_menu, create_acc_func,
                                        login_acc_func, bank_hub_func,
                                        acc_recovery_func, acc_detail_func)


def forgot_acc_recovery(start_menu,
                        create_acc_func,
                        login_acc_func,
                        bank_hub_func,
                        acc_recovery_func,
                        acc_detail_func):
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
                start_menu(create_acc_func, login_acc_func, bank_hub_func,
                           acc_recovery_func, acc_detail_func)
