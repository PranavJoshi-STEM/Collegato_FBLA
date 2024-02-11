# Import tkinter
from tkinter import *

# Import style
from configs import style

global_widgets = []
global img


def Widget(frame, path, zoom=1, subsample=1):

    img = PhotoImage(master=frame, file=path)
    # Apply zoom operation
    zoomed_img = img.zoom(zoom, zoom)
    
    # Apply subsample operation to the zoomed image
    final_img = zoomed_img.subsample(subsample, subsample)

    displayed_image = Label(frame, image=final_img, bg=style.bg)
    # Store a reference to the image to prevent Python's automatic garbage
    # collection
    displayed_image.image = img
    global_widgets.append(displayed_image)

    return displayed_image, final_img
