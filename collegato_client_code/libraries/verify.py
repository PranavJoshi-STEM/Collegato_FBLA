"""
Description:
    This code contains all functions that are used to verify a status
    with Better Entry.
"""

from email_validator import validate_email, EmailNotValidError

# this verifies that the email is valid
def valid_email(email):
	try:
		# validate and get info
		v = validate_email(email, check_deliverability=False)
		print(f"valid_email(): {v['email']} ==> True")
		return True
	except EmailNotValidError as e:
		# email is not valid, exception message is human-readable
		print(f"valid_email(): {email} ==> False")
		return False


# this verifies if a password is secure enough
# requirements: ≥1 num, ≥2 special chars, ≥8 in length
def valid_password(password):
	# check if the password is at least 8 characters long
    if len(password) < 8:
        return False
    
    # check if the password contains at least one digit
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break
    if not has_digit:
        return False
    
    # check if the password contains at least two special characters
    special_chars = "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~"
    special_count = 0
    for char in password:
        if char in special_chars:
            special_count += 1
    if special_count < 2:
        return False
    
    # if all the checks pass, the password is valid
    return True


# checks if a name is valid
def valid_name(name):
    # make sure the name isn't blank
    if name=='':
         return False
    allowed_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]
    for i in range(len(name)):
         if name[i] not in allowed_chars:
              return False
    return True


# function to test if a string is a valid code (when applicable)
def is_int(s, check_len=False, target_len=6):
    if check_len:
        state = (s.isdigit()) and (len(s) == target_len)
        print(f'is_int(): {s} ==> {state}')
        return state
    else:
        state = s.isdigit()
        print(f'is_int(): {s} ==> {state}')
        return state
        