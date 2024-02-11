"""
Description:
    Here, the user can create reports (summary of all their cards) incase
    they want to copy, paste and share the data.
"""

# Import statements
from tkinter import ttk
from tkinter import *
from datetime import datetime

# Import configs
from configs import config, style, image

# Import libraries
from serv import comm

# Import components
from components import Icon


def reports_tab(tab, NotificationCard):
    # function to update the text widget
    def update_text():
        # Generate text, big dict of all cards
        result = comm.SERV.send('all_card_details', data={}) 
            # standard header
        report = ' '*33 + 'BASIC DETAILS:' + ' '*33
        report += f'\nEMAIL: {comm.SERV.email}'
        report += f'\nGENERATED: {datetime.now().strftime("%d %B %Y, %I:%M%p")}'
        report += '\n' + '-'*72
            # all cards
        for target in result.keys():
            details = {'target':target}
            for key in result[target].keys():
                details[key] = result[target][key]

            report += f'\n\nTITLE: {result[target]["title"]}'
            report += f'\n\tDESCRIPTION: {result[target]["description"]}'
            if len(result[target]["tags"]) > 1:
                tags = ", ".join(result[target]["tags"])
            else:
                tags = "None"
            report += f'\n\tTAGS: {tags}'
            if checkbox_var.get():
                report += f'\n\tTARGET: {target}\n'
            report += '\n\n\n' + ' '*26 + '---------------' + ' '*26
            # end
        report +=   '\n\n' + '-'*26 + ' END OF REPORT ' + '-'*26

        # Show report
        NotificationCard.show_notification(fg=1,
                                           text='Generated report!')
        text_widget.config(state='normal')
        text_widget.delete('1.0', END)
        text_widget.insert(END, report)
        text_widget.config(state='disabled')


    # Splash image
    splash, img = Icon.Widget(tab, image.reports_splash, zoom=1)
    splash.image = img
    splash.place(anchor=CENTER, relx=0.5, rely=0.15)

    # Description
    label = Label(tab, fg=style.text, bg=style.highlight, font=style.h2,
        text='Generate a report of all your posts by clicking on the button!')
    label.place(anchor=N, relx=0.5, rely=0.24)

    # Checkbox
    checkbox_var = BooleanVar()
    checkbox = Checkbutton(tab, text='Include Target?', variable=checkbox_var,
                           fg=style.highlight, bg=style.text, font=style.tiny)
    checkbox.place(anchor=CENTER, relx=0.9, rely=0.5)

    # Readonly text widget
    text_widget = Text(tab, wrap='word', height=10, width=50,
                       state='disabled', font=style.p)
    text_widget.place(anchor=N, relx=0.5, rely=0.38)

    # Button to update text
    update_button = Button(tab, text='Generate Report',
                           command=update_text, **style.btn)
    update_button.place(anchor=CENTER, relx=0.5, rely=0.95)
    