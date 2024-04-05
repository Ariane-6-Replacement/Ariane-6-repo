import numpy as np
from python.core.rocket import Rocket
from python.ui.setup import UI
from python.structure.materials import materials as materials

def Elysium1():
    rocket = Rocket(
        orbit_options = ['LEO', 'GTO', 'GEO', "LTO"],
        orbit_dv = [9256, 9256 + 2440, 9256 + 2440 + 1472, 9256 + 2440 +679],
        orbit = 0, # index in orbit options
        payload = 20000,
        cd = 0.2,
        mf2 = 0.04,
        isp2 = 457,
        dv_split = 0.40,
        engine_options = ['Prometheus', 'Merlin1D'],
        engine_index = 0, # index in engine options
        engine_number = 9,
        mf1 = 0.05,
        reflights = 5,
        material_options = list(materials.keys()),
        material_tank = 3, # index in material options
        material_misc = 3, # index in material options
        bulkhead_options = ["shared", "separate"],
        bulkhead = 0, # index in bulkhead options
        pressure_ox = 5,
        pressure_fuel = 5,
        temperature_ox = 90,
        temperature_fuel = 111,
        diameter = 5, # m
        of_ratio = 3.5,
        trajectory_timestep = 0.01, # seconds
        trajectory_max_time = 900, # seconds
        number_of_engines_ascent = 9,
        number_of_engines_landing = 1,
        number_of_engines_reentry = 3,
        kick_angle = 68, # degrees
        kick_time = 10, # seconds
        delta_V_landing = 909, # m / s
        delta_V_reentry = 1905, # m / s
        reentry_burn_alt = 55_000, # m
        gravity_turn_alt = 10_000 # m
    )
    ui = UI(rocket)
    ui.create()
def falcon9():
    rocket = Rocket(
        orbit_options = ['LEO', 'GTO', 'GEO', "LTO"],
        orbit_dv = [9256, 9256 + 2440, 9256 + 2440 + 1472, 9256 + 2440 + 679],
        orbit = 0, # index in orbit options
        payload = 18500,
        cd = 0.2,
        mf2 = 0.03,
        isp2 = 348,
        dv_split = 0.41,
        engine_options = ['Prometheus', 'Merlin1D'],
        engine_index = 1, # index in engine options
        #engine_number = 9,
        #mf1 = 0.05,
        reflights = 10,
        material_options = list(materials.keys()),
        material_tank = 3, # index in material options
        material_misc = 3, # index in material options
        bulkhead_options = ["shared", "separate"],
        bulkhead = 1, # index in bulkhead options
        pressure_ox = 3.5,
        pressure_fuel = 3.5,
        temperature_ox = 90,
        temperature_fuel = 111,
        diameter = 3.66,
        of_ratio = 2.34,
        trajectory_timestep = 0.01,
        trajectory_max_time = 900,
        number_of_engines_ascent = 9,
        number_of_engines_landing = 1,
        number_of_engines_reentry = 3,
        kick_angle = 75.5, # degrees
        kick_time = 8,
        delta_V_landing = 200,
        delta_V_reentry = 2_000,
        reentry_burn_alt = 55_000,
        gravity_turn_alt = 1500
    )
    ui = UI(rocket)
    ui.create()

if __name__ == "__main__":
    # SELECT TEMPLATE TO RUN

    # Elysium1()
    falcon9()