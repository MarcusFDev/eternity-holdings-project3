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

accountlist = SHEET.worksheet('accountlist')

def create_account():
    """
    Begins the Account creation process.
    """
    print("Sending to Account Creation...")

def login_account():
    """
    Begins the Account login process.
    """
    print("Sending to Account Login...")

def login_or_create():
    """
    Gets User string input.
    Run a while loop to collect a valid string from user
    via the terminal, which must be the correct value of
    'Create' or 'Login'. The loop will repeat until input in valid.
    """
    print("To proceed with your banking experience, please choose 'Create' or 'Login'")
    print("Insert the values exactly as shown above.")
    print("Do not input inverted commas ('')\n")

    while True:
        mode_str = input("Enter here:\n")

        if validate_mode(mode_str):
            if mode_str == "Create":
                print(f"You chose to {mode_str} an Account!")
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
