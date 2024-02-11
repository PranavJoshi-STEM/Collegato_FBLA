import tkinter as tk
from configs import style


default_data = {
    'Ages':     {'13':False, '14':False, '15':False, '16':False, '17':False, 
                    '18':False, '18+':False},
    'Field':    {'Business':False, 'Engineering':False, 'IT':False,
                    'Music':False, 'Art':False, 'Law':False, 'Medical':False,
                    'Other':False},
    'Location': {'In-school':False, 'Online':False,
                    'External':False},
    'Timing':   {'Lunch':False, 'Weekends':False, 'Weekdays':False}
}


class Component:
    def __init__(self, root, data=None, on_checkbox_update=None, 
                fg=style._BLACK, bg=style.bg, state='normal'):
        self.root = root
        self.data = data or default_data
        self.on_checkbox_update = on_checkbox_update or \
        self.default_on_checkbox_update
        self.fg = fg
        self.bg = bg

        self.checkbox_widgets = {}
        self.checkbox_vars = {}

        # Call Widget method directly in the constructor
        self.Widget()


    def default_on_checkbox_update(self, title, option):
        print(f"Checkbox updated: {title} - {option}")


    def Widget(self, state='normal', load=False, tags=[]):
        frame = tk.Frame(self.root, bg=self.bg)

        for i, (title, options) in enumerate(self.data.items()):
            label = tk.Label(frame, text=f"{title}:", padx=10, bg=self.bg, 
                             font=style.p, fg=self.fg)
            label.grid(row=0, column=i, sticky="s")

            # Initialize checkbox_vars to store BooleanVar for each checkbox
            self.checkbox_vars[title] = [tk.BooleanVar() for _ in options]

            checkboxes = []
            for j, (option, checkbox_var) in enumerate(
                zip(options, self.checkbox_vars[title])):
                checkbox = tk.Checkbutton(frame, text=f"{option}", 
                                          variable=checkbox_var,
                                          fg=self.fg, bg=self.bg, 
                                          font=style.tiny,
                                          command=lambda option=option,
                          title=title: self.on_checkbox_update(title, option))
                checkbox.grid(row=j+1, column=i, sticky="w", padx=5)
                checkboxes.append(checkbox)

            # Store checkboxes for later reference
            self.checkbox_widgets[title] = checkboxes

        # load data when applicable
        if load:
            self.set_tags(tags)
        
        # disabled or enable
        if state == 'normal':
            self.enable_all_checkboxes()
        elif state == 'disabled':
            self.disable_all_checkboxes()
        
        return frame


    # disabled all checkboxes
    def disable_all_checkboxes(self):
        try:
            for title, options in self.data.items():
                for i, option in enumerate(options):
                    self.checkbox_widgets[title][i].config(state=tk.DISABLED)
        except:
            pass


    # enable all checkboxes
    def enable_all_checkboxes(self):
        try:
            for title, options in self.data.items():
                for i, option in enumerate(options):
                    self.checkbox_widgets[title][i].config(state=tk.NORMAL)
        except:
            pass


    # return the data
    def return_tags(self):
        loaded_data = {}
        for category, tags in self.data.items():
            loaded_data[category] = {tag: self.checkbox_vars[category][i].get()
             for i, tag in enumerate(tags)}
        return loaded_data
    

    # get all the true tags in a list
    def get_formatted_tags(self):
        true_tags = []
        for category, tag_dict in self.data.items():
            for tag, val in tag_dict.items():
                if val:
                    true_tags.append(tag)
        return true_tags


    # set all data
    def set_tags(self, enabled_tags):
        for category, tag_dict in self.data.items():
            for i, tag in enumerate(tag_dict):
                tag_dict[tag] = tag in enabled_tags
                self.checkbox_vars[category][i].set(tag_dict[tag])


    # set all the values to true
    def set_all_true(self):
        for title, options in self.data.items():
            for i, option in enumerate(options):
                self.checkbox_vars[title][i].set(True)


    # set all values to false
    def set_all_false(self):
        for title, options in self.data.items():
            for i, option in enumerate(options):
                self.checkbox_vars[title][i].set(False)
