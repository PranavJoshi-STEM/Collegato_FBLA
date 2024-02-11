"""
Description:
    This file has quick configs that can be altered, so if this software is
    sold to another company for usage, they can quickly customize it to work
    with their current system (i.e., they could change the port).
"""

# ------ Configs ------
ENCRYPTION_KEY_NAME = 'db.key'
COMMUNICATION_KEY_NAME = 'communication.key'
DB_NAME = 'collegato_database.db'


# if true, app gets paths like it's an exe
# if false, app gets paths from the file
# make sure its correctly enabled or things wont work
COMPILING_TO_EXE = False

PORT = 5050
