
from python.propulsion.inputs import first_stage
# from python.propulsion.inputs import propellant
from python.propulsion.volume_mass_calculator import get_propellant_mass_volume
import math

class Propulsion():
    def __init__(self, engine, of_ratio,p_ox,p_fuel):
        # engine name
        self.engine = engine

        self.of_ratio = of_ratio
        self.Isp = self.engine.get_Isp(of_ratio=of_ratio)
    def mass_volume(self,thrust, burn_time,t_fuel,t_ox,p_ox,p_fuel):
        # engine number and mass
        self.engine_number = math.ceil(thrust / self.engine.Thrust)
        self.total_engine_mass = self.engine.mass_sea * self.engine_number

        # calculate mass, volume
        mass_ox, mass_fuel, volume_ox, volume_fuel = get_propellant_mass_volume(thrust, burn_time, self.of_ratio,t_fuel,t_ox,p_ox,p_fuel)

        # propellant volume
        self.volume_ox = volume_ox
        self.volume_fuel = volume_fuel
        self.volume_total = self.volume_ox + self.volume_fuel


        # propellant mass
        self.mass_ox = mass_ox
        self.mass_fuel = mass_fuel
        self.mass_total = self.mass_ox + self.mass_fuel
        return self.total_engine_mass, self.mass_fuel, self.mass_ox, self.volume_fuel, self.volume_ox, self.engine_number

if __name__ == "__main__":
    # define inputs for Propulsion() class
    engine_name = engine.name
    thrust = first_stage.Thrust
    burn_time = first_stage.time_burn_1st

    # make propulsion class based on inputs
    propulsion = Propulsion("Prometheus")

    # print/return wanted values
    # print(propulsion.mass_ox, propulsion.mass_fuel, propulsion.mass_total)
    # print(propulsion.volume_ox, propulsion.volume_fuel, propulsion.volume_total)Ra