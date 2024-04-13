import gspread
from google.oauth2.service_account import Credentials
import datetime
import random
from money import Money

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

def update_sheet_data(first_name, last_name, date_of_birth, nine_digit_num, four_digit_num, starting_bal, worksheet):
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
    row_data = [fname, lname, bdate, acc_num, pin_num, starting_balance]
    # Updates worksheet with the new data
    worksheet_to_update.append_row(row_data)

def get_account_and_pin(column_index):
    """
    Checks the Account and Pin numbers
    values found in Google sheet. Converts
    those values into integers.
    """
    account_list_sheet = SHEET.worksheet('accountlist')

    column_values = account_list_sheet.col_values(column_index)
    # Collects all column values after the first row
    column_values = column_values[1:]
    # Returns the column data to integers & removes empty values
    return [int(value) for value in column_values if value]

def number_generator(first_name, last_name, date_of_birth):
    """
    Generates random 4 and 9 digit number.
    Calls get_account_and_pin function to collect
    data from Google Sheet. Checks generated numbers with
    sheet data to prevent duplicates, generates Account balance
    & Calls update_sheet function.
    """
    # Collects Sheet Data from Columns 3 and 5 respectively
    exist_acc_num = get_account_and_pin(3)
    exist_pin_num = get_account_and_pin(5)

    while True:
        # Generates a random 9 digit number.
        nine_digit_num = random.randint(100000000,999999999)
        # Generates a random 4 digit number.
        four_digit_num = random.randint(1000,9999)

        # Checks if generated num already exists in Google sheet
        if (nine_digit_num not in exist_acc_num) and \
           (four_digit_num not in exist_pin_num):
            print("These are your Account details:\n")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Date of Birth: {date_of_birth}")
            print("\nYour New Account Number:", nine_digit_num)
            print("Your New Account PIN Number:", four_digit_num)
            print("\nPlease take note of these details as you will need them to access your Account in Login.")

            starting_bal = Money(amount ='0.00', currency ='EUR')
            update_sheet_data(first_name, last_name, date_of_birth, nine_digit_num, four_digit_num, starting_bal, 'accountlist')
            break

def acc_create_confirm(first_name, last_name, date_of_birth):
    """
    Allows the user to confirm their First & Last name
    and their DOB. Giving the user the option to return if
    they made a mistake.
    """

    print("\nHere are your entered details:")
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Date of Birth: {date_of_birth}")

    print("\nAre these details correct? Please Confirm Yes or No")
    while True:
        crte_conf_str = input("Enter here:\n")
        # Calls Confirm Validation to check for correct input string
        if validate_confirm(crte_conf_str):
            if crte_conf_str == "Yes":
                print(f"Thank you {first_name} for your confirmation.\n")
                print("Creating your new Account with Eternity Holdings.\n")
                number_generator(first_name, last_name, date_of_birth)

            elif crte_conf_str == "No":
                print("No problem. Returning to Account Creation.")
                create_account()

            break 

def validate_confirm(crte_conf_str):
    """
    Checks if the user input in crte_conf_str is Valid.
    """
    # Checks if string equals to the respective two values
    if crte_conf_str == "Yes" or crte_conf_str == "No":
        return True
    else:
        print(f"Wrong User input of '{crte_conf_str}' detected, this is incorrect. Please try again.")
        return False

def create_account():
    """
    Collects DOB, First and Last Name data from user input.
    Calls validate_dob fuction if True code breaks, if false
    while loop restarts.
    """
    print("Welcome to the Account Creation Terminal.\n")

    first_name = input("Please Enter First Name:\n")

    last_name = input("Please Enter Last Name:\n")

    print("NOTICE: You must be 18+ to Create an Account\n")

    while True:
        date_of_birth = input("Please Enter Date of Birth in the format (YYYY-MM-DD):\n") 
        # Calls Date of Birth Validation function
        if validate_dob(date_of_birth):
            #print(f"Thank you {first_name}. Creating your new Account with Eternity Holdings.\n")
            acc_create_confirm(first_name, last_name, date_of_birth)
            break
        else:
            print("Please Try Again.\n")
            

def validate_dob(date_of_birth):
    """
    Validates user input for date.
    Checks user input to be over the Age of 18,
    -If the input is Valid and over 18 code returns true value.
    -If the input is Valid but under 18 code returns to start.
    -If the input is inValid, returns false value. 
    """
    try:
        # Formats User Date Input
        birth_date = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        # Collects Current Date
        current_date = datetime.date.today()
        # Calculates Age by subtracting User Input with Current Date
        age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        # Checks if Age is greater or equal to 18
        if age >= 18:
            return True
        else:
            print("Sorry, you must be 18 or older to create an account with us.\n")
            login_or_create()

    except ValueError:
        print(f"Sorry, your date input '{date_of_birth}' was incorrectly formatted.")
        return False

def logged_in_menu():
    """
    The Eternity Bank's main HUB
    """
    print("You are now at the Eternity Bank HUB.")

def login_account():
    """
    Collects User input for their Account.
    In the if statement it calls the locate_acc function,
    to compare user input with stored data. 

    -If True the loop breaks and calls logged_in_menu.
    -If False it returns user to the start.
    """
    print("Sending to Account Login...\n")

    while True:
        # Assigns a variable to each user input
        fname = input("Please Enter First Name:\n")
        lname = input("Please Enter Last Name:\n")
        acc_num = input("Please Enter Account Number:\n")
        pin_num = input("Please Enter the Account Pin number:\n")

        # Calls function and gives it the input values
        if locate_acc(fname, lname, acc_num, pin_num):
            print("You have Successfully logged in.\n")
            print(f"Welcome {fname}. we're happy to see you!")
            logged_in_menu()
            break
        else:
            print("Sorry your search does not match any Account in our database.\n")
            login_or_create()

def locate_acc(fname, lname, acc_num, pin_num):
    """
    Extracts coresponding data from worksheet.
    Creates a list of the data. Compares the data,
    with user input.
    -If the values match, returns True.
    -If not, returns False.
    """
    account_list_sheet = SHEET.worksheet('accountlist')
    # Collects all row data
    all_rows = account_list_sheet.get_all_values()
    # Iterate over each row in the sheet excluding the title row
    for row in all_rows[1:]:
        # Extract each data from the row in order
        sheet_fname, sheet_lname, sheet_acc_num, sheet_pin_num = row[:4]

        # Check if all the user input matches the data in the sheet
        if fname == sheet_fname and lname == sheet_lname and acc_num == sheet_acc_num and pin_num == sheet_pin_num:
            return True
        
    return False

def login_or_create():
    """
    Gets User string input.
    Run a while loop to collect a valid string from user
    via the terminal, which must be the correct value of
    'Create' or 'Login'. The loop will repeat until input is valid.
    """
    print("You're now at the Create & Login Terminal\n")
    print("To proceed with your banking experience, please choose 'Create' or 'Login'")
    print("Insert the values exactly as shown above.\n")

    while True:
        mode_str = input("Enter here:\n")
        # Calls Mode Validation to check for correct input string
        if validate_mode(mode_str):
            if mode_str == "Create":
                print(f"You chose to {mode_str} an Account!")
                print("Sending to Account Creation...\n")
                create_account()
            elif mode_str == "Login":
                print(f"You chose to {mode_str} to an Account!")
                login_account()

            break 

def validate_mode(mode_str):
    """
    Checks if the user input in mode_str is Valid.
    """
    # Checks if string equals to the respective two values
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
