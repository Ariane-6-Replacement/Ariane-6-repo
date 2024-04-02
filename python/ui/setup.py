import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

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
    def __init__(self, root, label, value_index, values, **kwargs):
        super().__init__(root, label)
        assert value_index < len(values), "Specified dropdown index is outside of range of values provided"
        self.var = tk.StringVar(value=str(values[value_index]))
        self.element = ttk.Combobox(root, textvariable=self.var, values=values, **kwargs)

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
    def __init__(self, rocket):
        self.rocket = rocket
        
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

    def create(self):
        self.root = tk.Tk()
        self.root.title("Input Screen")

        label_font = ('Helvetica', 12, 'bold')

        self.labels = {
            '0th_label': Label(self.root, "General properties", font=label_font),
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
            'submit': Button(self.root, columnspan=2, text="Submit")
        }
        
        for i, key in enumerate(self.labels.keys()):
            if hasattr(self.labels[key], 'label'):
                self.labels[key].label.grid(column=0, row=i)
            if hasattr(self.labels[key], 'element'):
                self.labels[key].element.grid(column=1, row=i)

        self.labels['dv_split'].element.bind("<Return>", lambda event: self.update_dv_split_slider())
        self.labels['submit'].label.bind("<ButtonRelease-1>", lambda event: self.submit_new_rocket())

        self.root.mainloop()

    def show_result(self):
        root = tk.Tk()
        root.title("Output Screen")
        label_font = ('Helvetica', 10, 'bold')
        ttk.Label(root, text="Parameter", font = label_font).grid(column=0, row=0, sticky='')
        ttk.Label(root, text="Value", font=label_font).grid(column=1, row=0, sticky='e')
        ttk.Label(root, text="Certainty", font=label_font).grid(column=2, row=0, sticky='')
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
            [f"Upper Stage Mass:", f"{(self.rocket.mass2/1000):.0f} kg", "Margin 40%"],
            [f"Total Mass:", f"{((self.rocket.mass2+self.rocket.mass)/1000):.0f} kg", "Margin 40%"],

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
            ttk.Label(root, text=value[0]).grid(column=0, row=i, sticky='')
            ttk.Label(root, text=value[1]).grid(column=1, row=i, sticky='e')
            ttk.Label(root, text=value[2]).grid(column=2, row=i, sticky='w')

        fig = self.rocket.trajectory.fig
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()

        # Place the canvas within the Tkinter window
        canvas_widget.grid(column=0, row=len(values)+1, columnspan = 3, sticky="")

        #iterate_button = ttk.Button(root, text="Iterate")
        #iterate_button.bind("<ButtonRelease-1>", lambda event: self.iterate_rocket())
        #iterate_button.grid(column=0, row=len(values) + 1, pady=10)
        plt.close()
        root.mainloop()

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