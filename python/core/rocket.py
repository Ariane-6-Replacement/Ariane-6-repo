
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
        self.__dict__.update(**kwargs)
        #self.aerodynamics = Aerodynamics()
        #self.control = Control()
        self.dv = self.orbit_dv[self.orbit]
        self.dv_2 = self.dv * (1 - self.dv_split )
        landingdv = 0
        if self.reflights > 0:
            landingdv = 1000
        self.dv_1 = self.dv - self.dv_2 + landingdv
        if self.engine_options[self.engine_index] == "Prometheus":
            from python.propulsion.inputs import Prometheus
            self.engine = Prometheus()
        elif self.engine_options[self.engine_index] == "Merlin1D":
            from python.propulsion.inputs import Merlin1D
            self.engine = Merlin1D()

        self.propulsion = Propulsion(self.engine, self.of_ratio, self.pressure_ox*10**5,
                                     self.pressure_fuel*10**5)
        self.structure = Structure(self.diameter / 2, self.material_options[self.material_tank], self.pressure_ox,
                                   self.pressure_fuel, self.material_options[self.material_misc])
        self.trajectory = Trajectory(self.orbit_options[self.orbit], self.payload, self.cd)

    def mass_estimation(self):
        self.inert_mass_fractions = np.array([self.mf2, self.mf2])
        self.ISPs = np.array([self.isp2, self.propulsion.Isp])

        # All outputs in tonnes

        self.wet_masses = MassCalculator.get_wet_masses(self.dv_1, self.dv_2, self.inert_mass_fractions,
                                                        self.ISPs, self.payload, self.reflights)
        self.prop_masses = MassCalculator.get_propellant_masses(self.wet_masses, self.inert_mass_fractions)
        self.dry_masses  = MassCalculator.get_dry_masses(self.wet_masses, self.inert_mass_fractions)

        # Convert tonnes to kg
        self.mass2, self.mass = self.wet_masses
        self.mass_prev = self.mass
        self.mass_total = self.mass + self.mass2 + self.payload
    def cost_estimator(self):
        cm = CostModel()
        self.prop_masses = np.array([self.prop_masses[0],self.mass_p / 1000])
        self.dry_masses = np.array([self.dry_masses[0], self.mass_s]) / 1000
        cm.calculate(self.dry_masses,self.prop_masses , self.reflights, self.engine.cost, self.engine_number)
        return cm.cost.total_lifetime_euros, cm.cost.per_launch_euros, cm.cost.development_cost_euros
    
    def iterate(self):
        e = 10e9
        i = 0
        while e > 10000:
            self.thrust, self.burntime = self.trajectory.thrust_burntime(self.mass_total, self.dv)
            self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = (
                self.propulsion.mass_volume(self.thrust, self.burntime, self.temperature_fuel, self.temperature_ox,
                                            self.pressure_ox, self.pressure_fuel))
            self.mass_p = self.mass_ox + self.mass_fuel
            self.structure.calc(self.bulkhead_options[self.bulkhead], self.volume_ox, self.mass_ox, self.volume_fuel,
                                self.mass_fuel, self.thrust, self.mass_e, self.engine_number)
            self.mass_t = self.structure.mass_total #Returns mass of the tank/s ITS/s and engine bay
            self.mass_es = self.structure.mass_engine_structure
            self.mass_lg = self.structure.mass_landing_gear
            self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
            self.mass = self.mass_p + self.mass_s
            self.mass_total = self.mass + self.mass2 + self.payload
            e = np.abs(self.mass - self.mass_prev)
            i += 1
            self.mass_prev = self.mass
            print(f"Iterated! Mass = {self.mass:.0f}, e = {e:.0f}")
            if i >= 100:
                print(f"Non convergence!")
                break
        self.lifetime_cost, self.per_launch_cost, self.development_cost = self.cost_estimator()