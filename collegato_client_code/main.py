'''
PLEASE RUN THIS FILE TO RUN THE PROJECT.  ANY OTHER FILE WILL NOT RUN THE
PROJECT.

Names: Pranav Joshi and Yajat Mittal
CNLC Year: 2024
Project name: Collegato (Client)
Description:
    This project allows users to login, signup and regain access to their
    accounts in the 'auth_phase'.  After being authenticated, the user can
    create, edit, delete or open listings and open their settings.
Notes:
    - 1024x576 tabs (16:9 ratio)
    - Project was first coded in MacOS and transferred onto Windows. Therefore,
      some lines of code were written to counter-act the obscurities of either
      operating system.
    - This project works by dividing each page into a function that gets
      ran when the user is on the respective page.
Code-choices:
    This entire project uses a file structure similar to real-world projects
    in development teams.  Additionally, everything is coded in PEP-8 and has
    comments (when necessary) for improved code readability.
'''

# Import statements
from tkinter import *

# Import configs
from configs import config

# Import phases
from auth_phase.auth_phase import auth_phase
from work_phase.work_phase import work_phase


# Functions
# Navigate to another page
def navigate(container, target_page_str, all_details):
    # get background before deletion
    bg_colour = container.cget('bg')

    # Destroy current page
    for widget in container.winfo_children():
        widget.destroy()

    # restore background
    container.configure(bg=bg_colour)

    # Based on the page you want to go to, run the correct function
    if target_page_str == 'work_phase':
        work_phase(container, navigate, all_details)

    elif target_page_str == 'auth_phase':
        auth_phase(container, navigate, all_details)


# Main function
def main():
    # Create base window
    win = Tk()
    win.title(config.WINDOW_NAME)

    # display window
    auth_phase(win, navigate)

    # Main loop
    win.resizable(width=False, height=False)
    win.mainloop()


# Entry point of script
if __name__ == '__main__':
    main()
    