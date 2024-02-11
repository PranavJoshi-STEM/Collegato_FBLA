"""
Description:
    This file contains all the functions related to authentifying the user
    or managing their account.
"""

# Import libraries
from libraries import helper, setget, email_configs


# ------ Signup ------
class Signup:
    def __init__(self):
        self.gen_code = helper.generate_code()


    # Send an email to the user
    def send_confirmation(self, email):
        email = helper.format_email(email)
        result = helper.verify_email(email)
        if not result: # email doesn't exist
            #Server sends a 6-digit-code to the email to confirm the email
            print("Email is being sent. ")
            template = email_configs.confirm_signup_email(self.gen_code)
        else: # email exists
            template = email_configs.email_exists()
            print(f'{email} -> exists in database')
            
        helper.send_email(email, template['subject'], template['body'])
        
        # if email exists (true) returns false as email isn't sent
        return not result 
           

    # Signs the user up if the email is correct
    def signup(self, conn, email:str, password:str, firstname:str,
               lastname:str, code:str) -> bool:
        '''Server creates an account if the 6-digit-code is correct;
        False if it failed, True if it worked
        Note:
            - Email will be all lower case letters (when applicable)
            - Firstname/lastname will only have first letter capitalized
            (.title())'''
        if code == self.gen_code:
            # extract data
            email = helper.format_email(email)
            firstname = helper.format_name(firstname)
            lastname = helper.format_name(lastname)
            try:
                print("Adding user info...")
                setget.create_user(conn, email, password, firstname, lastname)
            except Exception as e:
                print(f"Error: Email exists in database. {e}")
            
            # reset generated code
            self.gen_code = helper.generate_code()
            return True

        else:
            # reset generated code
            print(f"Got: {code} | Correct Code: {self.gen_code}")
            return False


# ------ Forgot Password ------
# Resets password of the email's account
def forgot_password(email, password, new_pwd=helper.generate_pwd()):
    """Server sends a temporary password to the email's inbox which can be
    used to login.  User can change password once they login."""
    result = helper.verify_email(email)
    if result:
        template = email_configs.forgot_password_email(new_pwd)
        hashed_password, salt = helper.hash_password(new_pwd)
        result = helper.execute_query(
            'UPDATE users SET password_hash=?, salt=? WHERE email=?', (
                hashed_password, salt, email))
        print(f'Changed password to {new_pwd}')
        helper.send_email(email, template['subject'], template['body'])
    else:
        print(f"{email} -> doesn't exist in database")


# ------ Login ------
def login(email, password):
    resp = setget.get_user_details(email, password, 'both')
    # resp should be type None or dict
    if resp==None:
        return [False, None]
    else:
        return [True, resp]
