"""
Description:
    A notification card that pops-up when called.
"""

# Import statements
import tkinter as tk

# Import configs
from configs import style

# --- Defaults ---
# normal (0) ==> 'black'
# error (-1) ==> 'red'
# success (1) ==> 'green'
default_colours = ['black', 'green', 'red']
default_fg = default_colours[0]
default_bg = 'lightblue'
# when duratio=='auto', this is multiplied by len of text
duration_multiplier = 50


class NC(tk.Frame):
    def __init__(self, master=None, **kwargs):
        # Settings
        self.display_duration = 2*1000 # milliseconds
        # System
        super().__init__(master, **kwargs)
        self.label = tk.Label(self, text='', fg=default_fg, 
                              font=style.ultra_tiny, bg=default_bg, width=35, 
                              height=4) # original width was 27
        self.label.pack(expand=True, fill='both')

    def show_notification(self, text='', duration=None, fg=default_fg,
                          bg=default_bg, width=35, height=4):
        # you can also use numbers for fg
        if type(fg) == int:
            fg = default_colours[fg]

        # determine the duration
        if duration is None:
            duration = self.display_duration
        if duration == 'auto':
            duration = duration_multiplier*len(text)
        # Ensure starting off-screen
        self.place(x=self.master.winfo_width(), y=0)
        self.label.config(text=text, fg=fg, bg=bg, width=width, height=height)
        self.after(10, self.slide_in)
        self.after(duration, self.slide_out)

    def slide_in(self):
        x = self.winfo_x()
        if x > self.master.winfo_width() - 280:
            self.place(x=x - 10, y=0)
            self.after(10, self.slide_in)

    def slide_out(self):
        x = self.winfo_x()
        if x < self.master.winfo_width():
            self.place(x=x + 10, y=0)
            self.after(10, self.slide_out)
        else:
            self.place_forget()
            