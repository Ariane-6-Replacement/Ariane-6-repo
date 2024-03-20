from python.structure.Components.dome_class import Dome
from python.structure.Components.cylinder_class import Cylinder
from python.structure.materials import materials as m
import numpy as np

class Tank:
    def __init__(self, outer_radius, pressure, material, thrust, volume, mass_p):
        self.outer_radius = outer_radius
        self.pressure = pressure
        self.thrust = thrust
        self.material = m[material]
        self.volume = volume
        self.mass_p = mass_p
       

      # Calculate dome_fwd and dome_aft directly within __init__
        g_0 = 9.81 # m / s^2
        self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
        self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_p*g_0*2/(np.pi*self.outer_radius**2), self.material)
        
        # Calculate cylinder height and create cylinder object
        cylinder_height = round((self.volume * 1.05 - self._dome_fwd.inner_volume - self._dome_aft.inner_volume) / (np.pi * self.outer_radius**2),3)
        self._cylinder = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height)
        
    @property
    def dome_fwd(self):
        return self._dome_fwd
    
    @property
    def dome_aft(self):
        return self._dome_aft
    
    @property
    def cylinder(self):
        return self._cylinder
            
    @property
    def mass(self) -> float:
        return (self._dome_fwd.mass + self._dome_aft.mass + self._cylinder.mass + self._cylinder.insulation)*1.2

    @property
    def height(self) -> float:
        return self._cylinder.height + self._dome_fwd.height + self._dome_aft.height
    
    @property
    def inner_volume(self) -> float:
        return self._dome_fwd.inner_volume() + self._cylinder.inner_volume() + self._dome_aft.inner_volume()
  

# if __name__ == "__main__":
#     tank_test = Tank(2.5,7.8E5,'2219',11E6,400,300E3)
#     print('DONE')
#     print('Thickness: ',tank_test._cylinder.thickness)
#     print('Mass: ',tank_test.mass)
#     print('FINISHED')