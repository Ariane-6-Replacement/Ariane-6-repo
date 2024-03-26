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
        isp2 = 296,
        dv_split = 0.3,
        engine_options = ['Prometheus'],
        engine = 0, # index in engine options
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

if __name__ == "__main__":
    main()