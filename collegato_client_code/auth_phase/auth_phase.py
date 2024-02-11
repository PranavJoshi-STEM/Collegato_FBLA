"""
Description:
    This file loads in each tab and allows the user to navigate between each
    auth related tab.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style

# Import tabs
from .welcome import welcome_tab
from .login import login_tab
from .signup import Signup
from .forgot_password import forgot_password_tab

# Import components
from components.NotificationCard import NC


# auth_phase
def auth_phase(root, nav_func, all_data={}):
    # Create notebook
    notebook = ttk.Notebook(root, height=config.TAB_HEIGHT,
                            width=config.TAB_WIDTH)
    notebook.pack(fill='both', expand=True)

    # Create frames for each tab
    create_frame = lambda: Frame(notebook, bg=style.bg,
                                 height=config.TAB_HEIGHT, 
                                 width=config.TAB_WIDTH
                                )
    welcome = create_frame()
    login = create_frame()
    signup = create_frame()
    forgot_password = create_frame()

    # Create notification card
    notif = NC(root)

    # Load tabs
    welcome_tab(welcome)
    login_tab(root, login, nav_func, all_data=all_data,
              NotificationCard=notif)

    # Signup tab (since it has 2 pages)
    signup_instance = Signup(root, signup, notebook, all_data=all_data,
                             nav_func=nav_func)
    signup_instance.signup_tab(NotificationCard=notif)
    forgot_password_tab(forgot_password, all_data=all_data,
                        NotificationCard=notif)

    # Pack frames to fill available space
    welcome.pack(fill='both', expand=True)
    login.pack(fill='both', expand=True)
    signup.pack(fill='both', expand=True)
    forgot_password.pack(fill='both', expand=True)

    # Add frames to the notebook with left-aligned tabs
    notebook.add(welcome, text='Welcome!')
    notebook.add(login, text='Login')
    notebook.add(signup, text='Sign-up')
    notebook.add(forgot_password, text='Forgot Password')