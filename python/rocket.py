#from aerodynamics.aerodynamics import Aerodynamics
#from control.control import Control

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory import Trajectory
import tkinter as tk
from tkinter import ttk
from python.structure.materials import materials as m
from python.cost_model import MassCalculator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Rocket():
    def __init__(self, input_dict):

        self.engine = input_dict["engine"].get()
        self.dv = float(input_dict["dv"].get())
        self.boostback = input_dict["boostback"].get()
        self.orbit = input_dict["orbit"].get()
        self.payload = float(input_dict["payload"].get())
        self.cd = float(input_dict["cd"].get())
        self.material_tank = input_dict["material_tank"].get()
        self.material_misc = input_dict["material_misc"].get()
        self.bulkhead = input_dict["bulkhead"].get()
        self.pressure_ox = float(input_dict["pressure_ox"].get())
        self.pressure_fuel = float(input_dict["pressure_fuel"].get())
        self.diameter = float(input_dict["diameter"].get())
        self.OF_ratio = float(input_dict["OF_ratio"].get())
        dv1 = float(input_dict["dv_split"].get())
        self.dv_split = [dv1, 1-dv1]
        self.root = None
        print(f"Engine: {self.engine}")
        print(f"Delta V: {self.dv} m/s")
        print(f"Boostback: {self.boostback}")
        print(f"Orbit: {self.orbit}")
        print(f"Payload: {self.payload} kg")
        print(f"Drag Coefficient: {self.cd}")
        print(f"Material: {self.material_tank}")
        #print(f"Bulkhead: {self.bulkhead}")
        print(f"Pressure: {self.pressure_ox} bar")


        #self.aerodynamics = Aerodynamics()
        #self.control = Control()
        self.propulsion = Propulsion(self.engine)
        self.structure = Structure(self.diameter/2, self.material_tank, self.pressure_ox, self.pressure_fuel, self.material_misc)
        self.trajectory = Trajectory(self.orbit, self.payload, self.cd)

     
    def mass_estimation(self):
        self.mass_s = 100000 # kg
        self.mass_p = 600000 #kg
        self.mass = self.mass_s + self.mass_p
        mass_estimator = MassCalculator()
        wet_masses = mass_estimator.get_wet_masses(self.dv, self.dv_split, inert_mass_fractions, self.propulsion.Isp, self.payload)
        prop_masses = mass_estimator.get_propellant_masses(wet_masses, inert_mass_fractions)
        dry_masses = mass_estimator.get_dry_masses(wet_masses, inert_mass_fractions)
    def cost_estimator(self):
        return self.mass * 25.00 #placeholder
    def iterate(self):

        self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass,  self.dv)
        self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = (
            self.propulsion.mass_volume(self.thrust, self.burntime, self.OF_ratio))
        self.mass_p = self.mass_ox + self.mass_fuel
        self.structure.calc(self.volume_ox, self.mass_ox, self.volume_fuel, self.mass_fuel, self.thrust)
        self.mass_t = self.structure.mass_total_tank
        self.mass_es = self.structure.mass_engine_structure(self.engine_number, self.thrust)
        self.mass_lg = self.structure.mass_landing_gear(self.mass_e, self.mass_p, self.mass_t, self.mass_es)
        self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
        self.mass = self.mass_p + self.mass_s

        self.cost = self.cost_estimator()

        self.show_result()
    def show_result(self):
        if self.root == None:
            self.root = tk.Tk()
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
            f"Estimated cost: €{self.cost:.0f} "
        ]

        # Dynamically create labels to display each value
        for i, value in enumerate(values):
            ttk.Label(self.root, text=value).grid(column=0, row=i, sticky='w')

        fig = self.trajectory.fig
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = canvas.get_tk_widget()

        # Place the canvas within the Tkinter window
        canvas_widget.grid(row=i+1, column=0, sticky="nsew")

        iterate_button = ttk.Button(self.root, text="Iterate", command= self.iterate)
        iterate_button.grid(column=0, row=len(values) + 1, pady=10)
        self.root.mainloop()
def make_rocket(input_dict):
    r = Rocket(input_dict)
    r.mass_estimation()
    r.iterate()

def update_value(event):
    # Get the value from the slider
    slider_value = slider.get()
    # Update the value displayed in the input box
    dvs.delete(0, tk.END)
    dvs.insert(0, f"{slider_value:.3f}")


