"""
Description:
    Account tab (for work phase).
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import random for the 12 digit num
import random

# Import configs
from configs import image, style

# Import components
from components import Icon

# Import libraries
from serv import comm

# generate random number
gen_random = lambda:random.randint(10**11, 10**12 - 1)


# Function that runs on button press
def delete_account(entry_data, num, NotificationCard, nav_func, root):
    # all notification types
    msg = []
    # have a var so this can run after the notification
    del_account = False
    # wrap this all in a true-except
    # because either the values havent been defined yet
    # or because the value entered isn't a number
    try:
        entered = int(entry_data['num_entry'].get())
        # number isnt the same
        if entered != int(num.get()):
            num.set(str(gen_random()))
            msg = ["Number entered doesn't match.", -1]
        else:
            msg = ['Deleted account and all data!', 1]
            del_account = True
    except:
        msg = ['Please enter a valid number.', -1]
    # show msg
    if msg!=[]:
        NotificationCard.show_notification(text=msg[0], fg=msg[1])
    # delete account
    if del_account:
        comm.SERV.send('delete_user', data={'email': comm.SERV.email,
                                            'password': comm.SERV.password},
                                            include_id=False)
        comm.SERV.set_credentials('', '')
        comm.logout(nav_func, root)


# GUI for the account tab
def account_tab(tab, NotificationCard, root, nav_func, all_data={}):
    global entry_data
    # Splash image
    splash, img = Icon.Widget(tab, image.account_splash, zoom=1)
    splash.image = img
    splash.place(anchor=CENTER, relx=0.5, rely=0.15)

    # tkinter stringvars
    entry_data = {
        'num_entry': StringVar(value=''),
    }
    num = StringVar(value=str(gen_random()))

    # top section
    reminder = Label(tab, font=style.p, fg=style.text, bg=style.highlight,
                text='Are you done using Collegato for today? Make sure'+\
'\nto log out, to keep your data secure!')
    logout_btn = Button(tab, text='Log out!', **style.btn,
                        command=lambda: comm.logout(nav_func, root))
        # place
    reminder.place(anchor=CENTER, relx=0.5, rely=0.32)
    logout_btn.place(anchor=CENTER, relx=0.5, rely=0.45)
    # divider
    divider = Label(tab, text='-'*20, font=style.h1, fg=style._BLACK,
                    bg=style.bg)
    divider.place(anchor=CENTER, relx=0.5, rely=0.55)
    # lower section
    warning = Label(tab, font=style.p, fg=style.text, bg=style.highlight,
                text='If you delete your account, you will be logged out and \
all'
                + '\nyour data will be deleted. To confirm deletion, retype' \
                + '\nthe following 12-digit number into the box below:',
                justify='left')
    confirm_int = Label(tab, textvariable=num, font=style.p, bg=style.RED,
                        fg=style.text)
    num_entry = Entry(tab, font=style.p, textvariable=entry_data['num_entry'])
    delete_btn = Button(tab, text='Delete account (NO GOING BACK!)',
                        fg=style.text, bg=style.RED, width=30, height=2,
                        command=lambda: delete_account(entry_data, num, 
                                            NotificationCard, nav_func, root))
        # place
    warning.place(anchor=CENTER, relx=0.5, rely=0.7)
    confirm_int.place(anchor=W, relx=0.25, rely=0.83)
    num_entry.place(anchor=E, relx=0.75, rely=0.83)
    delete_btn.place(anchor=CENTER, relx=0.5, rely=0.95)
