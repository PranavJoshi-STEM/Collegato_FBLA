# Import tkinter
from tkinter import *

# Import configs
from configs import style

# Import components
from components import PostCard


# Differentiate module ScrollList (this file) from class SL
class SL(Frame):
    # Create scroll list
    def __init__(self, parent, bg=style.bg):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, borderwidth=0, background=bg)
        self.frame = Frame(self.canvas, background=bg)
        self.vsb = Scrollbar(self, orient="vertical", 
                        command=self.canvas.yview, width=30)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4),
                                window=self.frame,
                                anchor="nw",
                                tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

    # Reset the scroll region to encompass the inner frame
    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # --- USEFUL FUNCTIONS ---
    # Add a list of widgets to the frame
    def populate(self, widgets, **kwargs):
        for widget in widgets:
            widget.grid(row=len(self.frame.grid_slaves()), column=0, **kwargs)


    # Clear all widgets
    def clear_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()


    # Load all Post Cards
    def load_cards(self, card_data_list, selectable=False, run_func=None):
        pady = 30
        widgets = []
        # add all the cards
        for i in range(len(card_data_list)):
            card_data = card_data_list[i]
            widgets.append(PostCard.Widget(
                self.frame,
                card_data['target'],
                card_data['title'],
                card_data['tags'],
                card_data['description'],
                selectable=selectable,
                run_func=run_func,
            ))
            c = (i % 4)  # column
            r = (i // 4)  # row

            #card.grid(pady=pady, row=r, column=c, sticky="nsew", padx=11)
            widgets[-1].grid(pady=pady, row=r, column=c, sticky="nsew", 
                            padx=11)
            #widgets.append(card)

        # Configure columns for centering
        for col in range(4):
            self.frame.columnconfigure(col, weight=1)
            self.frame.grid_columnconfigure(col, weight=1)
    

    def load_qna_cards(self, card_func, qna_list):
        widgets = []
        # create all widgets
        for i in range(len(qna_list)):
            widgets.append(card_func(self.frame, i, qna_list))
        # render all widgets
        self.populate(widgets, **{'padx':40, 'pady':20, 'sticky':'n'})
        # Configure columns for centering
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
