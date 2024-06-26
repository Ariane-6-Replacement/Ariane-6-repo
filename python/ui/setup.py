import copy
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk

from python.core.rocket import get_elysium_1_preset, get_falcon_9_preset

# This file contains the UI class which is used to create the input and output screen for the rocket.
# It uses the tkinter library as its base and creates the input screen based on the inputs given in the main.py file.
class Label():
    def __init__(self, root, label, **kwargs):
        self.label = ttk.Label(root, text=label, **kwargs)

class Entry():
    def __init__(self, root, value, range=None, **kwargs):
        self.var = tk.StringVar(value=str(value))
        self.element = ttk.Entry(root, textvariable=self.var, **kwargs)
        self.range = range

class Button():
    def __init__(self, root, columnspan, **kwargs):
        self.label = ttk.Button(root, **kwargs)
        self.label.grid(columnspan=columnspan)

class LabelEntry(Label):
    def __init__(self, root, label, value, range=None, **kwargs):
        super().__init__(root, label)
        self.var = tk.StringVar(value=str(value))
        self.element = ttk.Entry(root, textvariable=self.var, **kwargs)
        self.range = range

class LabelCombobox(Label):
    def __init__(self, root, label, value_index, values, callback=None, **kwargs):
        super().__init__(root, label)
        assert value_index < len(values), "Specified dropdown index is outside of range of values provided"
        self.var = tk.StringVar(value=str(values[value_index]))
        self.element = ttk.Combobox(root, textvariable=self.var, values=values, **kwargs)
        self.var.trace_add("write", callback)

class LabelCheckbutton(Label):
    def __init__(self, root, label, value, **kwargs):
        super().__init__(root, label)
        self.var = tk.BooleanVar(value=bool(value))
        self.element = ttk.Checkbutton(root, variable=self.var, **kwargs)

class LabelScale(Label):
    def __init__(self, root, label, padx, pady, from_, to_, **kwargs):
        super().__init__(root, label)
        assert to_ > from_, "Slider to value must be greater than from value"
        self.var = tk.DoubleVar(value=0.5)
        self.element = ttk.Scale(root, variable=self.var, from_=from_, to=to_, **kwargs)
        self.element.grid(padx=padx, pady=pady)

