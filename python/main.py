from core.rocket import Rocket
from ui.setup import UI
from structure.materials import materials as materials

def main():
    rocket = Rocket(
        dv = 3000,
        orbit_options = ['LEO', 'MEO', 'GEO', 'HEO'],
        orbit = 0, # index in orbit options
        payload = 20000,
        cd = 0.2,
        mf2 = 0.04,
        isp2 = 296,
        dv_split = 0.5,
        engine = "Prometheus",
        mf1 = 0.05,
        boostback = False,
        material_options = list(materials.keys()),
        material_tank = 0, # index in material options
        material_misc = 0, # index in material options
        bulkhead = "shared",
        pressure_ox = 5,
        pressure_fuel = 5,
        diameter = 5,
        of_ratio = 3.5,
    )
    ui = UI(rocket)
    ui.create()

if __name__ == "__main__":
    main()