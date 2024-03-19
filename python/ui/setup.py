import tkinter as tk
from tkinter import ttk

class Label():
    def __init__(self, root, label, font=...):
        self.label = ttk.Label(root, text=label, font=font)
        self.element = None

class LabelEntry(Label):
    def __init__(self, root, label, value, width=20):
        super().__init__(root, label)
        self.element = ttk.Entry(root, textvariable=tk.StringVar(val=value), width=width)

class LabelCombobox(Label):
    def __init__(self, root, label, value, values, width=20, state="readonly"):
        super().__init__(root, label)
        self.element = ttk.Combobox(self.root, textvariable=value, values=values, state=state, width=width)

class UI():
    def __init__(self, rocket):
        self.rocket = rocket
        self.root = tk.Tk()
        # self.input_dict = {}

    def update_value(event):
        # Get the value from the slider
        slider_value = slider.get()
        # Update the value displayed in the input box
        dvs.delete(0, tk.END)
        dvs.insert(0, f"{slider_value:.3f}")

    # def update_slider(event=None):
    #     # Get the value from the input box
    #     input_value = dvs.get()
    #     try:
    #         # Try to convert the input value to a float
    #         value = float(input_value)
    #         # Ensure the value is within the range 0 to 1
    #         value = max(0, min(1, value))
    #         # Update the slider position
    #         slider.set(value)
    #     except ValueError:
    #         # If the input value cannot be converted to a float, do nothing
    #         pass
    def create(self):
        self.root = tk.Tk()
        self.root.title("Input Screen")

        custom_font = ('Helvetica', 12, 'bold')
        ttk.Label(self.root, text="General properties", font=custom_font).grid(column=1, row=i)

        self.labels = {
            'dv': LabelEntry(self.root, "Delta V total (m/s):", self.rocket.dv),
            'orbit': LabelCombobox(self.root, "Orbit:", self.rocket.orbit_options[self.rocket.orbit], self.rocket.orbit_options, 17),
            'payload': LabelEntry(self.root, "Payload (kg):", self.rocket.payload),
            'drag_coeff': LabelEntry(self.root, "Drag Coefficient:", self.rocket.cd),
            'inert_mass': LabelEntry(self.root, "Inert mass fraction 2nd stage:", self.rocket.mf2),
            'isp_2': LabelEntry(self.root, "ISP 2nd stage:", self.rocket.isp2),
            '1_st_label': Label(self.root, "1st stage properties:", custom_font),
            'dv_frac_slider': LabelScale(self.root, "dV fraction stage 1:", 0, 1, "horizontal", 150, command = lambda a, b : a * b)
        }
        
        for i, key in enumerate(self.labels.keys()):
            self.labels[key].label.grid(column=0, row=i)
            e = self.labels[key].element
            if e is not None:
                e.grid(column=1, row=i)

        ttk.Label(self.root, text=).grid(column=0, row=i)
        slider = ttk.Scale(self.root, from_=0, to=1, orient="horizontal", length=150, command=update_value).grid(padx=10, pady=10)

        i += 1
        dvs = ttk.Entry(self.root, textvariable=input_dict["dv_split"])
        #dvs.bind("<Return>", update_slider)
        dvs.grid(column=1, row=i)
        #update_slider()

        i+=1
        ttk.Label(self.root, text="Engine:").grid(column=0, row=i)
        engine_options = ['Prometheus']
        ttk.Combobox(self.root, textvariable=input_dict["engine"], values=engine_options, state="readonly", width=17).grid(column=1, row=i)


        i += 1
        ttk.Label(self.root, text="Inert mass fraction 1st stage").grid(column=0, row=i)
        ttk.Entry(self.root, textvariable=input_dict["mf1"]).grid(column=1, row=i)
        # Boostback
        i += 1
        ttk.Label(self.root, text="Boostback:").grid(column=0, row=i)
        ttk.Checkbutton(self.root, variable=input_dict["boostback"]).grid(column=1, row=i)


        # Material
        i += 1
        ttk.Label(self.root, text="Material Tank:").grid(column=0, row=i)
        material_options = list(m.keys())
        ttk.Combobox(self.root, textvariable=input_dict["material_tank"], values=material_options, state="readonly", width=17
                    ).grid(column=1, row=i)

        input_dict["material_tank"].set(material_options[0])  # default value

        i += 1
        ttk.Label(self.root, text="Material Misc:").grid(column=0, row=i)
        material_options = list(m.keys())
        ttk.Combobox(self.root, textvariable=input_dict["material_misc"], values=material_options, state="readonly", width=17
                    ).grid(column=1, row=i)

        input_dict["material_misc"].set(material_options[0])  # default value

        #Bulkhead
        i += 1
        ttk.Label(self.root, text="Bulkhead:").grid(column=0, row=i)
        bulkhead_options = ['shared', 'separate']
        ttk.Combobox(self.root, textvariable=input_dict["bulkhead"], values=bulkhead_options, state="readonly", width=17
                    ).grid(column=1,row=i)

        # Pressure
        i += 1
        ttk.Label(self.root, text="Pressure OX (bar):").grid(column=0, row=i)
        ttk.Entry(self.root, textvariable=input_dict["pressure_ox"]).grid(column=1, row=i)

        i += 1
        ttk.Label(self.root, text="Pressure fuel (bar):").grid(column=0, row=i)
        ttk.Entry(self.root, textvariable=input_dict["pressure_fuel"]).grid(column=1, row=i)

        i += 1
        ttk.Label(self.root, text="Diameter (m):").grid(column=0, row=i)
        ttk.Entry(self.root, textvariable=input_dict["diameter"]).grid(column=1, row=i)

        i += 1
        ttk.Label(self.root, text="O/F ratio :").grid(column=0, row=i)
        ttk.Entry(self.root, textvariable=input_dict["OF_ratio"]).grid(column=1, row=i)


        # Submit button (Example action, customize as needed)
        i+=1
        ttk.Button(self.root, text="Submit", command= lambda: make_rocket(input_dict)).grid(column=0, row=i, columnspan=2)

        self.root.mainloop()

    def show_result(self):
        values = [
            f"Engine: {self.engine} N",
            f"Delta V: {self.dv} m/s",
            f"Boostback: {self.boostback}",
            f"Orbit: {self.orbit}",
            f"Payload: {self.payload} kg",
            f"Drag Coefficient: {self.cd}",
            f"Material: {self.material_tank}",
            #f"Bulkhead: {self.bulkhead}",
            f"Pressure: {self.pressure_ox} bar",
            f"Structural Mass: {self.mass_s:.0f} kg",
            f"Propellant Mass: {self.mass_p:.0f} kg",
            f"Upper Stage Mass: {self.mass2:.0f} kg",
            f"Estimated Cost: €{self.cost:.0f} "
        ]

        # Dynamically create labels to display each value
        for i, value in enumerate(values):
            ttk.Label(self.self.root, text=value).grid(column=0, row=i, sticky='w')

        fig = self.trajectory.fig
        canvas = FigureCanvasTkAgg(fig, master=self.self.root)
        canvas_widget = canvas.get_tk_widget()

        # Place the canvas within the Tkinter window
        canvas_widget.grid(row=i+1, column=0, sticky="nsew")

        iterate_button = ttk.Button(self.self.root, text="Iterate", command= self.iterate)
        iterate_button.grid(column=0, row=len(values) + 1, pady=10)
        self.self.root.mainloop()