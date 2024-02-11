"""
Description:
    This program contains all the extra functions needed to run the server.
"""

# Import statements
    # database manipulation
import smtplib
import threading
import sqlite3
#from pysqlcipher3 import dbapi2 as sqlcipher 
# Note: Line 120 in SQLiteContextManager was edited
    # generators
import random # generate card
import time  # generate card
import string # generating password
    # client-server communication
import os
import json
import sys
    # security
import bcrypt # hashing
from functools import lru_cache # memoize hashed inputs
from cryptography.fernet import Fernet #encryption/decryption
import hmac # prevent timing attacks
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Import libraries
from libraries import email_configs, configs




# ------ Encryption ------
# This will encrypt data
def encrypt_data(data, byte_key):
    print('Encrypting...')
    # Use Fernet for encryption
    cipher = Fernet(byte_key)
    data = json.dumps(data)
    ciphertext = cipher.encrypt(data.encode())
    return ciphertext


# This will decrypt data
def decrypt_data(ciphertext, byte_key):
    print('decrypting data')
    # Use Fernet for decryption
    print(byte_key)
    cipher = Fernet(byte_key)
    enc_data = ciphertext['encrypted_data'].encode()
    print(f'\tGOT: {enc_data}')
    # Problematic after here
    decrypted_data = cipher.decrypt(enc_data)
    # Decode the decrypted bytes to a string before loading as JSON
    decrypted_data_str = decrypted_data.decode('utf-8')
    # Load the JSON data
    decrypted_data_dict = json.loads(decrypted_data_str)
    return decrypted_data_dict


# This is for encrypting the args when passed into the execute query func,
# hence encrypted data is stored in the database; ensuring security. 
def encrypt_args(args: tuple, byte_key: bytes) -> tuple:
    # key, mode (AES cipher initialization)
    cipher = AES.new(byte_key, AES.MODE_ECB) 
    cipherargs = []
    for arg in args: # iterating through the args, and encrypting them
        try:
            # conditions on when to encode/convert to str/leave as is,
            #  based on type (for padding)
            if type(arg) == bytes:
                padded_arg = pad(arg, AES.block_size)
            elif type(arg) == list:
                    padded_arg = pad(str(arg).encode(), AES.block_size)
            else:
                padded_arg = pad(arg.encode(), AES.block_size)
            encrypted_arg = cipher.encrypt(padded_arg) # encrypting padded arg
            # adding encrypted args into a list
            cipherargs.append(encrypted_arg) 

        except:
            pass
    return tuple(cipherargs)  # returning tuple of encrypted args


# This is for decrypting args, eg. when trying to get info. 
def decrypt_args(cipherargs: tuple, byte_key: bytes) -> tuple:
    # key, mode (AES cipher initialization)
    cipher = AES.new(byte_key, AES.MODE_ECB) 
    decrypted_args = []
    
    for arg in cipherargs: # iterating through the args, to decrypt
        padded_arg = cipher.decrypt(arg) # decrypting arg
        # adding decrypted arg to a list, removing padding
        decrypted_args.append(unpad(padded_arg, AES.block_size).decode())  

    return tuple(decrypted_args) # returning decrypted args as a tuple 
    

# ------ Generate or get keys ------
# generates or accesses a file with an encryption key
def get_or_generate_encrypt_key(filename):
    # Connecting to a database in the dir/ directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # get path of file
    if configs.COMPILING_TO_EXE:
        dir_path = os.path.dirname(sys.executable)
    key_file_path = os.path.join(dir_path, '..', filename)
    # Check if the key file exists
    if os.path.exists(key_file_path):
        with open(key_file_path, 'rb') as key_file:
            return key_file.read()
    else:
        # Generate a new key and save it to the file
        key = (
            b'>\x1a9\x15\x82\x8d|\xda\xb7\xa7'
            b'0vw\xbe\xfc\xad\x18\x97\xdeB\xc3\xa9'
            b'nu1\x1c\x04\xf0\x96P\xf06'
        )
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
        return key

# generates or accesses a file with a key
def get_or_generate_comm_key(filename):
    # Connecting to a database in the dir/ directory
    dir_path = os.path.dirname(os.path.abspath(__file__))
    # get path of file
    if configs.COMPILING_TO_EXE:
        dir_path = os.path.dirname(sys.executable)
    key_file_path = os.path.join(dir_path, '..', filename)
    # Check if the key file exists
    if os.path.exists(key_file_path):
        with open(key_file_path, 'rb') as key_file:
            return key_file.read()
    else:
        # Generate a new key and save it to the file
        key = b'XNL1pDU_uxxoXS4vxkjZDbkF_mAg-wbUIQXYiRKm_Z0='
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
        return key




# ------ Database ------
# Thread-local variable to store connections
local = threading.local()

