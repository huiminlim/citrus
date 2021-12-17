import tkinter as tk
import tkinter.ttk as ttk

from view.main.coverage_mode.sdr_mode.CoverageSdrTab import CoverageSdrTab
from view.main.coverage_mode.wifi_mode.CoverageWifiTab import CoverageWifiTab


class CoverageDataScanner(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        # iid for entries
        self.idx = 0

        super().__init__(
            self.parent,
            # text="Data Scanner",
            *args, **kwargs
        )
        self.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.X
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            side=tk.TOP,
            anchor=tk.NW,
            fill=tk.BOTH
        )

        # create notebook to choose interface
        self.interfaces_selection = ttk.Notebook(
            self,
            style="primary.TNotebook",
            * args, **kwargs
        )
        self.interfaces_selection.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Add SDR tab
        self.sdr_tab = CoverageSdrTab(
            self.interfaces_selection,
            self.controller
        )

        # Add Wifi tab
        self.wifi_tab = CoverageWifiTab(
            self.interfaces_selection,
            self.controller
        )

        self.interfaces_selection.add(
            self.wifi_tab,
            text="WIFI"
        )
        self.interfaces_selection.add(
            self.sdr_tab,
            text="SDR"
        )

        # Select wifi as main tab
        self.interfaces_selection.select(self.wifi_tab)

    def disable_scan_button(self):
        pass
        # self.scan_button.state = tk.DISABLED

    def enable_scan_button(self):
        pass
        # self.scan_button.state = tk.NORMAL

    def populate_wifi_scan_results(self, json_list):
        for json in json_list:
            ssid = json['ssid']
            bssid = json['bssid']
            freq = json['channel_frequency']
            channel = json['channel_number'] + "@" + json['channel_width']

            self.wifi_tab.display_all_panel.insert(
                parent="",
                index=self.idx,
                iid=self.idx,
                text="",
                values=(ssid, bssid, freq, channel)
            )
            self.idx += 1

    def clear_wifi_scan_results(self):
        pass
        # self.panel.delete(*self.panel.get_children())

    def get_current_selected(self):
        return ""
        # return copy.deepcopy(self.current_selected)