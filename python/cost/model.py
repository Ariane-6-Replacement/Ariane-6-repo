import numpy as np
import math

# Cost and mass model for the rocket. It calculates the  mass of the rocket based on the inputs given in the main.py file.
# Additionally, it gives a first estimate for the cost, based on the final mass and properties of the rocket.


# Constants:

g_0 = 9.81 # m / s^2

class Cost:
     def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)



# Based on https://space.geometrian.com/calcs/opt-multi-stage.php and rocket equation
class MassCalculator:
    @staticmethod
    def get_wet_mass_i(dV_i, I_sp_i, inert_mass_fraction_i, future_stages_wet_mass):
        V_i = g_0 * I_sp_i
        R_i = math.exp(dV_i / V_i)
        return future_stages_wet_mass * (R_i - 1) / (1 - R_i * inert_mass_fraction_i)

    # Returns wet masses of each stage (starting with first stage) in tonnes.
    @staticmethod
    def get_wet_masses(dV1, dV2, inert_mass_fractions, Isp, m_payload, reflights):

        
        dV_split = np.array([dV2, dV1])
        assert dV_split.size == inert_mass_fractions.size, "Please provide arrays with equal lengths"
        assert dV_split.size == Isp.size, "Please provide arrays with equal lengths"

        wet_masses = np.array([m_payload,0,0])
        #print(f'Delta V For Stages: {dV_split / 1000} km / s')
        # for i in np.flip(np.array(range(stages))):
            # dV_i = dV_split[i]
         #    f_i = inert_mass_fractions[i]
         # #   wet_mass_i = MassCalculator.get_wet_mass_i(dV_i, I_sp[i], f_i, m_payload + np.sum(wet_masses))
        #    wet_masses = np.append(wet_masses, wet_mass_i)

       # wet_masses = np.zeros(len(dV_split))
        for i in range(1,len(wet_masses)):
            Vi = Isp[i-1]*9.81
            Ri = np.exp(dV_split[i-1]/Vi)
            wet_masses[i] = np.sum(wet_masses[0:i]) * (Ri-1) / (1-Ri*inert_mass_fractions[i-1])
        wet_masses2 = np.array([np.sum(wet_masses[0:2]), wet_masses[2]])
        return wet_masses2
    @staticmethod
    def get_propellant_masses(wet_masses, inert_mass_fractions):
        assert wet_masses.size == inert_mass_fractions.size, "Please provide arrays with equal lengths"
        return wet_masses * (1 - inert_mass_fractions)

    @staticmethod
    def get_dry_masses(wet_masses, inert_mass_fractions):
        assert wet_masses.size == inert_mass_fractions.size, "Please provide arrays with equal lengths"
        return wet_masses * inert_mass_fractions



class CostModel():
    def __init__(self):
        self.cost = Cost(total_lifetime=0,
                         per_launch=0,
                         total_lifetime_euros=0,
                         per_launch_euros=0)
        self.development = DevelopmentModel()
        self.production = ProductionModel()
        self.operational = OperationalModel()
        
    def man_years_to_million_euro_2022(self,man_years):
        return man_years * 0.3397536 # TODO: ADD REFERENCE

    def euro_to_man_years_2022(self, euro):
        return euro / 1000000 / 0.3397536

    def calculate(self,
                  dry_masses, # tonnes
                  prop_masses, # tonnes
                  rocket_reflights,
                  engine_unit_cost,
                  engine_number,
                  launches_per_year = 10,
                  lifetime = 20,
                  #rocket_fleet_count = 5,
                  number_of_engines = 11,
                  launch_site_capacity = 12,
                  engine_reflights = 15):
        self.rockets_per_stage = np.array([1, 1])
        #self.total_flights = rocket_fleet_count * rocket_reflights
        self.total_flights = launches_per_year * lifetime
        engine_cost = self.euro_to_man_years_2022(engine_unit_cost)
        self.number_of_rocket_stages = np.sum(self.rockets_per_stage)
        rocket_fleet_count = self.total_flights / (rocket_reflights + 1)
        self.development.calculate(dry_masses)
        self.cost.development_cost_euros = self.man_years_to_million_euro_2022(self.development.cost.total)
        self.production.calculate(dry_masses,
                                  self.rockets_per_stage,
                                  self.number_of_rocket_stages,
                                  rocket_fleet_count,
                                  engine_cost,
                                  engine_number,
                                  rocket_reflights,
                                  learning_factor=1.00)

        self.operational.calculate(prop_masses,
                                   self.total_flights,
                                   launches_per_year,
                                   self.production.cost.total_unit,
                                   engine_unit_cost,
                                   self.number_of_rocket_stages,
                                   number_of_engines,
                                   rocket_reflights,
                                   engine_reflights,
                                   launch_site_capacity)
        self.cost.production_euro = self.man_years_to_million_euro_2022(self.production.cost.total_unit)
        self.cost.operational_euro = self.man_years_to_million_euro_2022(self.operational.cost.total) / self.total_flights
        # Man-years
        self.cost.total_lifetime = self.production.cost.total + \
                                     self.operational.cost.total

        # Million euros
        self.cost.total_lifetime_euros = self.man_years_to_million_euro_2022(self.cost.total_lifetime)

        # Man-years

        #self.cost.per_launch = self.cost.total_lifetime / self.total_flights

        # Million euros
        self.cost.per_launch_euros = self.cost.production_euro + self.cost.operational_euro


