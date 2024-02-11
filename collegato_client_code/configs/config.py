"""
Description:
    Configs used in the project.
"""

# Root window
TAB_WIDTH = 1024
TAB_HEIGHT = 576
VERSION = '2.0.0'
WINDOW_NAME = f'Collegato Client {VERSION}'

# Filter window
FILTER_WIN_NAME = f'{WINDOW_NAME}: Filter'
FILTER_WIDTH = 512
FILTER_HEIGHT = 576

# Edit window
EDIT_WIN_TEMPLATE = f'{WINDOW_NAME}: Edit/Open'
EDIT_WIN_NAME = lambda target: f'{EDIT_WIN_TEMPLATE} ({target})'
EDIT_WIDTH = FILTER_WIDTH
EDIT_HEIGHT = FILTER_HEIGHT

# Client to server connection
PORT = 5050
BASE_URL = f'http://localhost:{PORT}/execute_command'
