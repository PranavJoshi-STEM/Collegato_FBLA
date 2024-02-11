"""
Description:
    This file has all the functions needed to set/get any data.
"""

# Imports
import os

# Import libraries
from libraries import helper, auth, configs




# ------ Connect to Database ------
# Get the directory of the main.py file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Connecting to a database in the dir/ directory
db_path = os.path.join(current_directory, '..', 'collegato_database.db')

# get encryption key --- Temporary ---
ENCRYPTION_KEY_PATH = helper.get_path(file=configs.ENCRYPTION_KEY_NAME)

KEY = helper.get_or_generate_encrypt_key(ENCRYPTION_KEY_PATH)




# ------ Users: setters/getters ------
# Function to get user details
def get_user_details(email, password, key):
    if helper.verify_password(email, password):
        result = helper.execute_query(
            'SELECT firstname, lastname FROM users WHERE email=?', (email,))
        if result:
            if key == 'both':
                return {'firstname': result[0], 'lastname': result[1]}
            else:
                return {'firstname': result[0], 'lastname': result[1]}[key]
    else:
        print('get_user_details(): User not verified')
        return None


# Function to set individual user details
def set_user_details(conn, email, password, key, new_data):
    if helper.verify_password(email, password):
        if key in ['firstname', 'lastname']:
            result = helper.execute_query(
                'UPDATE users SET {}=? WHERE email=?'.format(key),
                (new_data, email))
            return True
        elif key == 'both':
            result = helper.execute_query(
                'UPDATE users SET {}=? WHERE email=?'.format('firstname'),
                (new_data['firstname'], email))
            result = helper.execute_query(
                'UPDATE users SET {}=? WHERE email=?'.format('lastname'),
                (new_data['lastname'], email))
            return True
    return False


# Create a new user
def create_user(conn, email, password, firstname, lastname):
    print(
        f'create_user({email}, {password}, {firstname}, {lastname}) is \
        being ran')
    try:
        # Check if the email is already in use
        result = helper.execute_query('SELECT * FROM users WHERE email=?',
                                      (email,))
        if result:
            print(f'create_user({email}) already exists!')
            return False  # User with this email already exists

        # Hash the password and insert the user details into the database
        hashed_password, salt = helper.hash_password(password)
        result = helper.execute_query(
            'INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
            (helper.format_email(email), hashed_password, salt,
             str([]), helper.format_name(firstname),
             helper.format_name(lastname))
        )
        return True  # User account created successfully
    except Exception as e:
        print(f"Error: {e}")
    return False  # User account not created


# Delete a user
def delete_user(conn, email, password):
    if helper.verify_password(email, password):
        user_targets = \
        helper.execute_query('SELECT card_targets FROM users WHERE email=?',
                             (email,))[0]
        user_targets = eval(user_targets)  # converting str list to list type
        if user_targets:  # Checking if user_targets exist
            for target in user_targets:
                helper.execute_query('DELETE FROM cards WHERE target=?',
                                     (target,))
        result = helper.execute_query('DELETE FROM users WHERE email=?', (
            helper.format_email(email),))

        print(f'Deleted email: {email}')
        print('Deleted User Data')

        return True  # User account deleted successfully if it existed
    else:
        return False


# Function to set a new password
def set_new_password(conn, email, old_password, new_password):
    if helper.verify_password(email, old_password):
        hashed_password, salt = helper.hash_password(new_password)
        result = helper.execute_query(
            'UPDATE users SET password_hash=?, salt=? WHERE email=?', (
                hashed_password, salt, email)
        )
        print(f'Changed password to {new_password}')
        return True
    return False


