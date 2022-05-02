import tkinter as tk
from multiprocessing import Pipe
from tkinter import ttk

import numpy as np
from model.CalibrateHandler import CalibrateHandler
from model.ConfigPacker import ConfigParser
from view.main.FrequencyPane import FrequencyPane
from view.main.recording_mode.RecordingSettingPane import RecordingSettingPane
from view.main.recording_mode.RecordingSpecPlot import RecordingSpecPlot
from view.main.recording_mode.RecordingWaterfallPlot import \
    RecordingWaterfallPlot
from view.main.SelectDriverPane import SelectDriverPane


class RecordingPage(ttk.Frame):
    def __init__(self, parent, controller, pipe, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        self.pipe = pipe

        self.save_path = self.controller.session.get_session_workspace_path()

        # Store data for logging later on end
        self.run_count = 1
        self.data_store = []

        # Calibration data
        self.calibrate_data = None
        self.is_calibrating = False

        # Flag to indicate current 2d/3d
        self.is_3d = True

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

        # Create recording plot container
        self.recording_plot_container = tk.Frame(
            self.container
        )
        self.recording_plot_container.pack(
            padx=10,
            pady=10,
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # Waterfall plot - display in first show
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )

        # Create empty plot of graph
        self.recording_plot.create_empty_3d_plot()

        # Create bottom bar of buttons to handle recording mode
        self.bottom = RecordingSettingPane(
            self.recording_plot_container,
            self,
            self.controller
        )

        # Create select driver panel
        self.select_driver_pane = SelectDriverPane(self.container, self.controller)

        # Create side panel
        self.recording_setting = FrequencyPane(
            self.container,
            self.controller
        )

    def handle_calibrate(self):
        if self.is_calibrating == False:
            print("start recording mode calibration")

            # get centre freq
            center_freq = self.recording_setting.get_center_freq()

            # get bandwidth
            bandwidth = self.recording_setting.get_bandwidth()

            # check if calibration can be done
            if center_freq == "" or bandwidth == "":
                self.recording_setting.display_error_message(isStarted=False)
                return

            self.bottom.disable_calibration_button()
            print("start recording mode calibration")
            self.is_calibrating = True

            # Start process
            driver_name = self.select_driver_pane.get_driver_input()
            c = CalibrateHandler()
            self.pipe_here, pipe_calibrate = Pipe(True)
            c.start(driver_name, pipe_calibrate, center_freq, bandwidth, bandwidth)

            self.parent.after(100, self.get_calibrate)
            self.recording_setting.display_calibration_message()

    def get_calibrate(self):
        if self.pipe_here.poll(timeout=0):
            data = self.pipe_here.recv()
            self.calibrate_data = data
            self.is_calibrating = False

        if self.is_calibrating == True:
            self.parent.after(50, self.get_calibrate)
        else:
            self.recording_setting.display_calibration_done()
            self.bottom.enable_calibration_button()
            self.is_calibrating = False
            print("complete recording mode calibration")

    def handle_switch_spec_plot(self):
        self.recording_plot.destroy()
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )
        self.recording_plot.create_empty_3d_plot()
        self.recording_plot.set_2d()
        self.is_3d = False

    def handle_switch_waterfall_plot(self):
        self.recording_plot.destroy()
        self.recording_plot = RecordingWaterfallPlot(
            self.recording_plot_container,
            self.controller,
            self
        )
        self.recording_plot.create_empty_3d_plot()
        self.is_3d = True

    def handle_recording_start(self):
        print("start recording")

        # If forget to run calibrate take 20secs to calibrate
        if self.calibrate_data == None:
            print("Never calibrate")
            return

        # Start spectrum if frequency is valid and not already started
        if self.recording_setting.is_start_stop_freq_valid() and self.controller.is_recording_start == False:

            # Reinitialize
            if self.is_3d:
                self.handle_switch_waterfall_plot()
            else:
                self.handle_switch_spec_plot()

            # Disable toggle to other tab
            self.parent.disable_toggle_tab()

            # disable recording setting panes
            self.bottom.disable_setting_pane()

            # disable frequency toggle
            self.recording_setting.disable_frequency_pane()

            # Set controller state variable
            self.controller.is_recording_start = True

            # get centre freq
            center_freq = self.recording_setting.get_center_freq()

            # get bandwidth
            bandwidth = self.recording_setting.get_bandwidth()

            # Start process
            driver_name = self.select_driver_pane.get_driver_input()
            self.controller.start_recording_process(driver_name, center_freq, bandwidth)

            # Start to retrieve data to plot
            self.parent.after(50, self.get_process)

        # Else display error message
        else:
            # display error
            self.recording_setting.display_error_message(self.controller.is_recording_start)

    def get_process(self):
        if self.controller.is_recording_start == True and self.pipe.poll(timeout=0):
            data = self.pipe.recv()

            average_of_all_calibrate = np.average(data)
            data = np.subtract(data, self.calibrate_data)
            data = data + average_of_all_calibrate

            # do plot
            x = data.tolist()

            for idx in range(len(x)):
                if x[idx] < 0:
                    x[idx] = average_of_all_calibrate

            self.recording_plot.do_plot(x)

            # # append data for storage at end of run
            # self.data_store.append(x)

        else:
            self.parent.after(500, self.get_process)

    def handle_recording_stop(self):
        print("stop recording")

        if self.controller.is_recording_start == True:

            self.controller.stop_recording_process()

            # disable recording setting panes
            self.bottom.enable_setting_pane()

            # disable frequency toggle
            self.recording_setting.enable_frequency_pane()

            # Set controller state variable
            self.controller.is_recording_start = False

            # Enable traversal of tab
            self.parent.enable_toggle_tab()

            # # Save data to file and log out freq used
            # output_data_file = fr"{self.save_path}/recording_data_{self.run_count}"
            # np.save(output_data_file, np.array(self.data_store))
            # output_log_file = fr"{self.save_path}/recording_log_{self.run_count}.txt"
            # with open(output_log_file, "w") as f:
            #     start_freq = self.recording_setting.get_start_freq()
            #     end_freq = self.recording_setting.get_stop_freq()
            #     units = self.recording_setting.get_freq_units()
            #     f.write(f"Start freq: {start_freq}\n")
            #     f.write(f"End freq: {end_freq}\n")
            #     f.write(f"Units: {units}")
            # self.run_count += 1
            self.data_store = []

    # Provide interface for save pane to call common function
    def update_save_path(self, path):
        self.save_path = path

    # Provide interface for save pane to call common function
    def handle_save(self):
        self.handle_recording_save()

    def handle_recording_save(self):
        count = self.controller.session.get_current_recording_plot_num()
        filepath = f"{self.save_path}/recording_{count}"
        self.controller.session.increment_recording_plot_num()
        self.recording_plot.save(filepath)

    def get_driver(self):
        return self.select_driver_pane.get_driver_input()

    def setup_page_from_config(self, config, path):
        start_freq, center_freq, end_freq, driver = ConfigParser().parse_spectrum_config(config)
        self.recording_setting.set_start_freq(start_freq)
        self.recording_setting.set_center_freq(center_freq)
        self.recording_setting.set_stop_freq(end_freq)
        self.select_driver_pane.set_driver_input(driver)

        # self.bottom.set_save_path(path)
        # self.save_path = path
