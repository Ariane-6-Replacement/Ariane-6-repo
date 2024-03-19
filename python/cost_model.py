import math
import numpy as np

############################################################################

# ROCKET MASS CALCULATOR

############################################################################

# Constants

g_0 = 9.81 # m / s^2

# Inputs:

dV = 10_000 # Required delta V (m/s)
dV_split = [0.346768978, 0.653231022] # Stage dV fraction (0 to 1) 
m_payload = 22_800 # Payload mass (kg) 
inert_mass_fractions = [0.0551575931, 0.0403852128] # Mass of structure relative to total mass of that stage (0 to 1)
I_sp = [296.5, 340] # Engine specific impulse for each stage.
rockets_per_stage = np.array([1, 1])

############################################################################

# Based on https://space.geometrian.com/calcs/opt-multi-stage.php and rocket equation
class MassCalculator:
    def __init__(self):
        pass
    def get_wet_mass_i(self,dV_i, I_sp_i, inert_mass_fraction_i, future_stages_wet_mass):
        V_i = g_0 * I_sp_i
        R_i = math.exp(dV_i / V_i)
        return future_stages_wet_mass * (R_i - 1) / (1 - R_i * inert_mass_fraction_i)

    # Returns wet masses of each stage (starting with first stage) in tonnes.
    def get_wet_masses(self, dV, dV_split, inert_mass_fractions, I_sp, m_payload):
        assert len(dV_split) == len(inert_mass_fractions), "Please provide arrays with equal lengths"
        assert len(dV_split) == len(I_sp), "Please provide arrays with equal lengths"

        wet_masses = []
        stages = len(dV_split)

        for i in reversed(range(stages)):
            dV_i = dV * dV_split[i]
            f_i = inert_mass_fractions[i]
            wet_mass_i = self.get_wet_mass_i(dV_i, I_sp[i], f_i, m_payload + sum(wet_masses))
            wet_masses.append(wet_mass_i)

        # Convert to tonnes after iterations are done
        for i, _ in enumerate(wet_masses):
            wet_masses[i] /= 1000

        return list(reversed(wet_masses))

    def get_propellant_masses(self, wet_masses, inert_mass_fractions):
        assert len(wet_masses) == len(inert_mass_fractions), "Please provide arrays with equal lengths"
        m_props = []
        for i in range(len(wet_masses)):
            m_prop = wet_masses[i] * (1 - inert_mass_fractions[i])
            m_props.append(m_prop)
        return m_props

    def get_dry_masses(self, wet_masses, inert_mass_fractions):
        assert len(wet_masses) == len(inert_mass_fractions), "Please provide arrays with equal lengths"
        m_dry_masses = []
        for i in range(len(wet_masses)):
            m_dry_mass = wet_masses[i] * inert_mass_fractions[i]
            m_dry_masses.append(m_dry_mass)
        return m_dry_masses


