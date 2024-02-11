"""
Description:
    This page will allow the user to edit the details of a post.
"""
# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import libraries
from serv import comm

# Import pages
# Note: To avoid circular importing error, the pages are
#       imported in PostEditor.save(); around lines 39-40.

# Import components
from components import Icon, ScrollList, TagList


class PostEditor:
    def __init__(self):
        self.edit_window = {}
        self.btn_names = ['🔐Unlock', '🔒Lock ']
        self.btn_colours = [style.GREEN, style.RED]
        self.unlock_btn = None  # Button widget
        self.state = 0  # whether the button is locked or not
        self.post = None  # Reassign to tkinter vars
        self.desc = None
        self.widgets = None
        self.TL = {}




    # --- FUNCTIONS ---
    # This saves/applies the changes and closes the window
    def save(self, root, target):
        # import here to avoid circular import error
        import work_phase.view_list
        import work_phase.edit_actions
        # save window
        comm.SERV.send('set_card', data={'target': target, 'key': 'all', 
                       'new_data': {
            'title': self.post['title'].get(),
            'description': self.desc.get('1.0', END).strip(),
            'tags': self.TL[target].get_formatted_tags(),
        }})
        self.state = 0
        # update everything by making them pull the latest data
        work_phase.view_list.update_viewlist(update_card_data_list=True)
        work_phase.edit_actions.update_editactions(update_card_data_list=True)
        # destroy window
        root.destroy()


    # Unlocks or locks all fields
    def change_state(self, render_widgets_func, target):
        self.state = (self.state + 1) % 2  # change state
        # save text
        self.post['description'] = self.desc.get('1.0', END).strip()  
        # self.post['tags'] = self.TL[target].get_formatted_tags()
        print(f"edit_post_win line 62 ( \
            {self.post['tags']==self.TL[target].get_formatted_tags()})", 
            self.post['tags'], self.TL[target].get_formatted_tags())
        # update button
        self.unlock_btn.config(text=self.btn_names[self.state])
        self.unlock_btn.config(bg=self.btn_colours[self.state])
        # lock/unlock fields
        render_widgets_func(target, state=['disabled', 'normal'][self.state])


    # edit the data
    def edit_TL(self, title, option, target):
        self.TL[target].data[title][option] = \
            not self.TL[target].data[title][option]
        if option in self.post['tags']:
            self.post['tags'].remove(option)
        else:
            self.post['tags'].append(option)


    # Function for the page
    def edit_post_win(self, root, target, all_data={}):
        print(f'Target: {target}')
        root.configure(bg=style.bg)

        # Splash image
        splash, img = Icon.Widget(root, image.filter_splash, zoom=1)
        splash.image = img
        splash.place(anchor=N, relx=0.6, rely=0.05)

        # Unlock/lock button
        self.unlock_btn = Button(root, text=self.btn_names[0], **style.btn,
                command=lambda: self.change_state(self.render_widgets, target))
        self.unlock_btn.config(bg=self.btn_colours[0])

        # Save button
        save_btn = Button(root, text='Save and close', **style.btn,
                          command=lambda: self.save(root, target))

        # create scroll_list
        scroll_frame = Frame(root, height=root.winfo_reqheight() * 0.7)
        self.scroll_list = ScrollList.SL(scroll_frame, bg=style.highlight)
        self.scroll_list.place(relx=0, rely=0, relwidth=1, relheight=1)

        # create taglist
        self.TL[target] = TagList.Component(self.scroll_list.frame,
                                on_checkbox_update=lambda title, 
                                option: self.edit_TL(title, option, target))
        print(self.post['tags'])
        self.TL[target].set_tags(self.post['tags'])

        # render widgets 3 times to load, unlock and lock 
        # (fixes graphical issues)
        self.render_widgets(target, first_time=True)
        self.change_state(self.render_widgets, target)
        self.change_state(self.render_widgets, target)

        # Place everything
        self.unlock_btn.place(relx=0.05, rely=0.08)
        save_btn.place(relx=0.05, rely=0.16)
        scroll_frame.place(relx=0, rely=0.3, relheight=0.7, relwidth=1)


    # render the widgets
    def render_widgets(self, target, state='disabled', first_time=False):
        # add everything
        self.scroll_list.clear_widgets()
        self.widgets = []

        # create description widget
        self.desc = Text(self.scroll_list.frame, font=style.tiny,
                    wrap='word', height=30, width=50,
                    bg=style.entry_bg, fg=style.entry_text)
        self.desc.insert(END, self.post['description'])
        self.desc.configure(state=state)

        # title
        self.widgets.append(Label(self.scroll_list.frame, text='Title:',
                                    font=style.h2, bg=style.bg, fg=style.text))
        self.widgets.append(Entry(self.scroll_list.frame, 
                                  textvariable=self.post['title'],
                                  bg=style.entry_bg, fg=style.entry_text, 
                                  font=style.p,
                                  width=30, state=state))
        self.widgets.append(Label(self.scroll_list.frame, text='-' * 10,
                                    font=style.h1, bg=style.highlight, 
                                    fg=style.text))
        # description
        self.widgets.append(Label(self.scroll_list.frame, text='Description:',
                                    font=style.h2, bg=style.bg, fg=style.text))
        self.widgets.append(self.desc)
        self.widgets.append(Label(self.scroll_list.frame, text='-' * 10,
                                    font=style.h1, bg=style.highlight, 
                                    fg=style.text))
        # taglist + spacer
        print(self.post['tags'])
        self.widgets.append(
            self.TL[target].Widget(state=state, load=True, 
                                   tags=self.post['tags']))
        self.widgets.append(Label(self.scroll_list.frame, text=' ',
                                    font=style.h2, bg=style.highlight))
        # place all widgets
        self.scroll_list.populate(self.widgets, **{'sticky':'n', 'pady':5, 
                                                   'padx':40})

    # --- MAKES IT OPEN ---
    # Load this function on button press
    def openedit(self, target):
        print(f'Open/edit button on *{target}* has been pressed.')

        # Check if the window has already been made in the past
        if target not in list(self.edit_window.keys()):
            create_window = True
        else:
            # See if the window is still open or not
            if not self.edit_window[target].winfo_exists():
                create_window = True
            else:
                print("This window is already open.")
                create_window = False

        # create a window
        if create_window:
            # configure window
            self.edit_window[target] = Toplevel()
            self.edit_window[target].title(config.EDIT_WIN_NAME(target))
            self.edit_window[target].geometry(f'{config.EDIT_HEIGHT}x\
{config.EDIT_WIDTH}')
            self.edit_window[target].resizable(height=False, width=False)
            self.state = 0

            # load window
            self.post = {}
            raw_data = {}  # data needs to be formatted
            raw_data = comm.SERV.send('get_card', data={'key':'all', 
                                                        'target':target})
            self.post['title'] = StringVar(value=raw_data['title'])
            self.post['description'] = raw_data['description']
            self.post['tags'] = raw_data['tags']
            print('edit_post_win line 191:', self.post['tags'])
            # Load the new function in the window
            self.edit_post_win(self.edit_window[target], target)
