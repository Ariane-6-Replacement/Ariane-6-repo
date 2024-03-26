from python.core.rocket import Rocket
from python.ui.setup import UI
from python.structure.materials import materials as materials

def main():
    rocket = Rocket(
        dv = 10000,
        orbit_options = ['LEO', 'MEO', 'GEO', 'HEO'],
        orbit = 0, # index in orbit options
        payload = 20000,
        cd = 0.2,
        mf2 = 0.04,
        isp2 = 296,
        dv_split = 0.5,
        engine_options = ['Prometheus'],
        engine = 0, # index in engine options
        mf1 = 0.05,
        boostback = False,
        material_options = list(materials.keys()),
        material_tank = 0, # index in material options
        material_misc = 0, # index in material options
        bulkhead_options = ["shared", "separate"],
        bulkhead = 0, # index in bulkhead options
        pressure_ox = 5,
        pressure_fuel = 5,
        t_ox = 90,
        t_fuel = 111,
        diameter = 5,
        of_ratio = 3.5,
    )
    ui = UI(rocket)
    ui.create()

if __name__ == "__main__":
    main()