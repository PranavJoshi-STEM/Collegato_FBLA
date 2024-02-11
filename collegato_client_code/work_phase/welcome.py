"""
Description:
    Welcome tab (for work phase).
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import components
from components import Icon


def welcome_tab(tab):
    # Create logo and title
    logo, img = Icon.Widget(tab, image.logo_thick, subsample=3)
    logo.image=img
    #title = Label(tab, text='ollegato!', bg=style.bg, font=style.title)

    # Subheaders
    text = Label(tab, fg=style.text, bg=style.highlight, font=style.h2,
                 text='Welcome back to Collegato!', )
    credits = Label(tab, fg=style.text, bg=style.bg, font=style.h2,
                    text='By Pranav Joshi and Yajat Mittal')

    # Place everything
    # logo and title
    logo.place(anchor=CENTER, relx=0.5, rely=0.3)
    #title.place(relx=0.4, rely=0.1)
    # subheaders
    text.place(anchor=CENTER, relx=0.5, rely=0.5)
    credits.place(anchor=CENTER, relx=0.5, rely=0.9)
    