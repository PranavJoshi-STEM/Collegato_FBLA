"""
Descriptions:
    This entry has a title, entry and icon that can be configured to only show
    on certain conditions.
"""

# Import tkinter
from tkinter import *

# Import style
from configs import style


# do nothing if the always_show_icon is on.
def do_nothing(input):
    return input


def Widget(root, img, text, entry_placeholder, always_show_icon=True, 
           icon_activation=do_nothing, bind=do_nothing, show=None, 
           returnEntry=False, width=None, height=None, justify='left', 
           falseImg='', trueImg=''):
    frame = Frame(root, bg=style.bg, width=width, height=height)

    # Icon
    icon_label = Label(frame, image=img, bg=style.bg)
    # icon_label.place(relx=0, rely=0, relheight=0.5)
    icon_label.grid(column=0, row=1)

    # Text Label
    text_label = Label(frame, text=text, font=style.h2, bg=style.bg,
                       fg=style.text, width=width, justify=justify)
    # text_label.place(relx=0, rely=0.5, relwidth=0.1)
    text_label.grid(column=0, row=0, columnspan=10)

    # Entry
    entry_var = StringVar()
    entry = Entry(frame, textvariable=entry_var, font=style.p, justify='left',
                  bg=style.entry_bg, fg=style.entry_text, show=show,
                  width=width)
    # entry.place(relx=0.15, rely=0.5, relwidth=0.85, relheight=0.5)
    entry.grid(column=1, row=1, columnspan=9)
    entry.insert(0, entry_placeholder)

    # Function to update the icon based on activation condition
    def update_icon():
        if always_show_icon:
            icon_label.config(image=img)
        else:
            if icon_activation(entry_var.get()):
                icon_label.config(image=trueImg)
                bind(True)
            else:
                icon_label.config(image=falseImg)
                bind(False)

    # Bind the entry change to update the icon
    entry_var.trace_add('write', lambda name, index, mode: update_icon())

    # Initial update of the icon
    update_icon()

    if returnEntry:
        return frame, entry_var, entry
    else:
        return frame, entry_var
        