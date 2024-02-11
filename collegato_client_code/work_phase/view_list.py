"""
Description:
    View list tab (for work phase).  Here, the user can more safely
    operate the program without fearing for commiting a costly accident.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style

# Import components
from components import ScrollList

# import libraries
from serv import comm
from libraries import search

# import windows
from windows.filter_win import filter_win

# only allow 1 filter window to be open at a time
global filter_window, filter_func
filter_window = None
filter_func = lambda a:a


# importable function to set global label
def configure_global_label(s):
    global global_label
    global_label.configure(text=s)


# Opens the filter window
def filter_btn_press():
    global filter_window
    print('Filter button has been pressed!')

    # Check if filter_window is None or already exists
    if filter_window is None or not filter_window.winfo_exists():
        # Create a new window
        filter_window = Toplevel()
        filter_window.title(config.FILTER_WIN_NAME)
        filter_window.geometry(f'{config.FILTER_HEIGHT}x{config.FILTER_WIDTH}')
        filter_window.resizable(height=False, width=False)
        
        # Load the new function in the window
        filter_win(filter_window, configure_global_label, update_viewlist)
    else:
        print("Filter window is already open.")
        

# Searches for stuff
def search_posts(*args):
    global search_var, search_entry, filter_func
    query = search_var.get()
    print(query)
    update_viewlist(_filter_func=filter_func)


# The tab
def view_list_tab(tab, NotificationCard, all_data={}):
    global search_var, search_entry, card_data_list, scroll_list, global_label

    # get cards
    raw_card_data_list = comm.SERV.send('all_card_details', data={
        'email':comm.SERV.email, 'password':comm.SERV.password},
        include_id=False)
    card_data_list = [{**{'target':targ}, **raw_card_data_list[targ]} 
                      for targ in list(raw_card_data_list.keys())]
    
    # Create frames
    header = Frame(tab, bg=style.header_bg)
    scroll_area = Frame(tab, bg=style.bg)

    # Search
    search_var = StringVar(value='')
    search_var.trace_add('write', search_posts)

    # Create header
    magnifying_glass = Label(header, text='🔎', font=style.h1,
                             bg=style.header_bg)
    search_entry = Entry(header, bg=style.entry_bg,
                         fg=style.entry_text, font=style.h2,
                         textvariable=search_var)
    global_label = Label(header, font=style.tiny,
                  text='',
                  bg=style.header_bg, fg=style.header_text)
    filter_btn = Button(header, text='Filter ▼',
                        **{**style.btn, **{'bg':style.RED}},
                        command=filter_btn_press)

    # Place header
    magnifying_glass.place(anchor=CENTER, relx=0.05, rely=0.35)
    search_entry.place(anchor=CENTER, relx=0.3, rely=0.5,
                       relwidth=0.4, relheight=0.7)
    global_label.place(anchor=W, relx=0.51, rely=0.5, relwidth=0.30, 
                       relheight=1)
    filter_btn.place(anchor=E, rely=0.5, relx=0.97)

    # load all the cards and search for stuff
    scroll_list = ScrollList.SL(scroll_area)
    scroll_list.place(relx=0, rely=0, relheight=1, relwidth=1)

    update_viewlist()

    # Place everything
    header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scroll_area.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


# update the scrolllist
def update_viewlist(update_card_data_list=False, _filter_func=None, 
                    assign_filter_func=False):
    global checked, search_var, card_data_list, scroll_list, filter_func
    filter_func = _filter_func or filter_func
    checked = []
    scroll_list.clear_widgets()
    # update data by making calls
    if update_card_data_list:
        raw_card_data_list = comm.SERV.send('all_card_details', data={
            'email':comm.SERV.email, 'password':comm.SERV.password},
            include_id=False)
        card_data_list = [{**{'target':targ}, **raw_card_data_list[targ]} 
            for targ in list(raw_card_data_list.keys())]
    print(card_data_list)
    # load cards
    scroll_list.load_cards(filter_func(search.filter_and_search(
        search_var.get(), 
        card_data_list)), run_func=lambda num, targ: None)
