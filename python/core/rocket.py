#from aerodynamics.aerodynamics import Aerodynamics
#from control.control import Control
import numpy as np

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory import Trajectory
from python.structure.materials import materials as m
from python.cost_model import MassCalculator
from python.cost_model import Costmodel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Rocket():
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.root = tk.Tk()

        #self.aerodynamics = Aerodynamics()
        #self.control = Control()
        self.propulsion = Propulsion(self.engine, self.OF_ratio)
        self.structure = Structure(self.diameter / 2, self.material_tank, self.pressure_ox, self.pressure_fuel, self.material_misc)
        self.trajectory = Trajectory(self.orbit, self.payload, self.cd)

     
    def mass_estimation(self):
        mass_estimator = MassCalculator()
        wet_masses = mass_estimator.get_wet_masses(self.dv, self.dv_split, [self.mf1, self.mf2],
                                                   [self.propulsion.Isp, self.isp2], self.payload)
        self.mass_p, self.mass_p2 = mass_estimator.get_propellant_masses(wet_masses, [self.mf1, self.mf2])
        self.mass_s, self.mass_s2  = mass_estimator.get_dry_masses(wet_masses, [self.mf1, self.mf2])
        self.mass = self.mass_s + self.mass_p
        self.mass2 = self.mass_p2 + self.mass_s2

    def cost_estimator(self):
        cost_calc = Costmodel(np.array([self.mass_s,self.mass_s2]), np.array([self.mass_p,self.mass_p2]))
        cost_per_launch = cost_calc.get_cost_per_launch()
        return cost_per_launch
    
    def iterate(self):

        self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass,  self.dv)
        self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = (
            self.propulsion.mass_volume(self.thrust, self.burntime))
        self.mass_p = self.mass_ox + self.mass_fuel
        self.structure.calc(self.volume_ox, self.mass_ox, self.volume_fuel, self.mass_fuel, self.thrust)
        self.mass_t = self.structure.mass_total_tank
        self.mass_es = self.structure.mass_engine_structure(self.engine_number, self.thrust)
        self.mass_lg = self.structure.mass_landing_gear(self.mass_e, self.mass_p, self.mass_t, self.mass_es)
        self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
        self.mass = self.mass_p + self.mass_s

        self.cost = self.cost_estimator()

        self.show_result()

if __name__ == "__main__":




    r = Rocket(input_dict)
    r.mass_estimation()
    r.iterate()









