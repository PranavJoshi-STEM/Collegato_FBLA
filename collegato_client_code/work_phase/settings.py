"""
Description:
    Settings tab (for work phase).
    Here, the user can configure their settings.
"""

# Import tkinter
from tkinter import *

# Import libraries
from serv import comm
from libraries import verify

# Import configs
from configs import image, style

# Import components
from components import Icon, BetterEntry


def settings_tab(tab, NotificationCard, showNotif=False, all_data={}, 
                 nav_func=None, root=None):
    # Splash image
    splash, img = Icon.Widget(tab, image.settings_splash, zoom=1)
    splash.image = img
    splash.place(anchor=CENTER, relx=0.5, rely=0.15)

    # tkinter stringvars
    known_data = {
        'first_name': '',
        'last_name': '',
        'new_password': '',
        'confirm_password': '',
        'email': '',
    }
    entry_data = {}


    # --- rows ---
    row1 = Frame(tab, bg=style.bg)
    row2 = Frame(tab, bg=style.bg)
    # Icons
    unused, correctImg = Icon.Widget(tab, image.icon_correct,
                                        **style.be_96x96)
    unused, wrongImg = Icon.Widget(tab, image.icon_wrong,
                                    **style.be_96x96,)
    unused, passwordImg = Icon.Widget(tab, image.icon_password,
                                    **style.be_48x48,)
    unused, userImg = Icon.Widget(tab, image.icon_user,
                                    **style.be_48x48,)
    

    # --- row1 widgets ---
    # email
    email_widget, entry_data['email'], email_entry = BetterEntry.Widget(row1, 
    userImg,'NOTE: Cannot change email!', known_data['email'], width=23,
        returnEntry=True,
    )
    email_entry.config(state='readonly')
    # first name
    first_name_widget, entry_data['first_name'], first_name_entry = \
    BetterEntry.Widget(
        row1, '', 'First name', known_data['first_name'], width=8,
        always_show_icon=False, icon_activation=verify.valid_name,
        trueImg=correctImg, falseImg=wrongImg, returnEntry=True,
    )
    # last name
    last_name_widget, entry_data['last_name'], last_name_entry = \
        BetterEntry.Widget(
        row1, '', 'Last name', known_data['last_name'], width=8,
        always_show_icon=False, icon_activation=verify.valid_name,
        trueImg=correctImg, falseImg=wrongImg, returnEntry=True,
    )
    # placement
    email_widget.grid(row=0, column=0, columnspan=2, pady=10)
    first_name_widget.grid(row=1, column=0, sticky=NSEW, pady=10)
    last_name_widget.grid(row=1, column=1, sticky=NSEW, pady=10)


    # --- row2 widgets ---
    # label
    description = Label(row2, text='Password requirements: \
≥1 num, ≥2 special chars, ≥8 in length', fg=style.text, bg=style.highlight)
    # old password
    old_password_widget, entry_data['old_password'] = BetterEntry.Widget(row2,
        passwordImg, 'Enter your existing password', '', width=25, show='*')
    # old password
    new_password_widget, entry_data['new_password'] = BetterEntry.Widget(row2,
        '', 'Enter your new password', '',
        icon_activation=verify.valid_password,
        bind=lambda unused:same_password(entry_data),
        always_show_icon=False, trueImg=correctImg, falseImg=wrongImg,
        width=25, show='*')
    # confirm
    confirm_password_widget, entry_data['confirm_password'] = \
    BetterEntry.Widget(row2, 
        '', 'Please retype your password', '', width=25, show='*',
        icon_activation=lambda unused:same_password(entry_data),
        always_show_icon=False, trueImg=correctImg, falseImg=wrongImg)
    # Place everything
    description.grid(row=0, sticky=NSEW, pady=5)
    old_password_widget.grid(row=1, sticky=NSEW, pady=5)
    new_password_widget.grid(row=2, sticky=NSEW, pady=5)
    confirm_password_widget.grid(row=3, sticky=NSEW, pady=5)


    # --- Place rows, buttons and labels ---
    row1.place(anchor=N, relx=0.3, rely=0.3, relwidth=0.5, relheight=0.7)
    row2.place(anchor=N, relx=0.75, rely=0.27, relwidth=0.5, relheight=0.7)
    save_btn = Button(tab, text='Save', **style.btn,
                      command=lambda:check_status(tab, NotificationCard, 
                                                  entry_data, nav_func, root))
    label = Label(tab, text='In the event of a password change, you\nwill \
also be automatically logged out!',
                  fg=style.text, bg=style.highlight, font=style.tiny)
    save_btn.place(anchor=CENTER, relx=0.5, rely=0.9)
    label.place(anchor=CENTER, relx=0.75, rely=0.9)


    # -- Show notif that data has been saved if it has been saved --
    if showNotif==1:
        NotificationCard.show_notification(
            text='Data has been saved!', fg=1
        )
    elif showNotif==-1:
        NotificationCard.show_notification(
            text='Password was incorrect.', fg=-1
        )


    # --- Update all fields
    def set_field(d):
        print(d)
        entry_data['first_name'].set(d['firstname'])
        entry_data['last_name'].set(d['lastname'])
        first_name_widget.update()
        last_name_widget.update()
    comm.SERV.send('get_user_details', data={'key':'both'},
                   then=lambda dec_resp:set_field(dec_resp))
    email_entry.config(state='normal')
    entry_data['email'].set(comm.SERV.email)
    email_widget.update()
    email_entry.config(state='readonly')


