# SecTools
SecTools for IaM

Tool used to automate the process of Onboarding for certain users

# Installation
What will be needed are some tools required in python:

Recommended to clone this request to a USB. From the git clone, open a terminal from this location and run the following command for the `requirements.txt` file:

`pip3 -r install requirements.txt`

# Usage

To use the application you will need to create a creds.py file with the applicable variables that are mentioned within the `config.txt` file.
You will also need to load the users in the `Onboarding/db/empemails.csv` file, as this is the main file the tool uses to put in user information.

To Run:

`python3 login_session_Ops.py`

Which will prompt the user to pick which instance they would like to create accounts for. This will not automatically click the accounts, as `save` still needs to be clicked, but will however preconfigure user information.

<!--- YnVnZ3k0Mg== --->
