import math

from python.propulsion.density import get_density


# CLASSES
class FirstStage:
    def __init__(self, Thrust=19.97e6, burn_time=100):
        self.Thrust = Thrust  # Newton ; Derived from A64 (wiki); =Fz
        self.Fx = 10000  # TBR
        self.Fy = 10000  # TBR
        self.Mx, self.My, self.Mz = 0, 0, 0

        self.time_burn_1st = burn_time  # seconds, just a guess
        self.booster_area = 150  # m2  assuming 7 meter diameter


class Prometheus:
    def __init__(self):
        self.name = "Prometheus"
        self.Thrust = 980e3
        self.cost = 1e6
        self.mass_sea = 1385  # kg [source: paper: A viable and sustainable European path into space – for cargo and astronauts]
        self.mass_vac = 1750  # kg [source: paper: A viable and sustainable European path into space – for cargo and astronauts]
        #self.of_ratio = 3.5  # chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.eucass.eu/doi/EUCASS2017-537.pdf
        # self.of_ratio = 1.7 # wrong? https://aris-space.ch/introduction-to-prometheus/
        #self.Isp = self.get_Isp(of_ratio)
        self.exit_diameter = 1.751  # m
        self.exit_area = math.pi * self.exit_diameter ** 2 / 4
        self.height = 4.28  # m
        self.of_ratio = 3.5
        self.p_exit = 40000  # pa
        self.turbopump_overall_power = 10e6  # MW
        self.diameter_truss_structure = 3.35
        self.area_truss_structure = math.pi * self.diameter_truss_structure ** 2 / 4

    def get_Isp(self, of_ratio):
    #     """"
    #     Lower O/F can mean less mass because LOX is heavy. Nominal: Isp = 360 for 100bar and O/F=3.5
    #     assume Isp goes down with 10 for every 0.1 OF. chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.eucass.eu/doi/EUCASS2017-537.pdf
    #     """
    #     self.ISP = 360 - abs(3.5 - of_ratio) * 100
    #     return  self.ISP
        
        self.Isp = 306.266 # calculated using Isp_calculator.py. UPDATE ITERATIVELY (for now)
        return self.Isp



class Vinci:  # TODO add specs
    def __init__(self):
        pass


class Propellant:
    def __init__(self):
        # FUEL = METHANE

        # pressure
        self.pressure_ox = 8e5  # Pa
        self.pressure_fuel = 8e5  # Pa

        # temperature
        self.temperature_ox = 90  # K
        self.temperature_fuel = 111  # K

        # Molar mass
        self.M_ox = 32.0 / 1000  # kg/mol
        self.M_fuel = 16.04 / 1000  # kg/mol

        # density (determined using thermodynamic table, see density.py)
        self.density_ox = get_density("NIST_LOX_densities.json", self.temperature_ox, self.pressure_ox,
                                      self.M_ox * 1000)  # kg/m3 liquid oxygen
        self.density_fuel = get_density("NIST_methane_densities.json", self.temperature_fuel, self.pressure_fuel,
                                        self.M_fuel * 1000)  # kg/m3 liquid methane  # should be checked , at which temperature?

        # Raptor Mixture Ratio: 3.8 kg LOX to 1kg Methane. [Source](https://en.wikipedia.org/wiki/Raptor_(rocket_engine)).

# CHOOSE (so 'settings'/inputs can easily be imported by all files. For example, other engine choice will automatically be used by all files)
engine = Prometheus()
first_stage = FirstStage()
propellant = Propellant()
