"""
Description:
    This file returns a string which is an email template.
Note:
    This file does not follow PEP-8's 79 char line rule since it is much more
    readable when written normally.  This more accurately follows Python's zen
    of code being readable by essentially treating this as a .txt file.
"""

# ------ Constants ------
# Send emails with these credentials
SENDING_EMAIL = "noreply.collegato@gmail.com"
SENDING_EMAIL_PASSWORD = "yzkg zjbc afkp zohk"




# ------ Email Templates ------
def forgot_password_email(new_pwd):
    subject = "[COLLEGATO] New Password"
    body = f"""Dear Collegato User,
We received a request to reset your Collegato account password. Below is your temporary password:

{new_pwd}

Please use this temporary password to log in to your account and change this password afterwards.

Please note that this email is automated, and responses to it will not be checked. Please do not reply.

Thank you for choosing Collegato!

Best regards,
Collegato Team.
"""
    return {'subject':subject, 'body':body}


def confirm_signup_email(gen_code):
    subject = "[COLLEGATO] Confirm Your Collegato Account - 6-Digit Code"
    body = f"""Dear user,

Thank you for choosing Collegato! We're excited to welcome you to our community.

To complete the sign-up process and confirm your account, please use the following 6-digit code:

{gen_code}

Please enter this code into the designated field on our app.

If you did not sign up for Collegato or received this email in error, please disregard it. Your account will not be activated.

Please note that this email is automated, and responses to it will not be checked. Please do not reply.

Thank you for choosing Collegato!

Best regards,

Collegato Team"""

    return {'subject':subject, 'body':body}



def email_exists():
    subject = "[COLLEGATO] Collegato Account Already Exists - Sign-Up Request"
    body = """Dear Collegato User,
    
We received a sign-up request, using your email; despite an existing account. 

If it was you that attempted to sign-up, please remember only one account per email is allowed. 

If you still wish to proceed with creating a new account using this email, kindly delete your existing account.

If the sign-up request or confirmation wasn't initiated by you, please feel free to disregard this email.

Please note that this email is automated, and responses to it will not be checked.  Please do not reply.

Best regards,

Collegato Team"""
    return {'subject':subject, 'body':body}
