#from aerodynamics.aerodynamics import Aerodynamics
#from control.control import Control

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory import Trajectory
import tkinter as tk
from tkinter import ttk

class Rocket():
    def __init__(self):
        root = tk.Tk()
        root.title("Input Screen")

        ttk.Label(root, text="Engine:").grid(column=0, row=0)
        engine = tk.StringVar()
        engine_options = ['Prometheus']
        ttk.Combobox(root, textvariable=engine, values=engine_options, state="readonly").grid(column=1, row=0)

        engine.set("Prometheus")  # default value

        # Delta V
        ttk.Label(root, text="Delta V 1st stage (m/s):").grid(column=0, row=1)
        dv = tk.StringVar(value='3000')
        ttk.Entry(root, textvariable=dv).grid(column=1, row=1)

        # Boostback
        ttk.Label(root, text="Boostback:").grid(column=0, row=2)
        boostback = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, variable=boostback).grid(column=1, row=2)

        # Orbit
        ttk.Label(root, text="Orbit:").grid(column=0, row=3)
        orbit = tk.StringVar()
        orbit_options = ['LEO', 'MEO', 'GEO', 'HEO']
        ttk.Combobox(root, textvariable=orbit, values=orbit_options, state="readonly").grid(column=1, row=3)
        orbit.set("LEO")  # default value

        # Payload
        ttk.Label(root, text="Payload (kg):").grid(column=0, row=4)
        payload = tk.StringVar(value='20000')
        ttk.Entry(root, textvariable=payload).grid(column=1, row=4)

        # Drag Coefficient
        ttk.Label(root, text="Drag Coefficient:").grid(column=0, row=5)
        cd = tk.StringVar(value='0.2')
        ttk.Entry(root, textvariable=cd).grid(column=1, row=5)

        # Material
        ttk.Label(root, text="Material:").grid(column=0, row=6)
        material = tk.StringVar()
        material_options = ['steel', 'aluminum', 'composites']
        ttk.Combobox(root, textvariable=material, values=material_options, state="readonly").grid(column=1, row=6)

        material.set("steel")  # default value

        # Bulkhead
        ttk.Label(root, text="Bulkhead:").grid(column=0, row=7)
        bulkhead = tk.StringVar()
        bulkhead_options = ['shared', 'separate']
        ttk.Combobox(root, textvariable=bulkhead, values=bulkhead_options, state="readonly").grid(column=1,row=7)

        bulkhead.set("shared")  # default value

        # Pressure
        ttk.Label(root, text="Pressure (bar):").grid(column=0, row=8)
        pressure = tk.StringVar(value='5')
        ttk.Entry(root, textvariable=pressure).grid(column=1, row=8)

        ttk.Label(root, text="Diameter (m):").grid(column=0, row=9)
        diameter = tk.StringVar(value='5')
        ttk.Entry(root, textvariable=diameter).grid(column=1, row=9)

        # Submit button (Example action, customize as needed)
        ttk.Button(root, text="Submit", command=root.destroy).grid(column=0, row=10, columnspan=2)
        root.mainloop()

        self.engine = engine.get()
        self.dv = float(dv.get())
        self.boostback = boostback.get()
        self.orbit = orbit.get()
        self.payload = float(payload.get())
        self.cd = float(cd.get())
        self.material = material.get()
        self.bulkhead = bulkhead.get()
        self.pressure = float(pressure.get())
        self.diameter = float(diameter.get())

        print(f"Engine: {self.engine} N")
        print(f"Delta V: {self.dv} m/s")
        print(f"Boostback: {self.boostback}")
        print(f"Orbit: {self.orbit}")
        print(f"Payload: {self.payload} kg")
        print(f"Drag Coefficient: {self.cd}")
        print(f"Material: {self.material}")
        print(f"Bulkhead: {self.bulkhead}")
        print(f"Pressure: {self.pressure} bar")


        #self.aerodynamics = Aerodynamics()
        #self.control = Control()
        self.propulsion = Propulsion(self.engine)
        #self.structure = Structure()
        self.trajectory = Trajectory(self.orbit, self.payload, self.cd)

     
    def mass_estimation(self):
        self.mass_s = 100000 # kg
        self.mass_p = 600000 #kg
        self.mass = self.mass_s + self.mass_p
    def cost_estimator(self):
        return self.mass * 2500 #placeholder
    def iterate(self):
        try:
            self.root.destroy()
        except: pass
        self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass,  self.dv)
        self.mass_e, self.mass_p, self.volume_p, self.engine_number = self.propulsion.mass_volume(self.thrust, self.burntime)

        self.structure = Structure(self.pressure, self.material, self.volume_p, self.thrust, self.diameter)

        self.mass_t = self.structure.mass_total_tank
        self.mass_es = self.structure.mass_engine_structure(self.engine_number, self.thrust)
        self.mass_lg = self.structure.mass_landing_gear(self.mass_e, self.mass_p, self.mass_t, self.mass_es)
        self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
        self.mass = self.mass_p + self.mass_s

        self.cost = self.cost_estimator()

        self.show_result()
    def show_result(self):
        self.root = tk.Tk()
        values = [
            f"Engine: {self.engine} N",
            f"Delta V: {self.dv} m/s",
            f"Boostback: {self.boostback}",
            f"Orbit: {self.orbit}",
            f"Payload: {self.payload} kg",
            f"Drag Coefficient: {self.cd}",
            f"Material: {self.material}",
            f"Bulkhead: {self.bulkhead}",
            f"Pressure: {self.pressure} bar",
            f"Structural Mass: {self.mass_s} kg"
            f"Propellant Mass: {self.mass_p} kg"
            f"Estimated cost: {self.cost} €"
        ]

        # Dynamically create labels to display each value
        for i, value in enumerate(values):
            ttk.Label(self.root, text=value).grid(column=0, row=i, sticky='w')

        # Add an "Iterate" button that currently does nothing when clicked
        # You can define its functionality based on your needs
        iterate_button = ttk.Button(self.root, text="Iterate", command= self.iterate)
        iterate_button.grid(column=0, row=len(values) + 1, pady=10)
        self.root.mainloop()

if __name__ == "__main__":
    r = Rocket()
    r.mass_estimation()
    r.iterate()





