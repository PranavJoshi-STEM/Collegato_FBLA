"""
Description:
    Help menu tab (for work phase).
    Here, the user can find helpful information on how to
    operate the application.
    
Note:
    We don't follow PEP-8's 79 char line limit in this file as it's much
    easier to read QNA_LIST when the sentences are stretched out.  This
    more accurately reflects Python's zen of being readable.
"""

# Import tkinter
from tkinter import ttk
from tkinter import *

# Import configs
from configs import config, style, image

# Import libraries
from libraries import search

# Import components
from components import ScrollList

# --- ALL Q&A ---
QNA_LIST = [
    {"q": "How can I add a post?", 
     "a": "To add a post, go to *Edit Actions* and click on 'Add Post'."
    },
    {"q": "How do I delete a post?",
     "a": "To delete a post, go to *Edit Actions*, select the specific post and click on the 'Delete' option."
    },
    {"q": "What is the app about?",
     "a": "The app is designed for managing posts and opportunities."
    },
    {"q": "How can I change my password?",
     "a": "To change your account password, go to *Account Settings* and change your password."
    },
    {"q": "Can I edit my posts after publishing?",
     "a": "Yes, you can edit your posts after publishing. Simply locate the post and click on the 'Edit' option."
    },
    {"q": "Is this app paid?",
     "a": "No, the app is free to use with no associated fees."
    },
    {"q": "How can I contact support?",
     "a": "For support, you can reach out to Pranav Joshi (Joshipn2018@gmail.com) or Yajat Mittal by email."
    },
    {"q": "What is the max amount of posts?",
     "a": "There is no set limit to the number of posts you can create."
    },
    {"q": "What happens if I forget my password?",
     "a": "If you forget your password, you can use the 'Forgot Password' option on the login screen to reset it."
    },
    {"q": "Is my personal information secure?",
     "a": "Yes, we prioritize the security of your personal information through advanced encryption and security measures."
    },
    {"q": "Are there any age restrictions?",
     "a": "No, this app can be used by anyone."
    },
    {"q": "How often are app updates released?",
     "a": "App updates are released monthly to introduce new features and improvements. Keep your app up-to-date for the latest enhancements."
    },
    {"q": "Can I access the app offline?",
     "a": "No, full functionality requires an internet connection."
    },
]


# --- TAB RELATED STUFF ---
# Declare global variables
qna_matches = []
current_match_index = 0


# The qna card that will be rendered
def qna_card(frame, index, _QNA_LIST, remove_char=False):
    subframe = Frame(frame, bg=style.qna_bg, width=60, height=40)
    data = _QNA_LIST[index]
    # create widgets
    text = ''
    if remove_char:
        text += style.qna_title_prefix
    text += data['q']
    title = Label(subframe, text=text,
                  fg=style.qna_title, font=style.p, bg=style.qna_bg)
    description = Text(subframe, wrap='word', bg=style.qna_bg,
                       fg=style.qna_answer, font=style.p,
                       height=6, width=30, highlightthickness=0, bd=0,
                       pady=3)
    description.insert("1.0", data['a'])
    description.config(state=DISABLED)
    # place widgets
    title.pack(pady=5)
    description.pack(padx=5)
    # return subframe
    return subframe


# The tab with all of the help_menu's GUI
def help_menu_tab(tab, NotificationCard):
    # render the qna on button press
    def show_qna(match_index):
        global qna_matches
        if match_index != 'nothing found':
            if qna_matches:
                render_card(qna_matches[match_index][0]["q"],
                            qna_matches[match_index][0]["a"])
        else:
            render_card('No matches found.', '', remove_char=True)


    # find a match and render it
    def search_and_show():
        global qna_matches
        query = search_entry.get()

        qna_matches = search.qna_search(QNA_LIST, query)
        
        if qna_matches:
            show_qna(0)  # Show the best match
        else:
            show_qna('nothing found')


    # go next in list if the user presses the next button
    def next_match():
        global current_match_index
        if qna_matches:
            current_match_index = (current_match_index + 1) % len(qna_matches)
            show_qna(current_match_index)


    # --- SEARCH FRAME ---
    search_frame = Frame(tab, width=tab.winfo_reqwidth()//2, bg=style.bg)
    # Search entry
    label = Label(search_frame, text='Search 🔎', font=style.h1,
                             bg=style.highlight, fg=style.text)
    search_entry = Entry(search_frame, bg=style.entry_bg, fg=style.entry_text,
                         font=style.h2,
                         textvariable=search)
    
    label.place(anchor=CENTER, relx=0.5, rely=0.1)
    search_entry.place(anchor=CENTER, relx=0.5, rely=0.2, relwidth=0.8,
                       height=30)

    # show qna card
    def render_card(question='', answer='', remove_char=False):
        # forget the card if possible
        try:
            card.place_forget()
        except:
            pass
        card = qna_card(search_frame, 0, [{'q':question,'a':answer}],
                        remove_char=remove_char)
        card.place(anchor=CENTER, relx=0.5, rely=0.7, relwidth=0.85)
    render_card()
    # Buttons
    search_btn = Button(search_frame, text='Search', **style.btn,
                    command=search_and_show)
    next_btn = Button(search_frame, text='Next match', **style.btn,
                    command=next_match)
    # Render buttons
    search_btn.place(anchor=CENTER, relx=0.3, rely=0.4)
    next_btn.place(anchor=CENTER, relx=0.7, rely=0.4)


    # --- ALL CARDS FRAME ---
    all_cards_frame = Frame(tab, width=tab.winfo_reqwidth()//2)
    # the header
    header = Label(all_cards_frame, text='All QnA Cards:', font=style.h2,
                   bg=style.highlight, fg=style.text)
    # scroll_list and scroll_frame (so the scrollbar is smaller)
    scroll_frame = Frame(all_cards_frame, height=tab.winfo_reqheight()//10*9, 
                         bg=style._BLACK)
    scroll_list = ScrollList.SL(scroll_frame, bg=style._BLACK)
    # load all qna cards
    scroll_list.load_qna_cards(qna_card, QNA_LIST)
    # place everything
    header.place(relx=0, rely=0, relwidth=1, relheight=0.1)
    scroll_list.pack(expand=True, fill='both')
    scroll_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)


    # --- PLACE BOTH FRAMES ---
    search_frame.place(anchor=NW, relx=0, rely=0, relwidth=0.5, relheight=1)
    all_cards_frame.place(anchor=NW, relx=0.5, rely=0, relwidth=0.5, 
                          relheight=1)
