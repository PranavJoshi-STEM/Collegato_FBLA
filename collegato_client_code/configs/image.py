"""
Description:
    The images and icons used in the project.
"""

import os

# --- RELATIVE IMPORT ---
# Get the absolute path of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Create a function to reduce code
path = lambda tup, filename: os.path.join(*tup, filename)

# Store path components in a tuple
logo = (current_script_dir, '..', 'assets', 'logo')
title = (current_script_dir, '..', 'assets', 'titles')
icon = (current_script_dir, '..', 'assets', 'icons')


# --- IMAGES ---
# Logos
logo192 = path(logo, 'logo192.png')
logo512 = path(logo, 'logo512.png')
logo_high_res = path(logo, 'logo_high_res.png')
logo_thick = path(logo, 'logo_thick.png')


# Titles
login_splash = path(title, 'login.png')
signup_1_splash = path(title, 'signup_1.png')
signup_2_splash = path(title, 'signup_2.png')
forgot_password_splash = path(title, 'forgot_password.png')

settings_splash = path(title, 'settings.png')
welcome_splash = path(title, 'welcome.png')
filter_splash = path(title, 'filter.png')
edit_post_splash = path(title, 'edit_post.png')
account_splash = path(title, 'account.png')
reports_splash = path(title, 'reports.png')


# BetterEntry icons
icon_user = path(icon, 'user.png')
icon_password = path(icon, 'password.png')
icon_correct = path(icon, 'correct_96x96.png')
icon_wrong = path(icon, 'wrong_96x96.png')
