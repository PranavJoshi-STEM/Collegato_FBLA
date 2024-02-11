"""
Description:
    This page will allow the user to filter through all posts.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import components
from components import Icon, TagList


# applies the filter
def apply_filter(root, _TL, conf_global_label, update_viewlist):
    print('Applying filter!')
    data = _TL.return_tags()
    # Get tags
    print(data)
    tags = []
    for category_data in data.values():
        for tag, value in category_data.items():
            if value:
                tags.append(tag)
    print(tags)

    # Update text
    if not tags:
        text = "No filters applied."
    # format text to be displayed
    else:
        max_line_length = 35
        lines = []
        current_line = []
        current_length = 0

        # Calculate sentences
        for tag in tags:
            tag_length = len(tag) + 2
            if current_length + tag_length <= max_line_length:
                current_line.append(tag)
                current_length += tag_length
            else:
                lines.append(", ".join(current_line))
                current_line = [tag]
                current_length = tag_length
        if current_line:
            lines.append(", ".join(current_line))

        # Choose how to render text
        if len(lines) > 1:
            text = f"{len(tags)} Filters: {lines[0]},"+'\n'+f"{lines[1]}..."
        else:
            text = f"{len(tags)} Filters: {lines[0]}"

    # enact search
    def filter_tags(card_data_list):
        # make sure there are search params to filter
        if tags==[]:
            return card_data_list
        new_card_data_list = [card for card in card_data_list if
                              any(tag in tags for tag in card['tags'])]
        return new_card_data_list
    # update view_list
    conf_global_label(text)
    update_viewlist(_filter_func=filter_tags)


# The window
def filter_win(root, conf_global_label, update_viewlist):
    TL = TagList.Component(root)
    root.configure(bg=style.bg)
    # Splash image
    splash, img = Icon.Widget(root, image.filter_splash, zoom=1)
    splash.image = img
    splash.place(anchor=N, relx=0.5, rely=0.05)
    # tag list
    tag_list = TL.Widget()
    # all the buttons
    select_all_btn = Button(root, text='Select all', **style.btn,
                            command=lambda: TL.set_all_true())
    deselect_all_btn = Button(root, text='Deselect all', **style.btn,
                              command=lambda: TL.set_all_false())
    apply_btn = Button(root, text='Apply', **style.btn,
                       command=lambda: apply_filter(root, TL, 
                                                    conf_global_label, 
                                                    update_viewlist))
    # place everything
    tag_list.place(anchor=CENTER, relx=0.5, rely=0.6)
    btn_y = 0.9
    select_all_btn.place(anchor=N, relx=0.25, rely=btn_y)
    deselect_all_btn.place(anchor=N, relx=0.5, rely=btn_y)
    apply_btn.place(anchor=N, relx=0.75, rely=btn_y)
    