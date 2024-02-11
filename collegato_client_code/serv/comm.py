
'''
Description:
    This file contains all the functions that are used to communicate with
    the server.
'''

# Import statements
import requests # communication
#import httpx # communication
import json # type conversion
import os # paths
import ast # type conversion
import time # time the amount of time the function takes
from cryptography.fernet import Fernet # encryption

# Import configs
from configs.config import PORT, BASE_URL


# Function to set email and password
class Convey:
    def __init__(self):
        # --- CREATE SESSION ---
        self.session = requests.Session()
        #self.session = httpx.Client()

        # --- SET DEFAULT EMAIL, PASSWORD ---
        self.email = ''
        self.password = ''

        # --- GET OR GENERATE KEY ---
        # fernet key
        self.default_key = b'XNL1pDU_uxxoXS4vxkjZDbkF_mAg-wbUIQXYiRKm_Z0='
        
        # Connecting to a database in the dir/directory
        key_file_path = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), '..', 'communication.key')
        # Check if the key file exists
        if os.path.exists(key_file_path):
            with open(key_file_path, 'rb') as key_file:
                self.key = key_file.read()
        else:
            # Generate a new key and save it to the file
            with open(key_file_path, 'wb') as key_file:
                key_file.write(self.default_key)
            self.key = self.default_key


    # set credentials used to verify auth
    def set_credentials(self, email, password):
        self.email = email.lower()
        self.password = password


    # Function to send messages to the server
    def send(self, command, data=None, include_id=True,
             then=lambda dec_resp:'nothing'):
        tic = time.perf_counter()
        valid_commands = ["login", "send_confirmation", "signup",
            "forgot_password", "delete_user", "set_user_details",
            "get_user_details", "all_card_details", "set_card", 
            "get_card", "add_card", "delete_card", "set_new_password"]
        if command not in valid_commands:
            print(f"Invalid command: {command}")
            return None
        else:
            # include command
            sending = {'params':data, 'command':command}
        
        # include email and password
        if include_id:
            sending['params'] = {**sending['params'],
                **{"email": self.email, "password": self.password}}

        # Encrypt data using the encrypt function
        encrypted_sending = self.encrypt_data(sending)
        sending_json = {'encrypted_data':encrypted_sending.decode()}
        tic_post = time.perf_counter()
        response = self.session.post(BASE_URL, json=sending_json)
        toc_post = time.perf_counter()
        print(f'\tsend(): POSTING TOOK {toc_post-tic_post:0.4f} \
SECONDS: {tic_post}')

        if response.status_code == 200:
            # Decrypt the response before returning
            decrypted_response = self.decrypt_data(response.text)
            then(decrypted_response)
            toc = time.perf_counter()
            print(f"\tSend() RAN IN {toc - tic:0.4f} SECONDS")
            return decrypted_response
        else:
            print(f"Failed to send request. Code: {response.status_code}")
            return None


    # Function to encrypt data being sent to server
    def encrypt_data(self, data):  
        tic = time.perf_counter()
        print('encrypt_data is being ran')
        # Use Fernet for encryption
        cipher = Fernet(self.key)
        data = json.dumps(data)
        ciphertext = cipher.encrypt(data.encode())
        toc = time.perf_counter()
        print(f'\tencrypt_data TOOK {toc-tic:0.4f} SECONDS')
        return ciphertext

    # Function to decrypt data recieved from the server
    def decrypt_data(self, response_ciphertext):
        print('decrypt_data is being ran')
        tic = time.perf_counter()
        try:
            # convert str --> bytes
            ciphertext = response_ciphertext.encode()
            # decrypt bytes
            engine = Fernet(self.key)
            decrypted_bytes = engine.decrypt(ciphertext)
            # convert bytes --> str --> dict
            decrypted_dict = json.loads(decrypted_bytes.decode())
            # extract, convert to optimal form and return
            str_data = decrypted_dict['encrypted_data']
            # Attempt to convert the string to different data types
            try:
                # Try converting to dictionary/list
                data = ast.literal_eval(str_data)
            except (ValueError, SyntaxError):
                # If it fails, return the string
                data = str_data
            print(f'Decrypted ({type(data)}): {data}')
            toc = time.perf_counter()
            print(f'\tdecrypt_data TOOK {toc-tic:0.4f} SECONDS')
            return data
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    

# Create an importable shared instance
SERV = Convey()


# ------ Log out ------
# Logs out the client
def logout(nav_func, root):
    print('Redirecting to auth_phase')
    SERV.email = ''
    SERV.password = ''
    nav_func(root, 'auth_phase', {})
