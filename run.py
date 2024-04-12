import gspread
from google.oauth2.service_account import Credentials
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Eternity Holdings')

accountlist = SHEET.worksheet('accountlist')

def create_account():
    """
    Begins the Account creation process.
    """
    print("Welcome to the Account Creation Terminal.\n")

    first_name = input("Please Enter First Name:\n")
    print(f"Your name is {first_name}\n")

    last_name = input("Please Enter Last Name:\n")
    print(f"Your last name is {last_name}\n")

    print("NOTICE: You must be 18+ to Create an Account\n")

    while True:
        date_of_birth = input("Please Enter Date of Birth in the format (YYYY-MM-DD):\n") 

        if validate_dob(date_of_birth):
            print(f"Thank you {first_name,last_name}. Creating your new Account with Eternity Holdings.\n")
            break
        else:
            print("Please Try Again.\n")
            

def validate_dob(date_of_birth):
    """
    Validates user input for date.
    """
    try:
        birth_date = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        current_date = datetime.date.today()
        age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

        if age >= 18:
            return True
        else:
            print("Sorry, you must be 18 or older to create an account with us.\n")
            login_or_create()

    except ValueError:
        print(f"Sorry, your date input '{date_of_birth}' was incorrectly formatted.")
        return False


def login_account():
    """
    Begins the Account login process.
    """
    print("Sending to Account Login...\n")

def login_or_create():
    """
    Gets User string input.
    Run a while loop to collect a valid string from user
    via the terminal, which must be the correct value of
    'Create' or 'Login'. The loop will repeat until input in valid.
    """
    print("You're now at the Create & Login Terminal\n")
    print("To proceed with your banking experience, please choose 'Create' or 'Login'")
    print("Insert the values exactly as shown above.\n")

    while True:
        mode_str = input("Enter here:\n")

        if validate_mode(mode_str):
            if mode_str == "Create":
                print(f"You chose to {mode_str} an Account!")
                print("Sending to Account Creation...\n")
                create_account()
            elif mode_str == "Login":
                print(f"You chose to {mode_str} to an Account!")
                login_account()

            break # Ends While loop if Validate returns True

def validate_mode(mode_str):
    """
    Checks if the user input in mode_str is Valid.
    """
    if mode_str == "Create" or mode_str == "Login":
        return True
    else:
        print(f"Wrong User input of '{mode_str}' detected, this is incorrect. Please try again.")
        return False

def main():
    """
    Run all program functions.
    """
    
    login_or_create()

print("Welcome to Eternity Holdings the #1 App to automate your banking needs!\n")
main()