class UI():
    def __init__(self, default_preset="Elysium 1"): # "Elysium 1" or "Falcon 9"
        self.preset_names = ["Elysium 1", "Falcon 9"]
        self.presets = [get_elysium_1_preset(), get_falcon_9_preset()]

        if default_preset == "Falcon 9":
            self.preset = 1
        else:
            self.preset = 0

        self.set_rocket()

    def set_rocket(self, *args):
        if hasattr(self, 'labels'):
            self.preset = self.preset_names.index(str(self.labels['preset'].var.get()))
        self.rocket = self.presets[self.preset]
        self.create()
        
    def get_outputs(self):
        ui_outputs = {}

        for key, ui in self.labels.items():
            if hasattr(ui, 'var'):
                var = ui.var
                value = var.get()
                try:
                    index = ui.element.current()
                    values = ui.element.cget('values')
                    assert index < len(values), "Specified dropdown index is outside of range of values provided"
                    value = index
                except:
                    try:
                        # Try to convert the input value to a float
                        value = float(value)
                        if ui.range is not None:
                            value = max(float(ui.range[0]), min(float(ui.range[1]), value))
                    except:
                            try:
                                value = bool(value)
                            except:
                                raise TypeError("Failed to get value from tkinter element")
                ui_outputs[key] = value
        return ui_outputs

    def create_labels(self):
        label_font = ('Helvetica', 12, 'bold')

        self.labels = {
            '0th_label': Label(self.root, "General properties", font=label_font),
            'preset': LabelCombobox(self.root, "IDM Preset:", self.preset, self.preset_names, self.set_rocket, state="readonly", width=17),
            #'dv': LabelEntry(self.root, "Delta V total (m/s):", self.rocket.dv),
            'orbit': LabelCombobox(self.root, "Orbit:", self.rocket.orbit, self.rocket.orbit_options, state="readonly", width=17),
            'payload': LabelEntry(self.root, "Payload (kg):", self.rocket.payload),
            'cd': LabelEntry(self.root, "Drag Coefficient:", self.rocket.cd),
            'mf2': LabelEntry(self.root, "Inert mass fraction 2nd stage:", self.rocket.mf2),
            'isp2': LabelEntry(self.root, "ISP 2nd stage:", self.rocket.isp2),
            
            '1st_label': Label(self.root, "1st stage properties", font=label_font),
            
            'dv_split_slider': LabelScale(self.root, "dV fraction stage 1:", padx=10, pady=10, from_=0, to_=1, orient="horizontal", length=150, command=lambda event: self.update_dv_split()),
            'dv_split': Entry(self.root, self.rocket.dv_split, range=[0, 1]),
            'engine_index': LabelCombobox(self.root, "Engine:", self.rocket.engine_index, self.rocket.engine_options, state="readonly", width=17),
            #"N_engines":LabelEntry(self.root,"Number of Engines:",self.rocket.engine_number),
            'reflights': LabelEntry(self.root, "Number of reflights:", self.rocket.reflights),
            'material_tank': LabelCombobox(self.root, "Material Tank:", self.rocket.material_tank, self.rocket.material_options, state="readonly", width=17),
            'material_misc': LabelCombobox(self.root, "Material Misc:", self.rocket.material_misc, self.rocket.material_options, state="readonly", width=17),
            'bulkhead': LabelCombobox(self.root, "Bulkhead:", self.rocket.bulkhead, self.rocket.bulkhead_options, state="readonly", width=17),
            'pressure_ox': LabelEntry(self.root, "Pressure OX (bar):", self.rocket.pressure_ox),
            'pressure_fuel': LabelEntry(self.root, "Pressure fuel (bar):", self.rocket.pressure_fuel),
            'temperature_ox (80-90K)':  LabelEntry(self.root, "Temperature Ox (K):", self.rocket.temperature_ox),
            'temperature_fuel (95-111K)': LabelEntry(self.root, "Temperature Fuel (K):", self.rocket.temperature_fuel),

            'diameter': LabelEntry(self.root, "Diameter (m):", self.rocket.diameter),
            'of_ratio': LabelEntry(self.root, "O/F ratio:", self.rocket.of_ratio),
            '2nd_label': Label(self.root, "Trajectory simulation", font=label_font),

            'trajectory_timestep': LabelEntry(self.root, "Simulation Timestep (s):", self.rocket.trajectory_timestep, range=[0.001, 1]),
            'trajectory_max_time': LabelEntry(self.root, "Maximum Simulation Time (s):", self.rocket.trajectory_max_time, range=[1, 4000]),

            '3rd_label': Label(self.root, "Ascent properties", font=label_font),

            'number_of_engines_ascent': LabelEntry(self.root, "Number of Engines (ascent):", self.rocket.number_of_engines_ascent, range=[1, 30]),
            'kick_angle': LabelEntry(self.root, "Kick Angle (deg):", self.rocket.kick_angle, range=[0, 90]),
            'kick_time': LabelEntry(self.root, "Kick Time (s):", self.rocket.kick_time, range=[0, 300]),
            'gravity_turn_alt': LabelEntry(self.root, "Gravity Turn Altitude (m):", self.rocket.gravity_turn_alt, range=[0, 30_000]),

            '4th_label': Label(self.root, "Re-entry and landing properties", font=label_font),

            'number_of_engines_reentry': LabelEntry(self.root, "Number of Engines (re-entry):", self.rocket.number_of_engines_reentry, range=[1, 30]),
            'number_of_engines_landing': LabelEntry(self.root, "Number of Engines (landing):", self.rocket.number_of_engines_landing, range=[1, 30]),
            'delta_V_reentry': LabelEntry(self.root, "Delta V (re-entry) (m/s):", self.rocket.delta_V_reentry, range=[0, 10_000]),
            'delta_V_landing': LabelEntry(self.root, "Delta V (landing) (m/s):", self.rocket.delta_V_landing, range=[0, 10_000]),
            'reentry_burn_alt': LabelEntry(self.root, "Re-entry Burn Altitude (m/s):", self.rocket.reentry_burn_alt, range=[0, 200_000]),

            'submit': Button(self.root, columnspan=2, text="Submit")
        }

        for i, key in enumerate(self.labels.keys()):
            if hasattr(self.labels[key], 'label'):
                self.labels[key].label.grid(column=0, row=i)
            if hasattr(self.labels[key], 'element'):
                self.labels[key].element.grid(column=1, row=i)

        self.labels['dv_split'].element.bind("<Return>", lambda event: self.update_dv_split_slider())
        self.labels['submit'].label.bind("<ButtonRelease-1>", lambda event: self.submit_new_rocket())

    def create(self):
        if hasattr(self, 'root'):
            self.root.destroy()
        # if hasattr(self, 'results_root'):
        #     results_root.destroy()
        self.root = tk.Tk()
        self.root.title("Input Screen")

        self.create_labels()

        self.root.mainloop()

    def show_result(self):
        results_root = tk.Tk()
        results_root.title("Output Screen")
        label_font = ('Helvetica', 10, 'bold')
        ttk.Label(results_root, text="Parameter", font = label_font).grid(column=0, row=0, sticky='')
        ttk.Label(results_root, text="Value", font=label_font).grid(column=1, row=0, sticky='e')
        ttk.Label(results_root, text="Certainty", font=label_font).grid(column=2, row=0, sticky='')
        values = [
            [f"-----------General properties------------", "---------------", "---------------"],
            [f"Orbit:", f"{self.rocket.orbit_options[self.rocket.orbit]}", "Input"],
            [f"Payload:", f"{self.rocket.payload} kg", "Input"],
            [f"Drag Coefficient:", f"{self.rocket.cd}", "Input"],
            [f"Delta V total:", f"{self.rocket.dv} m/s", "Margin 10%"],

            [f"--------First-stage properties---------","---------------","---------------"],
            [f"Engine:", self.rocket.engine_options[self.rocket.engine_index], "Input"],
            [f"Number of reflights:", f"{self.rocket.reflights}", "Input"],
            [f"Thrust:", f"{(self.rocket.thrust / 10e6):.1f} MN ", "Margin 40%"],
            [f"Number of Engines:", f"{self.rocket.engine_number}","Margin 40%"],
            [f"Delta V first stage:", f"{(self.rocket.dv_1):.0f} m/s", "Margin 40%"],




            [f"---------Propellant properties---------","---------------","---------------"],
            [f"Pressure:", f"{self.rocket.pressure_ox} bar", "Input"],
            [f"Temperature Ox:", f"{self.rocket.temperature_ox} K", "Input"],
            [f"Temperature Fuel:", f"{self.rocket.temperature_fuel} K", "Input"],
            [f" O/F Ratio:", f"{self.rocket.of_ratio} ", "Input"],
            [f"Propellant Mass:", f"{self.rocket.mass_p:.0f} kg", "Margin 40%"],


            [f"--------Structural properties---------","---------------","---------------"],

            [f"Material:", f"{self.rocket.material_options[self.rocket.material_tank]}", "Input"],
            [f"Bulkhead:", f"{self.rocket.bulkhead_options[self.rocket.bulkhead]}", "Input"],
            [f"Structural Mass:", f"{self.rocket.mass_s:.0f} kg", "Margin 40%"],
            [f"1st Stage Mass:", f"{(self.rocket.mass/1000):.0f} T", "Margin 40%"],
            [f"Upper Stage Mass:", f"{(self.rocket.mass2/1000):.0f} T", "Margin 40%"],
            [f"Total Mass:", f"{((self.rocket.mass2+self.rocket.mass)/1000):.0f} T", "Margin 40%"],

            [f"----------------Cost-----------------","----------------","----------------"],
           # [f"Total Lifetime Cost:", f"{self.rocket.lifetime_cost:.0f} million euros", "Margin 40%"],
            [f"Development Cost:", f"{self.rocket.development_cost:.0f} million euros", "Margin 40%"],
            [f"Production cost per Launch:", f"{self.rocket.production_cost:.0f} million euros", "Margin 40%"],
            [f"Operational cost per Launch:", f"{self.rocket.operational_cost:.0f} million euros", "Margin 40%"],
            [f"Cost Per Launch:", f"{self.rocket.per_launch_cost:.0f} million euros", "Margin 40%"],
            #f"Estimated Cost: €{self.rocket.cost:.0f} "
        ]

        # Dynamically create labels to display each value
        for i, value in enumerate(values):
            i+=1
            ttk.Label(results_root, text=value[0]).grid(column=0, row=i, sticky='')
            ttk.Label(results_root, text=value[1]).grid(column=1, row=i, sticky='e')
            ttk.Label(results_root, text=value[2]).grid(column=2, row=i, sticky='w')
            
        trajectory_plot_button = ttk.Button(results_root, text="Show Trajectory Plots")
        trajectory_plot_button.bind("<ButtonRelease-1>", lambda event: self.create_trajectory_plot())
        trajectory_plot_button.grid(column=0, row=len(values) + 1, pady=10)
        results_root.mainloop()

    def create_trajectory_plot(self):
        fig = self.rocket.trajectory.setup_plot()
        # Create a new Tkinter root window
        new_root = tk.Tk()
        new_root.title("Trajectory Simulation Plots")

        # Create a canvas to embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_root)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, new_root)
        toolbar.update()

        # Pack the canvas and toolbar into the window
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Run the Tkinter main loop for the new window
        new_root.mainloop()

    def update_dv_split(self):
        value = self.labels['dv_split_slider'].var.get()
        # Reduce significant figures for readability
        value = float(f"{value:.3f}")
        self.labels['dv_split'].var.set(value)

    def update_dv_split_slider(self):
        input_box = self.labels['dv_split']
        value = float(self.labels['dv_split'].var.get())
        if input_box.range is not None:
            # Clamp
            value = max(float(input_box.range[0]), min(float(input_box.range[1]), value))
        self.labels['dv_split_slider'].var.set(value)
        self.labels['dv_split'].var.set(value)

    def submit_new_rocket(self):
        outputs = self.get_outputs()
        self.rocket.update_values(**outputs)
        self.rocket.mass_estimation()
        self.rocket.iterate()
        self.show_result()

    def iterate_rocket(self):
        self.rocket.iterate()
        self.show_result()