if __name__ == "__main__":
    wet_masses = get_wet_masses(dV, dV_split, inert_mass_fractions, I_sp, m_payload)
    prop_masses = get_propellant_masses(wet_masses, inert_mass_fractions)
    dry_masses = get_dry_masses(wet_masses, inert_mass_fractions)

    print("Wet masses:", wet_masses, "(tonnes)")
    print("Propellant masses:", prop_masses, "(tonnes)")
    print("Dry masses:", dry_masses, "(tonnes)")

    dry_masses = np.array(dry_masses)
    prop_masses = np.array(prop_masses)




    ############################################################################

    # COST CONVERSION FUNCTIONS

    def man_years_to_million_euro_2022(man_years):
        return man_years * 0.3397536 # TODO: ADD REFERENCE

    def million_euro_to_man_years_2022(million_euro):
        return million_euro / 0.3397536

    ############################################################################

    # COST INPUTS

    ############################################################################

    launches_per_year = 11
    rocket_fleet_count = 5
    number_of_engines = 11
    rocket_reflights = 15
    launch_site_capacity = 12 # Maximum number of launches that the launch site can do per year
    # TODO: Add engine unit cost in man-years
    engine_unit_cost = million_euro_to_man_years_2022(1_000_000) # Man-years
    engine_reflights = 15

    total_flights = rocket_fleet_count * rocket_reflights

    ############################################################################

    # DEVELOPMENT COST

    ############################################################################

    #---------------------------------------------------------------------------

    system_nature = "" # "new" # or: "similar", "similar_modified"
    team_experience = "" # "none" # or "some_related", "experienced"

    f1 = 1 # Technical Difficulty Factor
    f2 = 1 # Tech Quality Factor (from graph)
    f3 = 1 # Team Experience Factor
    f4 = 0.86 # Learning factor # 0.86 corresponds to 6 rockets per year

    if system_nature == "new":
        f1 = 1.25 # New system: 1.25
    elif system_nature == "similar":
        f1 = 0.9 # Similar systems exist: 0.8 -> 1.0
    elif system_nature == "similar_modified":
        f1 = 0.6 # Same as built by 1st party, only modifications: 0.4 -> 0.8

    if team_experience == "none":
        f3 = 1.2 # New : 1.1 -> 1.3
    elif team_experience == "some_related":
        f3 = 0.95 # Some related experience: 0.9 -> 1.1
    elif team_experience == "experienced":
        f3 = 0.75 # Previous relevant experience: 0.6 -> 0.9

    # Man-years
    def get_dev_costs_expandable(M_drymass, f_1, f_2, f_3):
        return 3140 * M_drymass ** 0.21 * f_1 * f_2 * f_3

    # Man-years
    def get_dev_costs_ballistic_reusable(M_drymass, f_1, f_2, f_3):
        return 4080 * M_drymass ** 0.21 * f_1 * f_2 * f_3

    reusable_costs = get_dev_costs_ballistic_reusable(dry_masses[0], f1, f2, f3)
    expandable_costs = get_dev_costs_expandable(dry_masses[1:dry_masses.size], f1, f2, f3)

    #---------------------------------------------------------------------------

    management_factor = 1.1

    # Man-years
    total_dev_cost = management_factor * (np.sum(reusable_costs) + np.sum(expandable_costs))

    #---------------------------------------------------------------------------

    ############################################################################

    print("Ballistic reusable dev costs:", reusable_costs)
    print("Expandable dev costs:", expandable_costs)
    print("Total dev costs:", total_dev_cost)

    ############################################################################

    # PRODUCTION COST

    ############################################################################

    #---------------------------------------------------------------------------

    # Man-years
    unit_production_cost = 5.0 * rockets_per_stage * f4 * dry_masses ** 0.46

    #---------------------------------------------------------------------------

    # Number of individual rocket stages (including identical ones)
    N = np.sum(rockets_per_stage)

    total_unit_production_cost = 1.02 ** N * np.sum(unit_production_cost)

    #---------------------------------------------------------------------------

    def get_total_production_cost(number_of_units, total_per_unit_production_cost):
        return number_of_units * total_per_unit_production_cost

    total_production_cost = get_total_production_cost(rocket_fleet_count, total_unit_production_cost)

    #---------------------------------------------------------------------------

    ############################################################################

    print("Unit production cost:", unit_production_cost)
    print("Total per unit production cost:", total_unit_production_cost)
    print("Total production cost for %s" % (rocket_fleet_count), "rockets:", total_production_cost)

    ############################################################################

    # FLIGHT OPERATIONS COST

    ############################################################################

    #---------------------------------------------------------------------------

    a_expandable = 3
    a_reusable = 4

    a_values = np.array([a_reusable, a_expandable])

    # Man-years
    technical_system_management_cost = (5 + np.sum(a_values)) * launches_per_year ** -0.35

    #---------------------------------------------------------------------------

    b_expandable = 12
    b_reusable = 20

    b_values = np.array([b_reusable, b_expandable])

    # Man-years
    prelaunch_operations_cost = (16 + np.sum(b_values)) * launches_per_year ** -0.35

    #---------------------------------------------------------------------------

    d_expandable = 1
    d_reusable = 2

    d_values = np.array([d_reusable, d_expandable])

    # Man-years
    launch_and_mission_operations_cost = (4 + np.sum(d_values)) * launches_per_year ** -0.15

    #---------------------------------------------------------------------------

    total_propellant_mass = np.sum(prop_masses)

    average_boil_off_rate = 0.2 # LOX and Methane similar: 0.2

    # Man-years / launch
    propellant_cost_per_launch = 0.016 * total_propellant_mass * average_boil_off_rate * (total_propellant_mass * launches_per_year) ** -0.16

    #---------------------------------------------------------------------------

    # recovery_cost is skipped because both land at launch site

    #---------------------------------------------------------------------------

    stage_refurbishment_effort = 3
    guidance_and_control_refurbishment_effort = 2
    engine_refurbishment_effort = 0.2
    fabrication_effort = total_unit_production_cost
    engine_effort = engine_unit_cost

    # Man-years
    refurbishment_cost = N * (stage_refurbishment_effort + guidance_and_control_refurbishment_effort) + number_of_engines * engine_refurbishment_effort \
                        + 2.5 * 10 ** -5 * rocket_reflights * fabrication_effort + 5 * 10 ** -5 * engine_reflights * engine_effort

    #---------------------------------------------------------------------------

    # Man-years per launch
    indirect_operations_cost_per_launch = 40 * launch_site_capacity ** 0.34 / launches_per_year ** 0.55

    #---------------------------------------------------------------------------

    ############################################################################

    print("Technical system management cost:", technical_system_management_cost)
    print("Prelaunch operations cost: ", prelaunch_operations_cost)
    print("Launch and mission operations cost: ", launch_and_mission_operations_cost)
    print("Propellant cost per launch:", propellant_cost_per_launch)
    print("Refurbishment cost:", refurbishment_cost)
    print("Indirect operations cost per launch:", indirect_operations_cost_per_launch)

    ############################################################################

    # COST OUTPUTS

    # reusable_costs
    # expandable_costs
    # total_dev_cost

    # unit_production_cost
    # total_unit_production_cost
    # total_production_cost

    # technical_system_management_cost
    # prelaunch_operations_cost
    # launch_and_mission_operations_cost

    # propellant_cost_per_launch
    # refurbishment_cost

    # indirect_operations_cost_per_launch

    ############################################################################

    total_lifecycle_cost =  total_dev_cost + \
                            total_production_cost + \
                            technical_system_management_cost  + \
                            prelaunch_operations_cost  + \
                            launch_and_mission_operations_cost  + \
                            refurbishment_cost

    cost_per_launch = total_lifecycle_cost / total_flights + propellant_cost_per_launch + indirect_operations_cost_per_launch

    print("Cost per launch (man-years):", cost_per_launch)
    print("Cost per launch (million euros):", man_years_to_million_euro_2022(cost_per_launch))