# Get path of database
def get_path(file=f'{configs.DB_NAME}', exit_amount=''):
    # get sub directory
    sub_dir_path = os.path.dirname(os.path.abspath(__file__))
    # get path of file
    if configs.COMPILING_TO_EXE:
        sub_dir_path = os.path.dirname(sys.executable)
    # Get the directory of the project
    dir_path = os.path.dirname(sub_dir_path)
    # Connecting to a database in the dir/ directory
    path = os.path.join(dir_path, exit_amount, file)
    return path


# get paths and key
ENCRYPTION_KEY_PATH = get_path(file=configs.ENCRYPTION_KEY_NAME)
key = get_or_generate_encrypt_key(ENCRYPTION_KEY_PATH)


class SQLiteContextManager:
    def __enter__(self):
        self.connection = sqlite3.connect(get_path(), check_same_thread=False)
        self.cursor = self.connection.cursor()
    
        return self.cursor
    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(local, "connection"):
            local.connection.commit()
            local.connection.close()
            del local.connection
        if exc_type is not None:
            print(f"Error: {exc_type}, {exc_value}")
        return True


# Execute queries
def execute_query(query, args=None, returnValue=True):
    tic = time.perf_counter()
    with SQLiteContextManager() as cursor:
        if args is not None:
            args = encrypt_args(args, key)
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.connection.commit()
        cursor.connection.close()
        toc = time.perf_counter()
        print(f'\n\t execute_query() TOOK {toc-tic:0.4f} SECONDS')
    if returnValue and result != []:
        return decrypt_args(result[0], key)
        



# ------ Passwords ------
# Function hashes password, after adding a salt. 
@lru_cache(maxsize=None) # 'None' means no limit on cache size
def hash_password(pwd, salt=None, email=''):
    # ^^^ add email input to ensure that each account needs to start their
    # cache from zero entries
    tic = time.perf_counter()
    # Converting pwd to bytes
    pwd = bytes(pwd, "utf-8")

    if salt==None:
        # Generating salt
        salt = bcrypt.gensalt(rounds=15)
    
    # Converting salt to bytes
    elif type(salt) != bytes:
        salt = bytes(salt, "utf-8")
    
    # Hashes password with salt.
    hashed_pwd = bcrypt.hashpw(pwd, salt)
    
    # Returns pwd hash and salt.
    toc = time.perf_counter()
    print(f'\thash_password() TOOK {toc-tic:0.4f} SECONDS')
    return hashed_pwd, salt


# Function checks user password, comparing it to password hash. 
def check_password(pwd, salt, pwd_hash):
    # Converting pwd to bytes
    pwd = bytes((salt+pwd), "utf-8")
    # Returns if pwd is correct. (True, False)
    return bcrypt.checkpw(pwd, pwd_hash)


# take the email and password and see if its a valid account
def verify_password(email, password):
    result = execute_query('SELECT password_hash, salt FROM users WHERE \
email=?', (email,))
    if result:
        stored_hash, salt = result
        hashed_password, _ = hash_password(password, salt, email)
        return hmac.compare_digest(bytes(hashed_password), bytes(stored_hash, 
                                                                'utf-8'))
    
    print(f'{email}, {password} -> not verified in database')
    return False


# takes the email, and checks if it exists in the database
def verify_email(email):
    result = execute_query('SELECT * FROM users WHERE email=?', (email,))
    if result:
        return True
    return False




# ------ Contact user/generate ------
# generate a random 6-digit code to be sent to the user
def generate_code():
    code = ""
    for i in range(6):
        code += str(random.randint(0,9))
    return code


# Function generates a random password to send the user,
# when password reset email is requested. 
def generate_pwd():
    # Choose a random length between 10 and 15
    length = random.randint(10, 15)
    special_characters = string.punctuation
    pwd = ''
    # Add at least one number
    pwd += str(random.randint(0, 9))
    # Add two special characters
    pwd += random.choice(special_characters)
    pwd += random.choice(special_characters)
    # Add remaining characters
    for _ in range(length - 3):
        pwd += random.choice(string.ascii_letters + string.digits + \
                             special_characters)
    # Shuffle the characters to make it random
    pwd_list = list(pwd)
    random.shuffle(pwd_list)
    return ''.join(pwd_list)


# Generate a unique target based on the time
def generate_unique_target(email):
    # Get current timestamp in milliseconds
    timestamp_ms = int(time.time() * 1000)
    # Generate a random number incase multiple cards are created 
    # at the same time
    random_num = random.randint(1_000, 10_000)
    # Create a unique target using the timestamp
    target = f"{timestamp_ms}_{email}_{random_num}"

    return target


# send the email
def send_email(email, subject, body):
    email = format_email(email)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=email_configs.SENDING_EMAIL,
                         password=email_configs.SENDING_EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=email_configs.SENDING_EMAIL,
            to_addrs=email,
            msg=f"Subject:{subject}\n\n{body}")


# ------ Format ------
def format_name(s:str) -> str:
    if s is None:
        return None 
    else:
        return s.title()


def format_email(s:str) -> str:
    if s is None:
        return None
    else:
        return s.lower()
