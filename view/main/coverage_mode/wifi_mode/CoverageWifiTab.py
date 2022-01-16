import tkinter as tk
from tkinter import ttk


class CoverageWifiTab(ttk.Frame):
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

        # Currently selected row of data from list of all wifi
        self.current_selected_from_display_all = {}

        # Currently selected row of data from list of selected
        self.current_item_in_selected_panel = ""

        # String length for button
        self.STRING_LENGTH = 10

        # uuid for selected
        self.iid = 0

        # Create column name list to select active wifi
        self.column_names = [
            'ssid',
            'bssid',
            'freq',
            'channel[#@MHz]'
        ]

        self.column_width = {
            'ssid': 160,
            'bssid': 140,
            'freq': 50,
            'channel[#@MHz]': 120
        }

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # # Create coverage value menu for rssi filtering
        # self.coverage_value_menu = CoverageValuesMenu(self.container, self.controller)

        # Label to inform display ALL ssid scanned
        self.display_all_panel_label = ttk.Label(
            self.container,
            text="All SSID available:"
        )
        self.display_all_panel_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

        # Create display treeview panel to show wifi ALL ssid scanned
        self.display_all_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.display_all_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.TOP
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.display_all_panel.column(
                column_name,
                width=self.column_width[column_name],
                anchor=tk.W
            )
            self.display_all_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # Label to inform display ALL ssid scanned
        self.display_tracked_panel_label = ttk.Label(
            self.container,
            text="SSID tracked:"
        )
        self.display_tracked_panel_label.pack(
            side=tk.TOP,
            anchor=tk.NW,
            padx=10,
            pady=5
        )

        # Create display treeview panel to show SELECTED SSID
        self.display_tracked_panel = ttk.Treeview(
            self.container,
            show='headings',
            style='primary.Treeview',
            columns=self.column_names,
            height=5
        )
        self.display_tracked_panel.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            anchor=tk.NW,
            side=tk.BOTTOM
        )

        # Setup columns and headings
        for column_name in self.column_names:
            self.display_tracked_panel.column(
                column_name,
                width=self.column_width[column_name]
            )
            self.display_tracked_panel.heading(
                column_name,
                text=column_name,
                anchor=tk.CENTER
            )

        # Container for button utilities
        self.button_container = ttk.Frame(self)
        self.button_container.pack(
            padx=5,
            side=tk.TOP,
            anchor=tk.CENTER
        )

        # Create scan button
        self.scan_button = ttk.Button(
            self.button_container,
            style="primary.TButton",
            text="Scan".center(self.STRING_LENGTH, ' '),
            command=self.controller.do_coverage_wifi_scan
        )
        self.scan_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create clear button
        self.clear_button = ttk.Button(
            self.button_container,
            style="secondary.TButton",
            text="Clear".center(self.STRING_LENGTH, ' '),
            command=self.coverage.clear_wifi_scan_results
        )
        self.clear_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create down button
        self.track_button = ttk.Button(
            self.button_container,
            style="success.TButton",
            text="Track".center(self.STRING_LENGTH, ' '),
            command=self.move_item_to_selected
        )
        self.track_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=(0, 10)
        )

        # Create down button
        self.untrack_button = ttk.Button(
            self.button_container,
            style="danger.TButton",
            text="Untrack".center(self.STRING_LENGTH, ' '),
            command=self.remove_item_from_selected
        )
        self.untrack_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=(0, 10)
        )

        # Allow clicking of treeview items
        self.display_all_panel.bind('<ButtonRelease-1>', self.select_item_from_display_all)

        # Allow clicking of treeview items
        self.display_tracked_panel.bind('<ButtonRelease-1>', self.select_item_from_display_tracked)

    # Store clicked item in the ALL pane corresponding to click action
    def select_item_from_display_all(self, a):
        curItem = self.display_all_panel.focus()
        data = self.display_all_panel.item(curItem)['values']

        try:
            idx = 0
            for name in self.column_names:
                self.current_selected_from_display_all[name] = data[idx]
                idx += 1
        except IndexError:
            return

    # Store clicked item in the Selected pane corresponding to click action
    def select_item_from_display_tracked(self, a):
        self.current_item_in_selected_panel = self.display_tracked_panel.focus()

    def move_item_to_selected(self):
        self.display_tracked_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple(self.current_selected_from_display_all.values())
        )
        self.iid += 1

    def clear_all_wifi_panel(self):
        self.display_all_panel.delete(*self.display_all_panel.get_children())

    def remove_item_from_selected(self):
        # If no items clicked, ignore
        if not self.display_tracked_panel.focus():
            return

        self.display_tracked_panel.delete(self.display_tracked_panel.focus())

    # Get list of selected MAC/bssid addr in SELECTED panel
    def get_tracked_list(self, isBSSID=True, isSSID=False):

        ssid_list = []

        idx = 1
        if isBSSID:
            idx = 1
        elif isSSID:
            idx = 0

        for child in self.display_tracked_panel.get_children():
            all_data = self.display_tracked_panel.item(child)["values"]
            ssid_list.append(all_data[idx])  # assumes first item is bssid

        return ssid_list

    def bssid2ssid(self, bssid):

        mapping = {}

        for child in self.display_tracked_panel.get_children():
            all_data = self.display_tracked_panel.item(child)["values"]
            mapping[all_data[1]] = all_data[0]

        return mapping[bssid]

    def insert(self, json):

        # Prepare data
        ssid = json["ssid"]
        bssid = json["bssid"]
        channel_freq = str(json["channel_frequency"])
        channel = str(json['channel_number']) + "@" + str(json['channel_width'])

        data = (ssid, bssid, channel_freq, channel)

        self.display_tracked_panel.insert(
            parent='', index=self.iid, iid=self.iid,
            values=tuple(data)
        )
        self.iid += 1
