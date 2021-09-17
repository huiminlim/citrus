import tkinter as tk
from tkinter import ttk

from view.main.coverage_mode.CoverageBar import CoverageBar
from view.main.coverage_mode.CoverageCanvas import CoverageCanvas
from view.main.coverage_mode.CoverageFileMenu import CoverageFileMenu
from view.main.coverage_mode.CoverageMenu import CoverageMenu
from view.main.coverage_mode.CoverageValuesMenu import CoverageValuesMenu


class CoveragePage(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller

        super().__init__(self.parent,  *args, **kwargs)
        self.pack(
            padx=10,
            pady=10,
            fill=tk.BOTH,
            expand=True  # ensures fill out the the parent
        )

        # Create main container
        self.container = ttk.Frame(self)
        self.container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True
        )

        # Create top half of container
        self.left_container = ttk.Frame(self.container)
        self.left_container.pack(
            padx=4,
            pady=4,
            fill=tk.BOTH,
            expand=True,
            side=tk.LEFT
        )

        # Create (menu) bottom half of container
        self.right_container = tk.Frame(self.container)
        self.right_container.pack(
            padx=4,
            pady=4,
            side=tk.RIGHT,
            fill=tk.BOTH
        )

        # Create canvas for left top container
        self.coverage_canvas = CoverageCanvas(self.left_container, self.controller)

        # Create bottom bar
        self.coverage_bar = CoverageBar(self.left_container, self.controller)

        # Create coverage menu to upload file
        self.coverage_file_menu = CoverageFileMenu(self.right_container, self.controller)

        # Create coverage menu bar for right top container
        self.coverage_menu = CoverageMenu(self.right_container, self.controller)

        # Create coverage value menu for right top container
        self.coverage_value_menu = CoverageValuesMenu(self.right_container, self.controller)

    def display_dxf(self, dxf):

        def print_entity(e):
            # print("LINE on layer: %s\n" % e.dxf.layer)
            # print("start point: %s\n" % e.dxf.start)
            # print("end point: %s\n" % e.dxf.end)
            print(f"Start: {e.dxf.start} | End: {e.dxf.end}")

        self.list_object = set()

        # try to parse and make sense of dxf
        msp = dxf.modelspace()
        for e in msp:
            if e.dxftype() == 'LINE':
                print_entity(e)
                # Draw line onto the canvas
                self.coverage_canvas.draw_line(
                    e.dxf.start[0],
                    e.dxf.start[1],
                    e.dxf.end[0],
                    e.dxf.end[1]
                )

                self.list_object.add((e.dxf.start[0], e.dxf.start[1]))
                self.list_object.add((e.dxf.end[0], e.dxf.end[1]))

        print(self.list_object)
