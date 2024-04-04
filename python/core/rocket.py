
import numpy as np

from python.propulsion.propulsion import Propulsion
from python.structure.structure import Structure
from python.trajectory.trajectory_simulator import Trajectory
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
        self.trajectory = Trajectory()

    def mass_estimation(self):
        self.inert_mass_fractions = np.array([self.mf2, self.mf2])
        self.ISPs = np.array([self.isp2, self.propulsion.Isp])


        self.wet_masses = MassCalculator.get_wet_masses(self.dv_1, self.dv_2, self.inert_mass_fractions,
                                                        self.ISPs, self.payload, self.reflights)
        self.prop_masses = MassCalculator.get_propellant_masses(self.wet_masses, self.inert_mass_fractions)
        self.dry_masses  = MassCalculator.get_dry_masses(self.wet_masses, self.inert_mass_fractions)
        self.mass2, self.mass = self.wet_masses
        self.mass_prev = self.mass
        self.mass_total = self.mass + self.mass2 + self.payload
        self.struct_frac_1 = self.inert_mass_fractions[1]
    def cost_estimator(self):
        cm = CostModel()
        self.prop_masses = np.array([self.prop_masses[0], self.mass_p / 1000])
        self.dry_masses = np.array([self.dry_masses[0], self.mass_s]) / 1000
        cm.calculate(self.dry_masses,self.prop_masses , self.reflights, self.engine.cost, self.engine_number)
        self.total_lifetime_cost = cm.cost.total_lifetime_euros
        self.per_launch_cost = cm.cost.per_launch_euros
        self.development_cost = cm.cost.development_cost_euros
        self.operational_cost = cm.cost.operational_euro
        self.production_cost = cm.cost.production_euro
    
    def iterate(self):
        e = 10e9
        i = 0

        # Propellant margins can be changed here. Seems too minor to include in the user interface (too much clutter). 
        first_stage_ascent_prop_margin = 1.02
        first_stage_landing_prop_margin = 1.1
        first_stage_reentry_prop_margin = 1.05

        max_converge = 100

        print("thrust", self.engine.Thrust)
        print("isp1", self.propulsion.Isp)
        print("isp2", self.isp2)
        print("kick_angle", np.radians(self.kick_angle))
        print("kick_time", self.kick_time)
        print("total mass 1", self.mass * first_stage_ascent_prop_margin)
        print("structural frac", self.struct_frac_1)
        print("prop mass 2", self.prop_masses[1])
        print("payload", self.payload)
        print("delta_V_landing", self.delta_V_landing * first_stage_landing_prop_margin)
        print("delta_V_reentry", self.delta_V_reentry * first_stage_reentry_prop_margin)
        print("cd", self.cd)
        print("diameter", self.diameter)
        print("reentry_burn_alt", self.reentry_burn_alt)
        print("gravity_turn_alt", self.gravity_turn_alt)

        while e > 10000:
            if i == 0 or i == max_converge - 1:
                self.trajectory.setup(
                    simulation_timestep = self.trajectory_timestep, # seconds
                    simulation_time = self.trajectory_max_time, # seconds
                    number_of_engines_ascent=self.number_of_engines_ascent,
                    number_of_engines_landing=self.number_of_engines_landing,
                    number_of_engines_reentry=self.number_of_engines_reentry,
                    thrust=self.engine.Thrust, # newtons
                    I_sp_1=self.propulsion.Isp, # seconds
                    I_sp_2=self.isp2, # seconds 
                    kick_angle=np.radians(self.kick_angle), # degrees -> radians
                    gamma_change_time=self.kick_time, # seconds
                    m_first_stage_total=self.mass * first_stage_ascent_prop_margin,
                    m_first_stage_structural_frac=self.struct_frac_1,
                    #m_second_stage_structural=9.272e3, # kg
                    m_second_stage_propellant=self.prop_masses[0], # kg
                    m_second_stage_payload=self.payload, # kg
                    delta_V_landing=self.delta_V_landing * first_stage_landing_prop_margin, # m / s
                    delta_V_reentry=self.delta_V_reentry * first_stage_reentry_prop_margin, # m / s
                    Cd_ascent=self.cd,
                    Cd_descent=1.0, # assumed constant
                    diameter=self.diameter, # meters
                    reentry_burn_alt=self.reentry_burn_alt, # meters
                    gravity_turn_alt=self.gravity_turn_alt # meters
                )
                self.trajectory.run()
            self.thrust = self.trajectory.number_of_engines_ascent * self.trajectory.thrust
            self.burntime = self.trajectory.burntime
            self.mass_e, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number = (
                self.propulsion.mass_volume(self.thrust, self.burntime, self.temperature_fuel, self.temperature_ox,
                                            self.pressure_ox, self.pressure_fuel))
            self.mass_p = self.mass_ox + self.mass_fuel
            self.structure.calc(self.bulkhead_options[self.bulkhead], self.volume_ox, self.mass_ox, self.volume_fuel,
                                self.mass_fuel, self.thrust, self.mass_e)
            self.mass_t = self.structure.mass_total #Returns mass of the tank/s ITS/s and engine bay
            self.mass_es = self.structure.mass_engine_structure
            self.mass_lg = self.structure.mass_landing_gear
            self.mass_s = self.mass_e + self.mass_es + self.mass_lg + self.mass_t
            self.mass = self.mass_p + self.mass_s
            self.struct_frac_1 = self.mass_s / self.mass
            self.mass_total = self.mass + self.mass2 + self.payload
            e = np.abs(self.mass - self.mass_prev)
            i += 1
            self.mass_prev = self.mass
            print(f"Iterated! Mass = {self.mass:.0f}, e = {e:.0f}")
            if i >= max_converge:
                print(f"Non convergence!")
                break
        self.cost_estimator()