"""
Description:
    Forgot password tab.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import components
from components import BetterEntry, Icon

# Import libraries
from libraries import verify
from serv import comm


# The tab
def forgot_password_tab(tab, all_data={}, NotificationCard=None):
    global entry_data, btn

    # Splash image
    splash, img = Icon.Widget(tab, image.forgot_password_splash, zoom=1)
    splash.image = img
    splash.place(anchor=CENTER, relx=0.5, rely=0.15)

    # tkinter stringvars
    entry_data = {}

    # The label
    info_label = Label(tab, bg=style.bg, text='\
Type in your email address.  We will email you \n\
a temporary password.  Change this password when\n\
you sign in and open settings.', fg=style.text, font=style.h2)

    # email better entry
    unused, correctImg = Icon.Widget(tab, image.icon_correct, **style.be_96x96)
    unused, wrongImg = Icon.Widget(tab, image.icon_wrong, **style.be_96x96,)
    email_widget, entry_data['email'] = BetterEntry.Widget(tab, '',
        'Please enter your email', 'E.g., Johndoe@example.com', width=25,
        always_show_icon=False, icon_activation=verify.valid_email,
        bind=btn_status,
        trueImg=correctImg, falseImg=wrongImg,
    )

    # Send email button
    btn = Button(tab, **style.btn, text='Send email',
                 command=lambda: check_and_send(NotificationCard))
    btn.configure(state='disabled')

    # place everything
    info_label.place(anchor=CENTER, relx=0.5, rely=0.4)
    email_widget.place(anchor=CENTER, relx=0.5, rely=0.7)
    btn.place(anchor=CENTER, relx=0.5, rely=0.9)


# If the email is invalid, disable the button
def btn_status(is_valid):
    global btn
    try:
        if is_valid:
            btn.configure(state='normal')
        else:
            btn.configure(state='disabled')
    except:
        # do nothing
        pass


# If the field is valid, send email!
def check_and_send(NotificationCard):
    global entry_data

    # send email
    print(f"Submitted: {entry_data['email'].get()}")
    comm.SERV.set_credentials(entry_data['email'].get(), '')
    comm.SERV.send('forgot_password', data={'email': comm.SERV.email})

    # notify the user that the image has been sent
    NotificationCard.show_notification(text='An email has been sent!\n \
Please check your inbox/spam.', fg=1, duration='auto')