# First page functions
def check_status(tab, NotificationCard, entry_data, nav_func, root):
    # make sure that all fields are filled (names)
    if (
        (entry_data['first_name'].get() != '' or \
            entry_data['last_name'].get() != '')
        and (
            entry_data['first_name'].get() == ''
            or entry_data['last_name'].get() == ''
        )
    ):
        NotificationCard.show_notification(
            text='You cannot leave any\n fields blank when changing name!', 
            fg=-1
        )
        return 0  # stop running the function
    # changing passwords
    changing_passwords = not all(entry_data[i].get() == '' for i in [
                    'old_password', 'new_password', 'confirm_password'])
    if changing_passwords:
        if any(entry_data[i].get() == '' for i in ['old_password', 
                                        'new_password', 'confirm_password']):
            for elem in ['old_password', 'new_password', 'confirm_password']:
                if entry_data[elem].get() == '':
                    NotificationCard.show_notification(
                        text='You cannot leave any fields \nblank when \
                            changing passwords!', fg=-1
                    )
                    return 0  # stop running the function

    # notifications that will be displayed if something failed
    name_msgs = [
        'Name can only have \ncharacters A-Z',
        'Name can only have \ncharacters A-Z',
    ]
    pass_msgs = [
        'Base password does \nnot fulfill requirements.',
        'Passwords do not match',
    ]
    # the validity of each field
    name_statuses = [
        verify.valid_name(entry_data['first_name'].get()),
        verify.valid_name(entry_data['last_name'].get()),
    ]
    pass_statuses = [
        verify.valid_password(entry_data['new_password'].get()),
        same_password(entry_data),
    ]

    # check if anything failed
    if False in name_statuses:
        # give helpful feedback depending on the error
        for i, status in enumerate(name_statuses):
            if status == False:
                NotificationCard.show_notification(
                    text=name_msgs[i], fg=-1
                )
                return 0  # stop running the function


    # check if anything failed
    if changing_passwords:
        if False in pass_statuses:
            # give helpful feedback depending on the error
            for i, status in enumerate(pass_statuses):
                if status == False:
                    NotificationCard.show_notification(
                        text=pass_msgs[i], fg=-1
                    )
                    return 0  # stop running the function
            
    # everything needs to be saved
    def save(nav_func, root):
        # set names
        comm.SERV.send('set_user_details', data={
            'key': 'both',
            'new_data': {
                'firstname':entry_data['first_name'].get().title(),
                'lastname':entry_data['last_name'].get().title()
            }
        })
        # not changing passwords
        if not changing_passwords:
            return 1

        # change password
        elif changing_passwords:
            # request the password to be saved
            status = comm.SERV.send("set_new_password", data={
                'email': comm.SERV.email,
                'old_password': entry_data['old_password'].get(),
                'new_password': entry_data['new_password'].get()
            }, include_id=False)
            # if the new password is saved, set new password and details
            if status:
                comm.SERV.set_credentials(
                    comm.SERV.email, entry_data['new_password'].get())
                comm.logout(nav_func, root)
                return 1
            else:
                return -1

    notifType = save(nav_func, root)

    # reload tab
    settings_tab(tab, NotificationCard, showNotif=notifType)


# to verify if the passwords are the same
def same_password(entry_data):
    try:
        # update confirm password widget's status
        entry_data['confirm_password'].set(
            entry_data['confirm_password'].get())
        # check 2 conditions
        condition1 = verify.valid_password(
            entry_data['new_password'].get())
        condition2 = (
            entry_data['confirm_password'].get()==entry_data[
                      'new_password'].get())
        # return True if both conditions are true
        return True==condition1 and True==condition2
    except:
        pass # Do nothing because the entry_data keys havent been created yet