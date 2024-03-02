import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from modules.config.constants import UiText
import modules.controllers.facade as facade
from modules.config.logger import setup_logging
from modules.controllers.view_data import ViewData

logger = setup_logging()

class ViewGeneratorApp:
    def __init__(self, root):
        self.log_box = None
        self.generate_button = None
        self.scale_entry = None
        self.scale_label = None
        self.explanation = None
        self.title = None
        self.url_label = None
        self.url_entry = None
        self.char_radio = None
        self.ship_radio = None
        self.type_var = None
        self.root = root
        self.root.title(UiText.APP_TITLE)

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Title and explanation label
        self.title = ttk.Label(self.main_frame, text=UiText.APP_TITLE, font=("Segoe UI", 16))
        self.title.grid(row=0, column=0, columnspan=2, pady=10)

        self.explanation = ttk.Label(self.main_frame, text=UiText.HELP_TEXT)
        self.explanation.grid(row=1, column=0, columnspan=2, pady=5)

        # URL entry
        self.url_label = ttk.Label(self.main_frame, text="URL:")
        self.url_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.grid(row=2, column=1, sticky=tk.E, pady=5)

        # Type selection (Ship or Character)
        self.type_var = tk.StringVar()
        self.ship_radio = ttk.Radiobutton(self.main_frame, text="Ship", variable=self.type_var, value="ship")
        self.ship_radio.grid(row=3, column=0, pady=5)
        self.char_radio = ttk.Radiobutton(self.main_frame, text="Character", variable=self.type_var, value="char")
        self.char_radio.grid(row=3, column=1, pady=5)
        self.type_var.set("ship")  # Default selection

        # Ship scale multiplier
        self.scale_label = ttk.Label(self.main_frame, text="Ship Scale Multiplier:")
        self.scale_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.scale_entry = ttk.Entry(self.main_frame, width=50)
        self.scale_entry.grid(row=4, column=1, sticky=tk.E, pady=5)

        # Generate button
        self.generate_button = ttk.Button(self.main_frame, text="Generate", command=self.generate_3d_view)
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Log box
        # self.log_box = scrolledtext.ScrolledText(self.main_frame, width=60, height=10, state='disabled')
        # self.log_box.grid(row=6, column=0, columnspan=2, pady=10)
        # self.log_box.config(state='normal')  # Enable editing to add logs

    def generate_3d_view(self):
        url = self.url_entry.get()
        type_selection = self.type_var.get()
        scale_multiplier = self.scale_entry.get()

        wreck_list_a, wreck_list_b = facade.create_both_wreck_lists(url)

        logger.info(f"Length of wreck_list_a: {len(wreck_list_a)}")
        logger.info(f"Length of wreck_list_b: {len(wreck_list_b)}")
        logger.info("Spinning up the graphics engine. This may take a moment!")

        self.root.destroy()
        facade.run_main_program(wreck_list_a, wreck_list_b, type_selection, float(scale_multiplier))



    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.config(state='disabled')
        self.log_box.yview(tk.END)


def start_ui():
    root = tk.Tk()
    app = ViewGeneratorApp(root)
    root.mainloop()
    return app.url_entry.get()
