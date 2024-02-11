"""
Description:
    Login tab.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import components
from components import BetterEntry, Icon

# Import libraries
from serv import comm


def login_tab(root, tab, nav_func, all_data={}, NotificationCard=None):
    # Splash image
    splash, img = Icon.Widget(tab, image.login_splash, zoom=1)
    splash.image = img
    splash.place(anchor=CENTER, relx=0.5, rely=0.15)

    # tkinter stringvars
    entry_data = {}

    # email better entry
    unused, img1 = Icon.Widget(tab, image.icon_user, **style.be_48x48)
    
    # E.g., Johndoe@example.com
    email_widget, entry_data['email'] = BetterEntry.Widget(tab, img1,
        'Please enter your email', 'E.g., Johndoe@example.com', width=25) 

    # password better entry
    unused, img2 = Icon.Widget(tab, image.icon_password, **style.be_48x48)
    password_widget, entry_data['password'] = BetterEntry.Widget(tab, img2,
        'Please enter your password', 'E.g., password1234', show='*', width=25)
    # E.g., password1234

    # submit btn
    submit_btn = Button(tab, text='Submit', **style.btn,
        command=lambda:on_btn_press(root, nav_func,
            NotificationCard, entry_data
        )
    )

    # place everything
    email_widget.place(anchor=CENTER, relx=0.5, rely=0.4)
    password_widget.place(anchor=CENTER, relx=0.5, rely=0.65)

    submit_btn.place(anchor=CENTER, relx=0.5, rely=0.9)


# Login and show notification on btn press
def on_btn_press(root, nav_func, NotificationCard, entry_data):
    # Test login
    response = comm.SERV.send('login', data={
        'email':entry_data['email'].get().lower(), 
        'password':entry_data['password'].get()
    }, include_id=False)
    print(response)

    # if it failed
    if response[0] == False:
        NotificationCard.show_notification(
            text='Login failed. Please try again!', fg=-1
        )
        # reset password since they probably got that wrong
        entry_data['password'].set('')

    # if it worked
    if response[0] == True:
        # proceed to work phase and pass in all details
        comm.SERV.set_credentials(entry_data['email'].get().lower(),
                                  entry_data['password'].get())
        nav_func(root, 'work_phase', {
                'email': entry_data['email'].get().lower(), 
                'password': entry_data['password'].get()
            }
        )
        