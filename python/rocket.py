#from aerodynamics.aerodynamics import Aerodynamics
#from control.control import Control

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory import Trajectory
import tkinter as tk
from tkinter import ttk
from python.structure.materials import materials as m


class Rocket():
    def __init__(self, engine, dv, boostback, orbit, payload, cd, material_tank, material_misc, pressure_ox,
                 pressure_fuel, diameter):

        self.engine = engine.get()
        self.dv = float(dv.get())
        self.boostback = boostback.get()
        self.orbit = orbit.get()
        self.payload = float(payload.get())
        self.cd = float(cd.get())
        self.material_tank = material_tank.get()
        self.material_misc = material_misc.get()
        # self.bulkhead = bulkhead.get()
        self.pressure_ox = float(pressure_ox.get())
        self.pressure_fuel = float(pressure_fuel.get())
        self.diameter = float(diameter.get())

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
    def cost_estimator(self):
        return self.mass * 25.00 #placeholder
    def iterate(self):
        try:
            self.root.destroy()
        except: pass
        self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass,  self.dv)
        self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = self.propulsion.mass_volume(self.thrust, self.burntime)
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
            f"Estimated cost: {self.cost:.0f} €"
        ]

        # Dynamically create labels to display each value
        for i, value in enumerate(values):
            ttk.Label(self.root, text=value).grid(column=0, row=i, sticky='w')

        iterate_button = ttk.Button(self.root, text="Iterate", command= self.iterate)
        iterate_button.grid(column=0, row=len(values) + 1, pady=10)
        self.root.mainloop()
def make_rocket(engine, dv, boostback, orbit, payload, cd, material_tank, material_misc, pressure_ox,
                 pressure_fuel, diameter):
    r = Rocket(engine, dv, boostback, orbit, payload, cd, material_tank, material_misc, pressure_ox,
                 pressure_fuel, diameter)
    r.mass_estimation()
    r.iterate()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Input Screen")
    i = 0
    ttk.Label(root, text="Engine:").grid(column=0, row=i)
    engine = tk.StringVar()
    engine_options = ['Prometheus']
    ttk.Combobox(root, textvariable=engine, values=engine_options, state="readonly").grid(column=1, row=i)

    engine.set("Prometheus")  # default value
    i += 1
    # Delta V
    ttk.Label(root, text="Delta V 1st stage (m/s):").grid(column=0, row=i)
    dv = tk.StringVar(value='3000')
    ttk.Entry(root, textvariable=dv).grid(column=1, row=i)

    # Boostback
    i += 1
    ttk.Label(root, text="Boostback:").grid(column=0, row=i)
    boostback = tk.BooleanVar(value=False)
    ttk.Checkbutton(root, variable=boostback).grid(column=1, row=i)

    # Orbit
    i += 1
    ttk.Label(root, text="Orbit:").grid(column=0, row=i)
    orbit = tk.StringVar()
    orbit_options = ['LEO', 'MEO', 'GEO', 'HEO']
    ttk.Combobox(root, textvariable=orbit, values=orbit_options, state="readonly").grid(column=1, row=i)
    orbit.set("LEO")  # default value

    # Payload
    i += 1
    ttk.Label(root, text="Payload (kg):").grid(column=0, row=i)
    payload = tk.StringVar(value='20000')
    ttk.Entry(root, textvariable=payload).grid(column=1, row=i)

    # Drag Coefficient
    i += 1
    ttk.Label(root, text="Drag Coefficient:").grid(column=0, row=i)
    cd = tk.StringVar(value='0.2')
    ttk.Entry(root, textvariable=cd).grid(column=1, row=i)

    # Material
    i += 1
    ttk.Label(root, text="Material Tank:").grid(column=0, row=i)
    material_tank = tk.StringVar()
    material_options = list(m.keys())
    ttk.Combobox(root, textvariable=material_tank, values=material_options, state="readonly").grid(column=1, row=i)

    material_tank.set(material_options[0])  # default value
    i += 1
    ttk.Label(root, text="Material Misc:").grid(column=0, row=i)
    material_misc = tk.StringVar()
    material_options = list(m.keys())
    ttk.Combobox(root, textvariable=material_misc, values=material_options, state="readonly").grid(column=1, row=i)

    material_misc.set(material_options[0])  # default value

    # Bulkhead
    # i += 1
    # ttk.Label(root, text="Bulkhead:").grid(column=0, row=i)
    ##bulkhead = tk.StringVar()
    # bulkhead_options = ['shared', 'separate']
    # ttk.Combobox(root, textvariable=bulkhead, values=bulkhead_options, state="readonly").grid(column=1,row=i)

    # bulkhead.set("shared")  # default value

    # Pressure
    i += 1
    ttk.Label(root, text="Pressure OX (bar):").grid(column=0, row=i)
    pressure_ox = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=pressure_ox).grid(column=1, row=i)

    i += 1
    ttk.Label(root, text="Pressure fuel (bar):").grid(column=0, row=i)
    pressure_fuel = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=pressure_fuel).grid(column=1, row=i)

    i += 1
    ttk.Label(root, text="Diameter (m):").grid(column=0, row=i)
    diameter = tk.StringVar(value='5')
    ttk.Entry(root, textvariable=diameter).grid(column=1, row=i)

    i += 1
    # Submit button (Example action, customize as needed)

    ttk.Button(root, text="Submit", command= lambda: make_rocket(engine, dv, boostback, orbit, payload, cd, material_tank, material_misc, pressure_ox,
                 pressure_fuel, diameter)).grid(column=0, row=i, columnspan=2)

    root.mainloop()
    engine = engine.get()
    dv = float(dv.get())
    boostback = boostback.get()
    orbit = orbit.get()
    payload = float(payload.get())
    cd = float(cd.get())
    material_tank = material_tank.get()
    material_misc = material_misc.get()
    # self.bulkhead = bulkhead.get()
    pressure_ox = float(pressure_ox.get())
    pressure_fuel = float(pressure_fuel.get())
    diameter = float(diameter.get())








