# Eternity Holdings

[Eternity Holdings](https://eternity-holdings-89f8c99223c1.herokuapp.com) has been designed as a mock prototype for a banking system. It's goal is to provide users with a virtual secure way to hold their money.

The Eternity Holdings prototype features a account creation & login system. A complete functional Deposit, Withdrawal and Currency Change system and Account Recovery features.

The project is a entirely back-end Python program. Heroku was introduced to test the program in a front-end environment. Click this [link](https://eternity-holdings-89f8c99223c1.herokuapp.com) to the Live version of Eternity Holdings.

---

# Table of Contents

1. [UX](#ux)

   - [Goals](#goals)
     - [Visitor Goals](#visitor-goals)
     - [Business Goals](#business-goals)
     - [User Stories](#user-stories)
   - [Visual Design](#visual-design)
     - [Flowcharts](#flowcharts)
     - [Google Sheet](#google-sheet)
     - [Colorama](#colorama)

2. [Features](#features)

    - [Main Menu](#main-menu)
        - [Account Creation](account-creation)
        - [Account Login](#account-login)
        - [Account Recovery](#account-recovery)
    - [Bank Hub](#bank-hub)
        - [Deposit & Withdawal](#deposit-&-withdrawal)
        - [Currency Convertor](#currency-convertor)
        - [Pin Change](#pin-change)
    - [Feature Ideas](#feature-ideas)
        - [Project Content](#project-content)
        - [Project Design](#project-design)

3. [Project Notes](#project-notes)

    - [GitHub Commits](#github-commits)

4. [Technology Used](#technology-used)

   - [Languages](#languages)
   - [Libraries](#libraries)
   - [Platforms](#platforms)
   - [Other Tools](#other-tools)

5. [Testing](#testing)

   - [Methods](#methods)
     - [Validation](#validation)
     - [General Testing](#general-testing)
   - [Bugs](#bugs)
     - [Known Bugs](#known-bugs)
     - [Fixed Bugs](#fixed-bugs)

6. [Deployment](#deployment)

    - [Github Deployment](#github-deployment)
        - [Github Preperation](#github-preparation)
        - [Github Instructions](#github-instructions)
        - [Google Sheets Instructions](#google-sheets-instructions)


7. [Credits and Contact](#credits-and-contact)

    - [Credits](#credits)
    - [Contact](#contact)

---

# UX

## Goals

### Visitor Goals

The target audience for Eternity Holdings are:

- Users that want a place to store their income.
- Users whom want to convert their funds easily.
- Users that don't want to be confused as to where and how to complete tasks.

The user goals are:

- To establish an Account with Eternity Holdings.
- To store funds in their Account.
- To withdraw those funds when needed.
- To use any currency they wish.
- To easily check account balance.
- To recover their account if they lost their pin or account numbers.

Eternity Holdings fills these goals by:

- Providing a clear & straight forward Account Creation & Login process. 
- Providing a deposit & withdrawal terminal once a user has logged in.
- Providing a Currency Converter system including a list of currently 11 supported currencies.
- Providing a quick & easy Account balance checker.
- Providing access to setup your Account recovery backup during Account Creation and later once logged in the ability to view, setup/change the Recovery Backup.
- Providing the ability to change the users Account Pin number.

### Business Goals

The Business Goals for Eternity Holdings are:

- Obtain more clients to build Bank balance.
- Be a respectable and trusted user bank.
- Be a good prototype showcase of a banking system.

### User Stories

1. As a User I want to be able to easily create and login to my account.
2. I'm someone who often misplaces and forgets numbers such as my Account Number and Pin. I want the ability to be able to get into my account if I lost them.
3. I want to be able to use different currencies, if it was one singular currency, it wouldn't be very flexible to use for me.
4. As a user I want to clearly read what i am looking at, too much white text on a screen can be very hard to read.

## Visual Design

### Flowcharts

Flowchart: A site called [Lucidchart](https://www.lucidchart.com) was used for the creation of the Project [Flowchart](https://lucid.app/lucidchart/2b48ac3d-3655-40a7-b44b-4afc8a233830/edit?viewport_loc=-1124%2C-212%2C9052%2C4612%2C0_0&invitationId=inv_d450b472-ad4d-46f3-9de1-6875b6845fb1). It helped visualize and plan the direction the project needed to take. In Python projects it is crucial to maintain a clear plan and general process you want to take your code. As frameworks helps build the foundations and develop front-end systems such as Websites a flowchart is invaluable to back-end coding.

### Google Sheet

For the purpose of this project, a Google sheet was used as a database for all account details. Eternity Holdings interacts with the Google sheet often to add and update data. To view the Google sheet please follow this [link]( https://docs.google.com/spreadsheets/d/1ivq5-UThXv3ynS0U6XLn5EbKDd-Uz_1iM0zv7xx-28g/edit?usp=sharing).

### Colorama

[Colorama](https://pypi.org/project/colorama/) is a Python library that was chosen to be used in Eternity Holdings. Once imported into the files and initiated by `init()`on line 37 in `run.py`lines of code could be colored to help improve the readability of text in the terminal.

Colorama was used extensively throughout the project with the use of colors such as Green, Red, Cyan & Yellow.

---
# Features

## Main Menu

The Main Menu is the first thing a user will see as soon as they load the program. It acts as the starting menu and connects the three major features of Eternity Holdings.
It prompts the user with 3 options to enter.

- 'CREATE' to call the `create_account` function to go to the Account Creator terminal.
- 'LOGIN' to call the `login_account` function to go to the Account Login terminal.
- 'RECOVER' to call the `acc_recovery` function to go to the Account Recovery terminal.

The function in the code is called `start_menu()` and located in `run.py` on line 80.
Utilizing `validate_mode` found in `utils.py` on line 41 and `validate_input` also found on line 73. These functions are constantly used throughout Eternity Holdings to handle user inputs. While `validate_mode` handles the expected input out of a list of options, `validate_input` regulates the user input and rejects invalid inputs such as `!$&+/,` special characters.

![Main menu image](startmenu.png)

### Account Creation

Account Creation functions are compiled in the `acc_creation.py` file. This is a major part of the banking system as users are required to create a account before having access to banking features. 
The `create_account` found on line 19 in `acc_creation.py` handles the intial account creation allowing users to input a Full Name & Date of Birth.

Eternity Holdings only allows 18+ users to create a account and uses `validate_dob` function on line 88 below to only accept valid dates of birth.

![Create Account image](create_acc.png)

Account Creation is also where the user is prompted a optional account recovery setup. This is a optional feature that users can establish once logged in also. It's purpose is to allow users a way to recover a lost account.

The function is called `create_backup_setup` on line 233 of `acc_creation.py`.

![Recovery backup](backup.png)

After this step and users details were previously confirmed, a account number and pin were generated and the users details were displayed in full again to write down, as they are nesasary for account login.

Accounts in Eternity Holdings are intended to be unique. In this current version, it is done based on the unique 9 digit Account number generated by `acc_num_generator` on line 200 of `acc_creation.py`.

![Account Creation complete](acc_create_complete.png)

### Account Login

Account Login functions are compiled in the `acc_login.py` file. This is the second major part of the banking system that goes hand in hand with with creating a account. Users are to expect to login to the account they created.

The function `login_account` on line 30 in `acc_login.py` prompts users to enter Full Name, Account Number and Pin. The user inputs are checked using `login_acc_checker` on line 103 in the same file. As all accounts are stored in a project Google Sheet the function takes the data from the sheet and compares it with the details provided, if a match is found the user is logged into their account.

![Account Login image](acc_login.png)

### Account Recovery

Account Recovery functions are compiled in the `acc_recovery.py` file. This was a feature implemented for users to recover their account if they lose their details. Users optionally have the ability to setup their recovery backup details when they create a account, and also a ability to do so upon logging in if they wish to change them.

The `acc_recovery` function on line 15 acts a central function for this feature. It's purpose is to prompt users with basic direction and connects two associated functions together. If the User has their backup information, the `acc_recovery_questions` on line 111 will be called.

![Account Recovery image](recoverymenu.png)

The questions will be checked with the details saved on the Google sheet database. The `get_backuo_data` function on line 162 in the `utils.py` file is used. If a match is found, account details will be printed to the terminal.

![Recovery Questions image](recoveryquest.png)

If a user does not know their account recovery the `forgot_acc_recovery` function will be called. Users will be informed at this time there is no way to gain access to their account and need further customer support.

![Forgot Recovery image](recoveryforgot.png)

## Feature Ideas

### Project Content

- A way to send funds to another account with a message, and a way to accept or decline funds sent my a different account.
- Bank statements to view a record of recent deposits & withdrawals as well as recent accepted or declined gifted funds.
- Account Recovery to utilize user emails and send emails to account owners for confirmation.
- More support for other currencies.
- Currency conversion to use active and up to date money conversions over manual set rates established in dictionary.

### Project Design

- Restructure file functions and store bank functions in seperate file.
- Reduce passed parameters to functions for better performance.

---

# Project Notes

## Github Commits

For Eternity Holdings, aome Github commits were larger than anticipated. The reason behind certain commits being very large was due to a major code restructure later in the project timeline. 

This divided some large sections of code into different `.py` files for better code maintainability. A example of this being done can be found under the commit title 
"Changed: Seperated Create/ultility Functions into files." Here is a [link](https://github.com/MarcusFDev/eternity-holdings-project3/commit/ef9f6e08878705c861a5c92d2e12ab4cb96a0031) to the commit.

---

# Technology Used

## Languages

- [Python](https://github.com/MarcusFDev/eternity-holdings-project3/blob/main/run.py)
    - Complete Project Functionality.

## Libraries

- [Colorama](https://pypi.org/project/colorama/)
    - For Terminal print to be colored for better project readability.
- [Money](https://pypi.org/project/money/)
    - For the user's Money to be formatted in a realistic way. 
- [GSpread](https://pypi.org/project/gspread/)
    - For Google Sheet functionality within the project to store all user Data.
- [PPrint](https://docs.python.org/3/library/pprint.html)
    - For dictionaries to be printed to the terminal in a better formatted way.
- [OS](https://docs.python.org/3/library/os.html)
    - For the use of a `clear()` function to maintain terminal readability.
- [Random](https://docs.python.org/3/library/random.html)
    - For generating random assortment of numbers used for Account Pin & Number.
- [Re](https://docs.python.org/3/library/re.html)
    - For excluding special characters in `validate_input` and matching email structure in `validate_email`.

## Platforms

- [Github](https://github.com/MarcusFDev/eternity-holdings-project3)
    - Storing code remotely.
- [Gitpod](https://www.gitpod.io)
    - IDE for project creation and development.
- [Heroku](https://eternity-holdings-89f8c99223c1.herokuapp.com)
    - Used for project deployment for a Python back-end project to be displayed on a front-end site.

## Other Tools

- [CI Python Linter](https://pep8ci.herokuapp.com)
    - Code Institute Python linter was used to validate every Python file.

# Testing

## Methods

### Validation

Each Eternity Holdings `.py` file was validated by the Code Institute Python Linter. Each file returning the same result.

- `run.py` file results:

![run.py Validation image](assets/images/runpy_validate.png)

- `acc_creation.py` file results:

![acc_creation.py Validation image](assets/images/acc_creation_validate.png)

- `acc_login.py` file results:

![acc_login.py Validation image](assets/images/acc_login_validate.png)

- `utils.py` file results:

![utils.py Validation image](assets/images/utilitypy_validate.png)

- `acc_recovery.py` file results:

![acc_recovery.py Validation image](assets/images/acc_recovery_validate.png)

### General Testing

- After every alteration that was made to the code, everything was prompty tested to check for noticable changes.
- Entire program functionality for every feature together & individually was tested thoroughly in both the GitPod IDE terminal & Heroku deployment terminal.
- Every user input was tested for unintended functionality utilizing the following ways:
    - Standard single `a` and multiple `abc` latin alphabet letters.
    - Standard single `1` and multiple `123` numbers.
    - A empty `Enter` with no text content.
    - A `Enter` that contains only `Blank` spacing.
    - A user input containing `?@,/+!` special characters where not intended.
- Google Sheet database was observed each time a new data entry was sent to test the spreadsheet was correctly updating as intended.
- Program was tested by two other individuals.

## Bugs

### Known Bugs

No active known bugs have been detected in the program.

### Fixed Bugs

- Fixed a issue that caused a unintended error entering `.` in the `acc_deposit` & `acc_withdraw` user inputs.
- Fixed a user input issue that caused account recovery passwords to not be case sensitive.
- Fixed a input issue that allowed special characters, blank spaces & empty enters to be accepted when updating the database.
- Fixed multiple terminal errors relating to function paramaters after major code restructure.
- Fixed Docstrings to better explain functions & files respectively.
- Fixed a currency conversion issue that caused loss or multiply of currency upon conversion values being changed.

# Deployment

[Eternity Holdings](https://eternity-holdings-89f8c99223c1.herokuapp.com) is a entirely back-end Python project. It does not work as a front-end application on its own. 

To experience the project outside of a IDE terminal environment [Heroku](https://eternity-holdings-89f8c99223c1.herokuapp.com) was used to bring Eternity Holdings to a front-end experience via a website terminal. 

A Code Institute [template](https://github.com/Code-Institute-Org/p3-template) was used as a building crucial building block to bring Eternity Holdings to a front-end viewing state.

To view my Heroku deployment of Eternity Holdings please follow this [link]( https://eternity-holdings-89f8c99223c1.herokuapp.com).

## Github Deployment

### Github Preparation

Requirements:

- You need a GitHub account.
- You need a IDE such as [GitPod](https://gitpod.io).
- You need a Google account.

### Github Instructions

1. Log into your Github account and navigate to this link to the project repository: https://github.com/MarcusFDev/eternity-holdings-project3.
2. You can choose to create your own repository and copy or clone the project code. If making your own repository you must use the [template](https://github.com/Code-Institute-Org/p3-template) for the project to function as intended.
3. Upon creating a workspace in your IDE locate the `requirements.txt` file. If missing, create one with the exact name. In the terminal enter `pip3 freeze > requirements.txt` to activate all dependencies.
4. Please see and follow Google Sheets Instructions below and return to Step 5. 
5. Drag & Drop the Google Sheets `.json` file into your project and rename it to `creds.json`.
6. Then type into the terminal `python3 run.py` to start the program.

### Google Sheets Instructions

1. Login to Google Sheets and make a copy of this [spreadsheet](https://docs.google.com/spreadsheets/d/1ivq5-UThXv3ynS0U6XLn5EbKDd-Uz_1iM0zv7xx-28g/edit#gid=0). Remove 'Copy of' from the sheet title.
2. To connect the Google sheet to the IDE environment first go to the [Google Cloud](https://console.cloud.google.com/welcome?pli=1&project=lovesandwiches-419910) service. Click 'Select a project' then 'New Project'.
3. Name the project 'Eternity Holdings' and hit create. Make sure to navigate to your project dashboard.
4. Click APIs & Services then Library. Search for Google Drive API and enable it. This will take you to a page where you can click 'Create Credentials'. These steps must be followed correctly:

    1. Choose 'Google Drive API'.
    2. Select 'Application Data'.
    3. Select 'No, I'm not using them'.
    4. Click Next.
    5. Enter the Service Account name 'Eternity Holdings' and click Create.
    6. Choose 'Editor' then press Continue and then Done.
    7. Now, click on the service account that has been created, then Click 'Keys'.
    8. Click on 'Add Key' and select 'Create New Key'.
    9. Select JSON and then click Create. This will trigger a `json` file with your API credentials in it to download to your computer. 

5. Now search the API library for the Google Sheets API and select 'Enable'.

## Credits and Contact

### Credits

IDE Template:

- This Code Institute [template](https://github.com/Code-Institute-Org/p3-template) was used to set up the IDE environment for the Eternity Holdings project.

### Contact

Please feel free to reach out if you have any questions. Contact me via my email at marcusf.dev@gmail.com