class DevelopmentModel():
    def __init__(self):
        self.cost = Cost(cryogenic_expandable=0,
                         ballistic_reusable=0,
                         total=0)
    
    def calculate(self,
                  dry_masses, # tonnes
                  system_nature="similar",
                  team_experience="some_related"):
        self.management_factor = 1.1
        self.f1 = 1 # Technical Difficulty Factor
        self.f2 = 1 # Tech Quality Factor (from graph)
        self.f3 = 1 # Team Experience Factor

        if system_nature == "new":
            self.f1 = 1.25 # New system: 1.25
        elif system_nature == "similar":
            self.f1 = 0.9 # Similar systems exist: 0.8 -> 1.0
        elif system_nature == "similar_modified":
            self.f1 = 0.6 # Same as built by 1st party, only modifications: 0.4 -> 0.8

        if team_experience == "none":
            self.f3 = 1.2 # New : 1.1 -> 1.3
        elif team_experience == "some_related":
            self.f3 = 0.95 # Some related experience: 0.9 -> 1.1
        elif team_experience == "experienced":
            self.f3 = 0.75 # Previous relevant experience: 0.6 -> 0.9

        # Man-years
        # SET TO ZERO BECAUSE WE REUSE A6
        self.cost.cryogenic_expandable = 3140 * dry_masses[0] ** 0.21 * self.f1 * self.f2 * self.f3 * 000000000

        # Man-years
        self.cost.ballistic_reusable = 4080 * dry_masses[1:dry_masses.size] ** 0.21 * self.f1 * self.f2 * self.f3

        # Man-years
        self.cost.total = self.management_factor * (np.sum(self.cost.cryogenic_expandable) + np.sum(self.cost.ballistic_reusable))


class ProductionModel():
    def __init__(self):
        self.cost = Cost(unit=0,
                         total_unit=0,
                         total=0)
        
    def calculate(self,
                  dry_masses, # tonnes
                  rockets_per_stage,
                  number_of_rocket_stages,
                  rocket_fleet_count,
                  engine_cost,
                  number_engines,
                  reflights,
                  learning_factor):
        # Man-years
        self.cost.core = 4 *(5.0 * learning_factor * dry_masses[1] ** 0.46 + number_engines * engine_cost) / (reflights + 1)
        self.cost.upper = 4 * 5.0 * learning_factor * dry_masses[0] ** 0.46

        # Man-years
        self.cost.total_unit = 1.02 * (self.cost.core + self.cost.upper)

        # Man-years
        self.cost.total = rocket_fleet_count * self.cost.total_unit 



class OperationalModel():
    def __init__(self):
        self.cost = Cost(technical_system_management=0,
                         prelaunch_operations=0,
                         launch_and_mission_operations=0,
                         propellant=0,
                         refurbishment=0,
                         indirect_operations=0,
                         total=0)
    
    def calculate(self,
                  prop_masses, # tonnes
                  total_flights,
                  launches_per_year,
                  total_unit_production_cost,
                  engine_unit_cost,
                  number_of_rocket_stages,
                  number_of_engines,
                  rocket_reflights,
                  engine_reflights,
                  launch_site_capacity):
        a_expandable = 3
        a_reusable = 4
        a_values = np.array([a_reusable, a_expandable])

        # Man-years
        self.cost.technical_system_management = (5 + np.sum(a_values)) * launches_per_year ** -0.35

        b_expandable = 12
        b_reusable = 20
        b_values = np.array([b_reusable, b_expandable])

        # Man-years
        self.cost.prelaunch_operations = (16 + np.sum(b_values)) * launches_per_year ** -0.35

        d_expandable = 1
        d_reusable = 2
        d_values = np.array([d_reusable, d_expandable])

        # Man-years
        self.cost.launch_and_mission_operations = (4 + np.sum(d_values)) * launches_per_year ** -0.15

        total_propellant_mass = np.sum(prop_masses)
        average_boil_off_rate = 0.2 # LOX and Methane similar: 0.2

        # Man-years
        self.cost.propellant = (0.016 * total_propellant_mass * average_boil_off_rate *
                               (total_propellant_mass * launches_per_year) ** -0.16) * total_flights

        #---------------------------------------------------------------------------
        # recovery_cost is skipped because both land at launch site
        #---------------------------------------------------------------------------

        stage_refurbishment_effort = 3
        guidance_and_control_refurbishment_effort = 2
        engine_refurbishment_effort = 0.2
        fabrication_effort = total_unit_production_cost
        engine_effort = engine_unit_cost

        # Man-years
        self.cost.refurbishment = number_of_rocket_stages * (stage_refurbishment_effort + guidance_and_control_refurbishment_effort) + \
                                  number_of_engines * engine_refurbishment_effort + \
                                  2.5 * 10 ** -5 * rocket_reflights * fabrication_effort + \
                                  5 * 10 ** -5 * engine_reflights * engine_effort

        # Man-years
        self.cost.indirect_operations = (40 * launch_site_capacity ** 0.34 / launches_per_year ** 0.55) * total_flights

        self.cost.total = self.cost.technical_system_management + self.cost.prelaunch_operations + \
                          self.cost.launch_and_mission_operations + self.cost.propellant + \
                          self.cost.refurbishment + self.cost.indirect_operations