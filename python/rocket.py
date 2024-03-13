from aerodynamics.aerodynamics import Aerodynamics
#from control.control import Control
#from python.propulsion.propulsion import Propulsion
#from structure.structure import Structure
#from trajectory.trajectory import Trajectory
import tkinter as tk
from tkinter import ttk

class Rocket():
    def __init__(self):
        root = tk.Tk()
        root.title("Input Screen")

        # Engine Thrust
        ttk.Label(root, text="Engine Thrust (N):").grid(column=0, row=0)
        engine_thrust = tk.StringVar(value='1000000')
        ttk.Entry(root, textvariable=engine_thrust).grid(column=1, row=0)

        # ISP
        ttk.Label(root, text="ISP:").grid(column=0, row=1)
        ISP = tk.StringVar(value='350')
        ttk.Entry(root, textvariable=ISP).grid(column=1, row=1)

        # Delta V
        ttk.Label(root, text="Delta V 1st stage (m/s):").grid(column=0, row=2)
        dv = tk.StringVar(value='3000')
        ttk.Entry(root, textvariable=dv).grid(column=1, row=2)

        # Boostback
        ttk.Label(root, text="Boostback:").grid(column=0, row=3)
        boostback = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, variable=boostback).grid(column=1, row=3)

        # Orbit
        ttk.Label(root, text="Orbit:").grid(column=0, row=4)
        orbit = tk.StringVar()
        orbit_options = ['LEO', 'MEO', 'GEO', 'HEO']
        ttk.Combobox(root, textvariable=orbit, values=orbit_options, state="readonly").grid(column=1, row=4)
        orbit.set("LEO")  # default value

        # Payload
        ttk.Label(root, text="Payload (kg):").grid(column=0, row=5)
        payload = tk.StringVar(value='20000')
        ttk.Entry(root, textvariable=payload).grid(column=1, row=5)

        # Drag Coefficient
        ttk.Label(root, text="Drag Coefficient:").grid(column=0, row=6)
        cd = tk.StringVar(value='0.2')
        ttk.Entry(root, textvariable=cd).grid(column=1, row=6)

        # Material
        ttk.Label(root, text="Material:").grid(column=0, row=7)
        material = tk.StringVar()
        material_options = ['steel', 'aluminum', 'titanium']
        ttk.Combobox(root, textvariable=material, values=material_options, state="readonly").grid(column=1,
                                                                                                           row=7)
        material.set("steel")  # default value

        # Bulkhead
        ttk.Label(root, text="Bulkhead:").grid(column=0, row=8)
        bulkhead = tk.StringVar()
        bulkhead_options = ['shared', 'separate']
        ttk.Combobox(root, textvariable=bulkhead, values=bulkhead_options, state="readonly").grid(column=1,
                                                                                                           row=8)
        bulkhead.set("shared")  # default value

        # Pressure
        ttk.Label(root, text="Pressure (bar):").grid(column=0, row=9)
        pressure = tk.StringVar(value='5')
        ttk.Entry(root, textvariable=pressure).grid(column=1, row=9)

        # Submit button (Example action, customize as needed)
        ttk.Button(root, text="Submit", command=root.destroy).grid(column=0, row=10, columnspan=2)
        root.mainloop()

        self.engine_thrust = engine_thrust.get()
        self.ISP = ISP.get()
        self.dv = dv.get()
        self.boostback = boostback.get()
        self.orbit = orbit.get()
        self.payload = payload.get()
        self.cd = float(cd.get())
        self.material = material.get()
        self.bulkhead = bulkhead.get()
        self.pressure = pressure.get()

        print(f"Engine Thrust: {self.engine_thrust} N")
        print(f"ISP: {self.ISP}")
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
        #self.propulsion = Propulsion()
        #self.structure = Structure()
        #self.trajectory = Trajectory()


    # TEMP
    def print_inputs(self):
        print("Inputs:")
        print("Aerodynamics:", self.aerodynamics.input)
        print("Control:", self.control.input)
        print("Propulsion:", self.propulsion.input)
        print("Structure:", self.structure.input)
        print("Trajectory:", self.trajectory.input)

    # TEMP
    def print_outputs(self):
        print("Outputs:")
        print("Aerodynamics:", self.aerodynamics.output)
        print("Control:", self.control.output)
        print("Propulsion:", self.propulsion.output)
        print("Structure:", self.structure.output)
        print("Trajectory:", self.trajectory.output)
     
    def mass_estimation(self):
        self.mass_s = 100000 # kg
        self.mass_p = 600000 #kg

    def cost_estimator(self):
        pass
    def iterate(self):
        try:
            self.root.destroy()
        except: pass
        #self.trust, self.burntime = self.trajectory.FUNCTION(self.cd, self.mass_p, self.mass_s, self.dv, self.engine_thrust)
        #self.mass_e, self.mass_p, self.volume_p, self.engine_number = self.propulsion.FUNCTION(self.engine_trust, self.ISP, self.trust, self.burntime)
        #self.mass_t = self.structure.TANKDESIGNFUNCTION(self.mass_p, self.volume_p)
        #self.mass_es = self.structure.ENGINEDESIGNFUNCTION(self.engine_number, self.engine_thrust)
        #self.mass_lg = self.structure.LGDESIGNFUNCTION(self.mass_e, self.mass_p, self.mass_t, self.mass_es)
        #self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t

        self.show_result()
    def show_result(self):
        self.root = tk.Tk()
        values = [
            f"Engine Thrust: {self.engine_thrust} N",
            f"ISP: {self.ISP}",
            f"Delta V: {self.dv} m/s",
            f"Boostback: {self.boostback}",
            f"Orbit: {self.orbit}",
            f"Payload: {self.payload} kg",
            f"Drag Coefficient: {self.cd}",
            f"Material: {self.material}",
            f"Bulkhead: {self.bulkhead}",
            f"Pressure: {self.pressure} bar",
            f"Structural Mass: {self.mass_s} kg"
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





