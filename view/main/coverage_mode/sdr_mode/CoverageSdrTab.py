import tkinter as tk
from tkinter import ttk


class CoverageSdrTab(ttk.Frame):
    def __init__(self, parent, controller, coverage, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.coverage = coverage

        super().__init__(
            self.parent,
            *args, **kwargs
        )
        self.pack(
            side=tk.BOTTOM,
            fill=tk.X
        )

        # uuid for selected
        self.iid = 0

        # Currently selected row of data from list of tracked freq
        # map (col_name->val)
        self.current_selected = {}

        # for clearing purposes
        self.current_selected_focus = ""

        # Create column name list to show tracked freq
        self.column_names = [
            'name',
            'freq (MHz)'
        ]

        self.column_width = {
            'name': 100,
            'freq (MHz)': 50
        }

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH,
            expand=True
        )

        # Label to inform display tracking
        self.tracking_label = ttk.Label(
            self.container,
            text="Tracking Frequencies:"
        )
        self.tracking_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

        # Create display treeview panel to show all freq tracked
        self.tracking_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            # height=5
        )
        self.tracking_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.TOP
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.tracking_panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.CENTER
            )
            self.tracking_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # Allow clicking of treeview items
        self.tracking_panel.bind('<ButtonRelease-1>', self.select_item)

        # ---------------------------------------------

        # Create container for form to input tracked freq
        self.form_container = ttk.LabelFrame(self, text="Add New Tracked")
        self.form_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        self.form_internal_container = ttk.Frame(self.form_container)
        self.form_internal_container.pack(
            padx=10,
            pady=10,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # Input tracked freq name label and entry box
        self.tracked_name_label = tk.Label(
            self.form_internal_container,
            text="Name",
            width=15,
            anchor=tk.NW
        )
        self.tracked_name_label.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.tracked_name_text = tk.StringVar()
        self.tracked_name = ttk.Entry(
            self.form_internal_container,
            textvariable=self.tracked_name_text
        )
        self.tracked_name.grid(
            row=0,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Input tracked freq label and entry box
        self.tracked_freq_label = tk.Label(
            self.form_internal_container,
            text="Tracked Frequency",
            width=15,
            anchor=tk.NW
        )
        self.tracked_freq_label.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=5,
            pady=5
        )
        self.tracked_freq_text = tk.StringVar()
        self.tracked_freq = ttk.Entry(
            self.form_internal_container,
            textvariable=self.tracked_freq_text
        )
        self.tracked_freq.grid(
            row=1,
            column=5,
            columnspan=2,
            padx=5,
            pady=5
        )

        # Button Containers
        self.button_containers = tk.Frame(self)
        self.button_containers.pack(side=tk.TOP)

        # TODO: fix the command
        self.track_button = ttk.Button(
            self.button_containers,
            style="primary.Outline.TButton",
            text="Track",
            command=self.add_to_tracked
        )
        self.track_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )

        # TODO: fix the command
        self.untrack_button = ttk.Button(
            self.button_containers,
            style="primary.Outline.TButton",
            text="Untrack",
            command=self.untrack_item
        )
        self.untrack_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.LEFT,
            anchor=tk.CENTER
        )

        # TODO: fix the command
        self.clear_button = ttk.Button(
            self.button_containers,
            style="primary.Outline.TButton",
            text="Clear",
            command=self.coverage.clear_sdr_scan_results
        )
        self.clear_button.pack(
            padx=5,
            pady=(0, 10),
            side=tk.RIGHT,
            anchor=tk.CENTER
        )

    # # Store clicked item in the ALL pane corresponding to click action
    # def get_items(self):
    #     curItem = self.tracking_panel.focus()
    #     data = self.tracking_panel.item(curItem)['values']
    #     print(data)

    #     try:
    #         idx = 0
    #         for name in self.column_names:
    #             self.current_selected[name] = data[idx]
    #             idx += 1
    #     except IndexError:
    #         return

    def select_item(self, a):
        self.current_selected_focus = self.tracking_panel.focus()

    def untrack_item(self):
        # If no items clicked, ignore
        if not self.tracking_panel.focus():
            return

        self.tracking_panel.delete(self.tracking_panel.focus())

    def clear_all_sdr_panel(self):
        self.tracking_panel.delete(*self.tracking_panel.get_children())

    def add_to_tracked(self):

        name = self.tracked_name_text.get()
        try:
            freq = float(self.tracked_freq_text.get())
        except ValueError:
            # TODO: show error message
            return

        self.tracking_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple((name, freq))
        )
        self.iid += 1

        # clear value after get
        self.tracked_name_text.set("")
        self.tracked_freq_text.set("")