def update_slider(event=None):
    # Get the value from the input box
    input_value = dvs.get()
    try:
        # Try to convert the input value to a float
        value = float(input_value)
        # Ensure the value is within the range 0 to 1
        value = max(0, min(1, value))
        # Update the slider position
        slider.set(value)
    except ValueError:
        # If the input value cannot be converted to a float, do nothing
        pass


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Input Screen")
    input_dict = {}
    i = 0
    ttk.Label(root, text="Engine:").grid(column=0, row=i)
    input_dict["engine"] = tk.StringVar()
    engine_options = ['Prometheus']
    ttk.Combobox(root, textvariable=input_dict["engine"], values=engine_options, state="readonly").grid(column=1, row=i)

    input_dict["engine"].set("Prometheus")  # default value
    i += 1
    # Delta V
    ttk.Label(root, text="Delta V total (m/s):").grid(column=0, row=i)
    input_dict["dv"] = tk.StringVar(value='3000')
    ttk.Entry(root, textvariable=input_dict["dv"]).grid(column=1, row=i)

    # Boostback
    i += 1
    ttk.Label(root, text="Boostback:").grid(column=0, row=i)
    input_dict["boostback"] = tk.BooleanVar(value=False)
    ttk.Checkbutton(root, variable=input_dict["boostback"]).grid(column=1, row=i)

    # Orbit
    i += 1
    ttk.Label(root, text="Orbit:").grid(column=0, row=i)
    input_dict["orbit"] = tk.StringVar()
    orbit_options = ['LEO', 'MEO', 'GEO', 'HEO']
    ttk.Combobox(root, textvariable=input_dict["orbit"], values=orbit_options, state="readonly").grid(column=1, row=i)
    input_dict["orbit"].set("LEO")  # default value

    # Payload
    i += 1
    ttk.Label(root, text="Payload (kg):").grid(column=0, row=i)
    input_dict["payload"]= tk.StringVar(value='20000')
    ttk.Entry(root, textvariable=input_dict["payload"]).grid(column=1, row=i)

    # Drag Coefficient
    i += 1
    ttk.Label(root, text="Drag Coefficient:").grid(column=0, row=i)
    input_dict["cd"] = tk.StringVar(value='0.2')
    ttk.Entry(root, textvariable=input_dict["cd"]).grid(column=1, row=i)

    # Material
    i += 1
    ttk.Label(root, text="Material Tank:").grid(column=0, row=i)
    input_dict["material_tank"] = tk.StringVar()
    material_options = list(m.keys())
    ttk.Combobox(root, textvariable=input_dict["material_tank"], values=material_options, state="readonly").grid(column=1, row=i)

    input_dict["material_tank"].set(material_options[0])  # default value

    i += 1
    ttk.Label(root, text="Material Misc:").grid(column=0, row=i)
    input_dict["material_misc"] = tk.StringVar()
    material_options = list(m.keys())
    ttk.Combobox(root, textvariable=input_dict["material_misc"], values=material_options, state="readonly").grid(column=1, row=i)

    input_dict["material_misc"].set(material_options[0])  # default value

    #Bulkhead
    i += 1
    ttk.Label(root, text="Bulkhead:").grid(column=0, row=i)
    input_dict["bulkhead"] = tk.StringVar()
    bulkhead_options = ['shared', 'separate']
    ttk.Combobox(root, textvariable=input_dict["bulkhead"], values=bulkhead_options, state="readonly").grid(column=1,row=i)

    input_dict["bulkhead"].set("shared")  # default value

    # Pressure
    i += 1
    ttk.Label(root, text="Pressure OX (bar):").grid(column=0, row=i)
    input_dict["pressure_ox"] = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=input_dict["pressure_ox"]).grid(column=1, row=i)

    i += 1
    ttk.Label(root, text="Pressure fuel (bar):").grid(column=0, row=i)
    input_dict["pressure_fuel"] = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=input_dict["pressure_fuel"]).grid(column=1, row=i)

    i += 1
    ttk.Label(root, text="Diameter (m):").grid(column=0, row=i)
    input_dict["diameter"] = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=input_dict["diameter"]).grid(column=1, row=i)

    i += 1
    ttk.Label(root, text="O/F ratio :").grid(column=0, row=i)
    input_dict["OF_ratio"] = tk.StringVar(value='3.5')
    ttk.Entry(root, textvariable=input_dict["OF_ratio"]).grid(column=1, row=i)

    # dV_fraction slider
    i += 1
    ttk.Label(root, text="dV fraction stage 1:").grid(column=0, row=i)
    slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", length=200, command=update_value)
    slider.grid(row=i, column=1, padx=10, pady=10)

    # Create an input box
    i += 1
    #input_box = ttk.Entry(root)
    #input_box.grid(row=i, column=1, padx=10, pady=5)


    input_dict["dv_split"] = tk.StringVar(value='0.5')
    dvs = ttk.Entry(root, textvariable=input_dict["dv_split"])
    dvs.bind("<Return>", update_slider)
    dvs.grid(column=1, row=i)
    update_slider()

    # Submit button (Example action, customize as needed)
    i+=1
    ttk.Button(root, text="Submit", command= lambda: make_rocket(input_dict)).grid(column=0, row=i, columnspan=2)

    root.mainloop()