# ------- Cards: setters/getters ------
# Function to retrieve all card details
def all_card_details(email, password):
    if helper.verify_password(email, password):
        result = helper.execute_query(
            'SELECT card_targets FROM users WHERE email=?', (email,))
        card_targets = eval(result[0])
        card_details = {}

        for target in card_targets:
            result = helper.execute_query(
                'SELECT * FROM cards WHERE target=?', (target,))
            if result:
                # Convert tags from string to list
                data = result
                card_details[target] = {
                    'title': data[1], 'description': data[2],
                    'tags': eval(data[3])
                }

        return card_details
    return None


# Function to add a card
def add_card(email, password, title, description, tags):
    print(f'add_card({email}, {password}, {title}, ' \
          + f'{description}, {tags}) is being ran')
    if helper.verify_password(email, password):
        # Generate a unique target value (you can use your own logic here)
        target = helper.generate_unique_target(email)
        # Convert tags from list to string
        tags_str = str(tags)
        # Insert the card into the cards table
        helper.execute_query(
            'INSERT INTO cards VALUES (?, ?, ?, ?)', (
                target, title, description, tags_str
            ), returnValue=False
        )
        # Get the current user's card_targets
        result = helper.execute_query(
            'SELECT card_targets FROM users WHERE email=?', (email,))
        current_card_targets = eval(result[0]) if result else []
        # Append the new target to the current card_targets
        current_card_targets.append(target)
        # Update the user's card_targets
        helper.execute_query('UPDATE users SET card_targets=? WHERE email=?', (
            str(current_card_targets), email), returnValue=False)
        return target
    print(f'add_card(): User not verified.')
    return False


# Function to delete a card
def delete_card(email, password, target_list):
    if helper.verify_password(email, password):
        for target in target_list:
            result = helper.execute_query(
                'DELETE FROM users WHERE email=? AND ? IN (card_targets)', (
                    email, target))
            result = helper.execute_query(
                'DELETE FROM cards WHERE target=?', (target,))
        return True
    return False


# Function to set individual card details
def set_card(email, password, target, key, new_data):
    if helper.verify_password(email, password):
        if key == 'all':
            user_targets = eval(helper.execute_query(
                'SELECT card_targets FROM users WHERE email=?',
                (email,))[0])
            if target in user_targets:
                for key in ['title', 'description', 'tags']:
                    # Check if the card belongs to the user
                    query = 'UPDATE cards SET {}=? WHERE target=?'.format(key)
                    helper.execute_query(query, (new_data[key], target),
                                         returnValue=False)
                return True
        elif key in ['title', 'description', 'tags']:
            user_targets = eval(helper.execute_query(
                'SELECT card_targets FROM users WHERE email=?',
                (email,))[0])
            if target in user_targets:
                # Check if the card belongs to the user
                query = 'UPDATE cards SET {}=? WHERE target=?'.format(key)
                helper.execute_query(query, (new_data, target),
                                     returnValue=False)
                return True
        else:
            print(f'set_card({email}, {password}, {target},' \
                  + f'{key}, {new_data}): Invalid key!')
    else:
        print(f'set_card({email}, {password}, {target},' \
              + f'{key}, {new_data}): User not verified!')
    return False


# Function to get individual card details
def get_card(email, password, target, key):
    if helper.verify_password(email, password):
        if key == 'all':
            result = helper.execute_query(
                'SELECT * FROM cards WHERE target=?', (target,))
            if result:
                # Convert tags from string to list
                data = result  # Access the first tuple in the result
                card_details = {
                    'title': data[1], 'description': data[2],
                    'tags': eval(data[3])
                }
                return card_details
        elif key in ['title', 'description', 'tags']:
            result = helper.execute_query(
                'SELECT * FROM cards WHERE target=?', (target,))
            if result:
                # Convert tags from string to list
                data = result  # Access the first tuple in the result
                card_details = {
                    'title': data[1], 'description': data[2],
                    'tags': eval(data[3])
                }
                return card_details[key]
        elif key == 'target':
            return target
        else:
            print(f'get_card({email},{password},{target},{key}): Invalid key')
    else:
        print(f'get_card({email}, {password}): User not verified!')
        return None
    