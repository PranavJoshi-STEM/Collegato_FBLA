"""
Description:
    The colours and fonts used in this project
"""

# Import statements
import platform


# --- UNIVERSAL --- 
# colours
bg = ['#a2c4c9', '#326FB4', '#64B5F6', '#6EB0E5'][3]  # shades of blue
text = 'white'
highlight = '#3A4F6F'  # darkblue
_font = ['Verdana', 'Arial'][0]
GREEN = 'green'

# specific ones
_BLACK = '#131312'
    # entry labels
entry_bg = 'white'
entry_text = _BLACK
    # cards in list tabs
card_bg = '#326FB4' # blue
card_text = 'white'
card_checkbox = [_BLACK, 'lime']  # unchecked state, checked state
    # cards in help menu
qna_title = 'green'
qna_title_prefix = '> '
qna_answer = _BLACK
qna_bg = '#FBFAF5' # off-white
    # header
header_text = _BLACK
header_bg = '#a2c4c9' # blue
RED = '#f44346' # red


# texts and buttons (mac has different sizes)
sizes = [75, 35, 20, 15, 10, 9]  # default Windows 11 sizes
button_text = text
# detect mac
if platform.system() == 'Darwin':
    button_text = _BLACK
# load sizes
title = (_font, sizes[0])
h1 = (_font, sizes[1])  # header
h2 = (_font, sizes[2])  # subheader
p = (_font, sizes[3])  # normal text
tiny = (_font, sizes[4])  # for the cards
ultra_tiny = (_font, sizes[5])  # for the notification card

# unpacked styles
be_48x48 = {'zoom': 4, 'subsample': 5}
be_96x96 = {'zoom': 1, 'subsample': 2}
btn = {'bg': '#76a5af', 'width': 20, 'height': 2, 'fg': button_text}
edit_actions_btn = {'bg': RED, 'width': 10, 'height': 2, 'fg': text}
