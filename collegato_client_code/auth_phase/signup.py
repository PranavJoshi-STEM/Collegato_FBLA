"""
Description:
    First signup tab.
Note:
    Once the account is made, it will redirect to the login page.
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

class Signup():
    def __init__(self, root, tab, notebook, all_data={},
                 nav_func=lambda:print('Nothing')):
        self.tab = tab
        self.all_data = all_data
        self.notebook = notebook
        # phase==0 ==> signup_1()
        # phase==1 ==> signup_2()
        self.nav_func = nav_func
        self.root = root

    # switches the phase to the target
    def phase_switch(self, NotificationCard, entry_data, target_phase=0):
        for widget in self.tab.winfo_children():
            widget.destroy()

        # change phase and run page
        subpage = [self.signup_1, self.signup_2][target_phase]
        subpage(NotificationCard)


    # function rendered in auth_phase, deals with things automatically
    def signup_tab(self, NotificationCard=None):
        self.signup_1(NotificationCard)


    # first page
    def signup_1(self, NotificationCard):
        # Splash image
        splash, img = Icon.Widget(self.tab, image.signup_1_splash, zoom=1)
        splash.image = img
        splash.place(anchor=CENTER, relx=0.5, rely=0.15)

        # tkinter stringvars
        self.entry_data = {}

        # main rows
        row1 = Frame(self.tab) # email, first name, last name
        row2 = Frame(self.tab) # password, confirm password

        # Icons
        unused, correctImg = Icon.Widget(self.tab, image.icon_correct,
                                         **style.be_96x96)
        unused, wrongImg = Icon.Widget(self.tab, image.icon_wrong,
                                       **style.be_96x96,)

        # -- row1 widgets --
        # email
        email_widget, self.entry_data['email'] = BetterEntry.Widget(row1, '',
            'Please enter your email', 'E.g., Johndoe@example.com', width=23,
            always_show_icon=False, icon_activation=verify.valid_email,
            trueImg=correctImg, falseImg=wrongImg,
        )
        # first name
        first_name_widget, self.entry_data['first name'] = BetterEntry.Widget(
            row1, '', 'First name', '', width=8,
            always_show_icon=False, icon_activation=verify.valid_name,
            trueImg=correctImg, falseImg=wrongImg,
        )
        # last name
        last_name_widget, self.entry_data['last name'] = BetterEntry.Widget(
            row1, '', 'Last name', '', width=8,
            always_show_icon=False, icon_activation=verify.valid_name,
            trueImg=correctImg, falseImg=wrongImg,
        )

        # -- row1 placement --
        email_widget.grid(row=0, column=0, columnspan=2)
        first_name_widget.grid(row=1, column=0, sticky=NSEW)
        last_name_widget.grid(row=1, column=1, sticky=NSEW)
        
        # -- row2 widgets --
        # label
        description = Label(row2, text='Password requirements: \
≥1 num, ≥2 special chars, ≥8 in length', fg=style.text, bg=style.highlight)
        # password
        password_widget, self.entry_data['password'] = BetterEntry.Widget(row2,
            '', 'Please create your password', '',
            icon_activation=verify.valid_password,
            bind=lambda unused:same_password(self.entry_data),
            always_show_icon=False, trueImg=correctImg, falseImg=wrongImg,
            width=25, show='*')
        # confirm
        confirm_password_widget, self.entry_data['confirm password'] = \
        BetterEntry.Widget(row2, 
            '', 'Please retype your password', '', width=25, show='*',
            icon_activation=lambda unused: same_password(self.entry_data),
            always_show_icon=False, trueImg=correctImg, falseImg=wrongImg,)
        
        # -- row2 placement --
        description.grid(row=0, sticky=NSEW)
        password_widget.grid(row=1, sticky=NSEW)
        confirm_password_widget.grid(row=2, sticky=NSEW)
        
        # Buttons
        btn_frame = Frame(self.tab)
        btn_lambda = lambda: self.check_status(NotificationCard)
        btn = Button(btn_frame, text='Next  →',
            command=btn_lambda, **style.btn)
        btn.pack()

        # Place everything
        divider = Label(self.tab, text=('|\n'*20), fg=style.text, bg=style.bg)

        row1.place(relx=0.05, rely=0.3)
        row2.place(relx=0.55, rely=0.3)
        divider.place(anchor=CENTER, relx=0.5, rely=0.5)

        btn_frame.place(anchor=CENTER, relx=0.5, rely=0.9)


    # First page functions
    def check_status(self, NotificationCard):
        # make sure that all fields are filled
        for elem in list(self.entry_data.keys()):
            if self.entry_data[elem].get()=='':
                NotificationCard.show_notification(
                    text='You cannot leave any\n fields blank!', fg=-1
                )
                return 0 # stop running the function
        # notifications that will be displayed if something failed
        messages = [
            'Please enter a valid email',
            'Name can only have characters A-Z',
            'Name can only have characters A-Z',
            'Base password does \nnot fulfill requirements.',
            'Passwords do not match',
        ]
        # the validity of each field
        statuses = [
            verify.valid_email(self.entry_data['email'].get()),
            verify.valid_name(self.entry_data['first name'].get()),
            verify.valid_name(self.entry_data['last name'].get()),
            verify.valid_password(self.entry_data['password'].get()),
            same_password(self.entry_data),
        ]

        # check if anything failed
        if False in statuses:
            # give helpful feedback depending on the error
            for i, status in enumerate(statuses):
                if status==False:
                    NotificationCard.show_notification(
                        text=messages[i], fg=-1
                    )
                    return 0 # stop running the function
            
        # everything is valid 
        else:
            status = comm.SERV.send('send_confirmation',
                           data={
                            'email':self.entry_data['email'].get().lower()},
                           include_id=False)
            if status==True:
                self.phase_switch(NotificationCard, self.entry_data,
                                target_phase=1)
            else:
                NotificationCard.show_notification(text='Operation failed, \
could not\nsend email', fg=-1)


    # second page
    def signup_2(self, NotificationCard):
        global submit_btn

        # Splash image
        splash, img = Icon.Widget(self.tab, image.signup_2_splash, zoom=1)
        splash.image = img
        splash.place(anchor=CENTER, relx=0.5, rely=0.15)

        # The label
        info_label = Label(self.tab, bg=style.bg, text="\
We've sent a 6-digit code to the provided \n\
email address.  Please type this 6-digit code\n\
to verify your email.  Check your inbox/spam.", fg=style.text, font=style.h2)

        # icons
        unused, correctImg = Icon.Widget(self.tab, image.icon_correct,
                                         **style.be_96x96)
        unused, wrongImg = Icon.Widget(self.tab, image.icon_wrong,
                                       **style.be_96x96,)

        # better entry
        code_widget, self.entry_data['code'] = BetterEntry.Widget(self.tab, '',
            'Please type in this code:', '', width=25,
            always_show_icon=False, icon_activation=lambda s: verify.is_int(
                s, check_len=True, target_len=6
            ), trueImg=correctImg, falseImg=wrongImg, bind=self.btn_status,
        )

        # Buttons
        back_btn = Button(self.tab, **style.btn, text='←  Go back',
                          command=lambda: self.phase_switch(
                            NotificationCard, self.entry_data, target_phase=0
                          )
                         )
        submit_btn = Button(self.tab, **style.btn, text='Submit',
                            command=lambda: self.submit(NotificationCard)
                           )
        submit_btn.configure(state='disabled')

        # place everything
        info_label.place(anchor=CENTER, relx=0.5, rely=0.4)
        code_widget.place(anchor=CENTER, relx=0.5, rely=0.7)
        back_btn.place(anchor=CENTER, relx=0.3, rely=0.9)
        submit_btn.place(anchor=CENTER, relx=0.7, rely=0.9)


    # second page functions
    # If the email is invalid, disable the button
    def btn_status(self, is_valid):
        global submit_btn
        try:
            if is_valid:
                submit_btn.configure(state='normal')
            else:
                submit_btn.configure(state='disabled')
        except:
            # do nothing
            pass


    # If the field is valid, send email!
    def submit(self, NotificationCard):
        # send email
        print(f"Submitted: {self.entry_data['code'].get()}")
        # define vars
        def get(key:str) -> str:
            return self.entry_data[key].get()
        is_correct_code = comm.SERV.send('signup', data={
                'email': get('email').lower(),
                'password': get('password'),
                'firstname': get('first name').title(), 
                'lastname': get('last name').title(), 
                'code': get('code'),
            }, include_id=False,                         
        )
        if is_correct_code:
            comm.SERV.set_credentials(get('email').lower(), get('password'))
            NotificationCard.show_notification(text='Logged in,\n \
welcome to Collegato!', fg=1, duration='auto')
            self.nav_func(self.root, 'work_phase', {})
        else:
            # notify the user that the code is incorrect
            NotificationCard.show_notification(text='Code is incorrect.\n \
Please try again.', fg=-1, duration='auto')


# --- icon_activation functions ---
# for the confirm_password_widget
def same_password(entry_data):
    try:
        # update confirm password widget's status
        entry_data['confirm password'].set(
            entry_data['confirm password'].get())
        # check 2 conditions
        condition1 = verify.valid_password(
            entry_data['password'].get())
        condition2 = (
            entry_data['confirm password'].get()==entry_data['password'].get())
        # return True if both conditions are true
        return True==condition1 and True==condition2
    except:
        pass # Do nothing because the entry_data keys havent been created yet
