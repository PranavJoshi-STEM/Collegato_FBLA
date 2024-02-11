"""
PLEASE RUN THIS FILE TO RUN THE PROJECT.  ANY OTHER FILE WILL NOT RUN THE
PROJECT.

Names: Pranav Joshi and Yajat Mittal
CNLC Year: 2024
Project name: Collegato (Server)
Description:
    This server is needed to run the Collegato Client.
Notes:
    - This project will create several files
Code-choices:
    This entire project uses a file structure similar to real-world projects
    in development teams.  Additionally, everything is coded using Python's
    PEP-8 code style and has comments (when necessary) for improved code
    readability.
"""


# Import statements
from flask import Flask, request, jsonify
import sqlite3
import time # time the amount of time between recieving and sending
#from pysqlcipher3 import dbapi2 as sqlcipher

# Import libraries
from libraries import auth, setget, helper, configs

# Set up flask
app = Flask(__name__)


# ------ Connect to Database ------
# get paths
ENCRYPTION_KEY_PATH = helper.get_path(file=configs.ENCRYPTION_KEY_NAME)
COMMUNICATION_KEY_PATH = helper.get_path(file=configs.COMMUNICATION_KEY_NAME)
DB_PATH = helper.get_path(file=configs.DB_NAME)

# get encryption key
key = helper.get_or_generate_encrypt_key(ENCRYPTION_KEY_PATH)
# create communication key
helper.get_or_generate_comm_key(COMMUNICATION_KEY_PATH)


# Encrypt database and create tables
# replaced sqlite3 with sqlcipher
with sqlite3.connect(helper.get_path(DB_PATH)) as connection:
    cursor = connection.cursor()

    # Attach the encrypted database
    #connection.execute(f'ATTACH DATABASE ? AS encrypted KEY ?', (
    #    helper.database_path(exit_amount='.'), encryption_key))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            salt TEXT,
            card_targets TEXT,
            firstname TEXT,
            lastname TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            target TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            tags TEXT
        )
    ''')

    # Detach the encrypted database
    #connection.execute('DETACH DATABASE encrypted')



# ------ Test commands (used in testing) ------
    #setget.delete_user(connection, 'joshipn2018@gmail.com', 'password123@@')
    #setget.create_user(connection, 'joshipn2018@gmail.com', 'password123@@', 
    # 'Pranav', 'Joshi')


# ------ Handle Commands ------
# create signup instance
signup_instance = auth.Signup()


# Endpoint for handling client requests
@app.route('/execute_command', methods=['POST'])
def execute_command():
    tic = time.perf_counter()
    data = helper.decrypt_data(request.get_json(),
                helper.get_or_generate_comm_key(COMMUNICATION_KEY_PATH))

    command = data.get('command')
    params = data.get('params', {})
    print(f'\nGOT REQUEST:\n\tcommand: {command}\n\tparams: {params}\n')

    if command is None:
        return helper.encrypt_data({"error": "Command not provided"},
                helper.get_or_generate_comm_key(COMMUNICATION_KEY_PATH)), 400

    # Process the command
        # auth_phase
    if command == "login":
        result = auth.login(**params)
    elif command == "send_confirmation":
        result = signup_instance.send_confirmation(**params)
    elif command == "signup":
        result = signup_instance.signup(connection, **params)
    elif command == "forgot_password":
        result = auth.forgot_password(**params)

        # work_phase
    elif command == "delete_user":
        result = setget.delete_user(cursor, **params)
    elif command == "set_user_details":
        result = setget.set_user_details(cursor, **params)
    elif command == "get_user_details":
        result = setget.get_user_details(**params)
    elif command == "all_card_details":
        result = setget.all_card_details(**params)
    elif command == "set_card":
        result = setget.set_card(**params)
    elif command == "get_card":
        result = setget.get_card(**params)
    elif command == "add_card":
        result = setget.add_card(**params)
    elif command == "delete_card":
        result = setget.delete_card(**params)
    elif command == "set_new_password":
        result = setget.set_new_password(connection, **params)
    else:
        result = {"error": "Invalid command"}

    return_data = helper.encrypt_data({'encrypted_data': str(result)},
            helper.get_or_generate_comm_key(COMMUNICATION_KEY_PATH))
    toc = time.perf_counter()
    print(f'\tSERVER REPLIED IN {toc - tic:0.4f} SECONDS: {toc}')
    return return_data


# Entry point of script
if __name__ == '__main__':
    app.run(debug=True, port=configs.PORT)
