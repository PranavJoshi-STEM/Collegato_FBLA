"""
Description:
    A small card that has all the details of a post.
"""

# Import statements
from tkinter import *
from random import *

# Import libraries
from configs.style import *

# Import pages
from windows.edit_post_win import PostEditor

# Max len defaults
#max_title_len = 15 # if font was p
max_title_len = 20
max_description_len = 60
end = '...'


checkbox_var = {}
checkbox = {}
PE = {}


# Scrolling label tag
class ShufflingLabel(Label):
    def __init__(self, master, tags, max_length=10, shuffle_speed=500):
        Label.__init__(self, master, bg=highlight, fg=card_text, text="", 
                       font=tiny, pady=3)
        self.tags = tags
        self.max_length = max_length
        self.shuffle_speed = shuffle_speed
        self.current_tag_index = 0
        self.shuffle()

    def shuffle(self):
        if len(self.tags) != 0:
            tag = self.tags[self.current_tag_index]
            tag_length = min(len(tag), self.max_length)

            if tag_length < self.max_length:
                shuffled_tag = tag[-tag_length:] + " " * \
                               (self.max_length - tag_length)
            else:
                shuffled_tag = ''.join(random.sample(tag, tag_length))

            self.config(text=shuffled_tag)
            self.current_tag_index = (self.current_tag_index + 1) % \
                                     len(self.tags)
            self.after(self.shuffle_speed, self.shuffle)


# Checkbox function
def on_checkbox_toggle(run_func, target):
    global checkbox_var, checkbox
    # change checkbox colour
    checkbox[target].configure(bg=card_checkbox[checkbox_var[target].get()])
    run_func(int(checkbox_var[target].get()), target)


# Post
def Widget(scroll_list, target, title, tags, description, selectable=False,
           bg=card_bg, run_func=None):
    PE[target] = PostEditor()
    global checkbox_var, checkbox

    card = Frame(scroll_list, width=30, bg=bg, padx=8, pady=8, height=50,
                 bd=2, relief='solid')
                 
    # format texts
    def shortened_string(s, max_len):
        if len(s) > max_len:
            return s[:max_len-3] + '...'
        return s

    # shortened_string = lambda s, max_len: (s[:max_len-3] + '...') 
    # if len(s) > max_len else s
    formatted_title = shortened_string(title, max_title_len)
    formatted_description = shortened_string(description, max_description_len)
    # Labels
    title_label = Label(card, bg=bg, fg=card_text, text=formatted_title,
                        font=tiny, pady=3)
    shuffling_tags = ShufflingLabel(card, tags, max_length=15)
    description_text = Text(card, wrap="word", bg=bg, fg=card_text, font=tiny,
                            height=4, width=25, highlightthickness=0, bd=0,
                            pady=3)
    description_text.insert("1.0", formatted_description)
    description_text.config(state=DISABLED)
    # Button
    edit_btn = Button(card, **btn, text='Open/edit',
                      command=(lambda:PE[target].openedit(target)), pady=3)
    edit_btn.configure(width=28)
    # Checkbox
    checkbox_var[target] = BooleanVar(value=False)
    checkbox[target] = Checkbutton(card, variable=checkbox_var[target], 
                  command=lambda: on_checkbox_toggle(run_func, target),
                           bg=card_checkbox[0])
    # place everything
    title_label.pack(anchor=CENTER)
    shuffling_tags.pack(anchor=CENTER)
    description_text.pack()
    edit_btn.pack()
    if selectable:
        checkbox[target].place(anchor=NE, relx=1, rely=0)
    # return card
    return card
