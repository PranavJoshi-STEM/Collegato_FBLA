"""
Description:
    Edit actions tab (for work phase).
    This tab contains more powerful actions so the user can do operations
    quickly.
"""

# Import statements
from tkinter import ttk
from tkinter import *

# Import configs
from configs import style

# Import components
from components import ScrollList, TagList

# Import libraries
from serv import comm
from libraries import search

# Import pages
from windows import edit_post_win
from work_phase.view_list import update_viewlist

# import windows
from windows.filter_win import filter_win


# count boxes ticked
global checked
checked = []


# Searches for stuff
def search_posts(*args):
    global search_var, search_entry
    query = search_var.get()
    print(query)
    update_editactions()


# see if the buttons should be enabled or not
def check_state(num, target):
    global delete_btn, open_btn, checked

    # if it was unchecked
    if num==0:
        checked.pop(checked.index(target))
    # if it was checked
    elif num==1:
        checked.append(target)

    # see if buttons should be enabled
    if len(checked) > 0:
        delete_btn.configure(state='normal')
        open_btn.configure(state='normal')
    elif len(checked)==0:
        delete_btn.configure(state='disabled')
        open_btn.configure(state='disabled')
    else:
        print(f'How is this possible? checked={checked}')


# delete all selected cards
def delete_all():
    global checked, card_data_list, delete_btn, open_btn
    print(f'Deleting: {checked}')

    # delete all cards
    card_data_list = [card_data for card_data in card_data_list if 
                      card_data['target'] not in checked]
    delete_btn.configure(state='disabled')
    open_btn.configure(state='disabled')
    comm.SERV.send('delete_card', data={'target_list':checked})
    update_viewlist(update_card_data_list=True)
    # update screen
    update_editactions()


# open all selected cards
def open_all():
    global checked
    print(f'Opening: {checked}')
    editors = {}
    # open all cards
    for target in checked:
        editors[target] = edit_post_win.PostEditor()
        editors[target].openedit(target)
    

# create a new card
def new():
    global card_data_list
    targ = comm.SERV.send('add_card', data={'title':'Unnamed', 'tags': [],
        'description':'Enter information here... \
(i.e., contact info, email, description)'})
    card_data_list.append({'title':'Unnamed', 'tags': [], 'target':targ,
        'description':'Enter information here... \
(i.e., contact info, email, description)'})
    update_viewlist(update_card_data_list=True)
    update_editactions()


# The tab
def edit_actions_tab(tab, NotificationCard, all_data={}):
    global search_var, search_entry, delete_btn, open_btn, card_data_list, \
           scroll_list

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
    search_entry = Entry(header, bg=style.entry_bg, fg=style.entry_text,
                         font=style.h2,
                         textvariable=search_var)
    label = Label(header, text='| Actions:', font=style.h2,
                  fg=style.header_text, bg=style.header_bg)
    delete_btn = Button(header, text='- Delete', **style.edit_actions_btn, 
                        command=delete_all)
    delete_btn.configure(state='disabled')
    open_btn = Button(header, text='* Open', **style.edit_actions_btn, 
                      command=open_all)
    open_btn.configure(state='disabled')
    new_btn = Button(header, text='+ New', **style.edit_actions_btn, 
                     command=new)

    # Place header
    magnifying_glass.place(anchor=CENTER, relx=0.05, rely=0.35)
    search_entry.place(anchor=CENTER, relx=0.3, rely=0.5, relwidth=0.4,
                       relheight=0.7)
    label.place(anchor=W, relx=0.5, rely=0.5, relwidth=0.15, relheight=0.8)
    delete_btn.place(anchor=W, relx=0.67, rely=0.5)
    open_btn.place(anchor=W, relx=0.77, rely=0.5)
    new_btn.place(anchor=W, relx=0.87, rely=0.5)

    # load all the cards and search for stuff
    scroll_list = ScrollList.SL(scroll_area)
    scroll_list.place(relx=0, rely=0, relheight=1, relwidth=1)
    
    # update the edit actions scroll list with all the new data
    update_editactions()

    # Place everything
    header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scroll_area.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


# update the scroll list of edit actions
def update_editactions(update_card_data_list=False):
        global checked, search_var, card_data_list, scroll_list
        checked = []
        scroll_list.clear_widgets()
        if update_card_data_list:
            raw_card_data_list = comm.SERV.send('all_card_details', data={
                'email':comm.SERV.email, 'password':comm.SERV.password},
                include_id=False)
            card_data_list = [{**{'target':targ}, **raw_card_data_list[targ]} 
                for targ in list(raw_card_data_list.keys())]
        scroll_list.load_cards(search.filter_and_search(search_var.get(), 
            card_data_list), selectable=True, run_func=check_state)
