from python.core.rocket import Rocket
from python.ui.setup import UI
from python.structure.materials import materials as materials

def main():
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
        diameter = 5,
        of_ratio = 3.5,
    )
    ui = UI(rocket)
    ui.create()
def falcon9():
    rocket = Rocket(
        orbit_options = ['LEO', 'GTO', 'GEO', "LTO"],
        orbit_dv = [9256, 9256 + 2440, 9256 + 2440 + 1472, 9256 + 2440 +679],
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
    )
    ui = UI(rocket)
    ui.create()

if __name__ == "__main__":
    main()
    # falcon9()