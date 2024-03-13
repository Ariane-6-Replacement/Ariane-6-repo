from volume_mass_calculator import volume_fuel, volume_ox, mass_fuel, mass_ox, thrust
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from structure import structure



pressure = 7e5
structure1 = structure.Structure(6,pressure,"6082",volume_ox,mass_ox,pressure, volume_fuel,mass_fuel, thrust,"6062")
print("pressure:",pressure,"mass1:", structure1.mass, "height:",structure1.height)





