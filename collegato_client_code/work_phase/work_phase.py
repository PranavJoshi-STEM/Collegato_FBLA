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

# Import components
from components.NotificationCard import NC

# Import tabs
from .welcome import welcome_tab
from .view_list import view_list_tab
from .edit_actions import edit_actions_tab
from .settings import settings_tab
from .account import account_tab
from .help_menu import help_menu_tab
from .reports import reports_tab


def work_phase(root, nav_func, all_data={'email':'', 'password':''}):
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
    view_list = create_frame()
    edit_actions = create_frame()
    settings = create_frame()
    account = create_frame()
    help_menu = create_frame()
    reports = create_frame()

    # Create notification card
    notif = NC(root)

    # Load tabs
    welcome_tab(welcome)
    view_list_tab(view_list, notif, all_data=all_data)
    edit_actions_tab(edit_actions, notif, all_data=all_data)
    settings_tab(settings, notif, all_data=all_data, nav_func=nav_func, 
                 root=root)
    account_tab(account, notif, root, nav_func, all_data=all_data)
    help_menu_tab(help_menu, notif)
    reports_tab(reports, notif)

    # Pack frames to fill available space
    welcome.pack(fill='both', expand=True)
    view_list.pack(fill='both', expand=True)
    edit_actions.pack(fill='both', expand=True)
    settings.pack(fill='both', expand=True)
    account.pack(fill='both', expand=True)
    help_menu.pack(fill='both', expand=True)
    reports.pack(fill='both', expand=True)

    # Add frames to the notebook with left-aligned tabs
    notebook.add(welcome, text='Welcome!')
    notebook.add(view_list, text='👀 View List')
    notebook.add(edit_actions, text='✏ Edit Actions')
    notebook.add(settings, text='Settings')
    notebook.add(account, text='Account')
    notebook.add(help_menu, text='Help Menu')
    notebook.add(reports, text='Reports')
    