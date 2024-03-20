from python.propulsion.volume_mass_calculator import volume_fuel, volume_ox, mass_fuel, mass_ox, thrust
from python.structure import python.structure

pressure = 7e5
structure1 = structure.Structure(6,pressure,"6082",volume_ox,mass_ox,pressure, volume_fuel,mass_fuel, thrust,"6062")
print("pressure:",pressure,"mass1:", structure1.mass, "height:",structure1.height)





