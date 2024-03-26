
import numpy as np

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory import Trajectory
from python.cost.model import MassCalculator
from python.cost.model import CostModel

class Rocket():
    def __init__(self, **kwargs):
        self.update_values(**kwargs)

    def update_values(self, **kwargs):
        print(f"{kwargs}")
        self.__dict__.update(**kwargs)
        #self.aerodynamics = Aerodynamics()
        #self.control = Control()

        self.propulsion = Propulsion(self.engine_options[self.engine], self.of_ratio, self.pressure_ox,self.pressure_fuel)
        self.structure = Structure(self.diameter / 2, self.material_options[self.material_tank], self.pressure_ox, self.pressure_fuel, self.material_options[self.material_misc])
        self.trajectory = Trajectory(self.orbit_options[self.orbit], self.payload, self.cd)

    def mass_estimation(self):
        self.inert_mass_fractions = np.array([self.mf1, self.mf2])
        self.ISPs = np.array([self.propulsion.Isp, self.isp2])

        # All outputs in tonnes

        self.wet_masses = MassCalculator.get_wet_masses(self.dv, self.dv_split, self.inert_mass_fractions, self.ISPs, self.payload)
        self.prop_masses = MassCalculator.get_propellant_masses(self.wet_masses, self.inert_mass_fractions)
        self.dry_masses  = MassCalculator.get_dry_masses(self.wet_masses, self.inert_mass_fractions)

        # Convert tonnes to kg
        self.mass, self.mass2 = self.wet_masses * 1000
        self.mass_prev = self.mass
    def cost_estimator(self):
        cm = CostModel()

        cm.calculate(self.dry_masses, self.prop_masses)
        return cm.cost.total_lifetime_euros, cm.cost.per_launch_euros
    
    def iterate(self):
        e = 10e9
        i = 0
        while e > 50000:
            self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass, self.dv)
            self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = (
                self.propulsion.mass_volume(self.thrust, self.burntime, self.temperature_fuel, self.temperature_ox,
                                            self.pressure_ox, self.pressure_fuel))
            self.mass_p = self.mass_ox + self.mass_fuel
            self.structure.calc(self.bulkhead_options[self.bulkhead], self.volume_ox, self.mass_ox, self.volume_fuel,
                                self.mass_fuel, self.thrust)
            self.mass_t = self.structure.mass_total #Returns mass of the tank/s ITS/s and engine bay
            self.mass_es = self.structure.mass_engine_structure(self.engine_number, self.thrust)
            self.mass_lg = self.structure.mass_landing_gear(self.mass_e, self.mass_p, self.mass_t, self.mass_es)
            self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
            self.mass = self.mass_p + self.mass_s
            e = np.abs(self.mass - self.mass_prev)
            i += 1
            self.mass_prev = self.mass
            print(f"Iterated! Mass = {self.mass:.0f}, e = {e:.0f}")
            if i >= 100:
                print(f"Non convergence!")
                break
        self.lifetime_cost, self.per_launch_cost = self.cost_estimator()