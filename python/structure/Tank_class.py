from dome_class import Dome
from cylinder_class import Cylinder
import numpy as np
from materials import materials as m
class Tank:
    def __init__(self, outer_radius, pressure, material ,thrust, volume, fluid ) -> None:
        self.outer_radius = outer_radius
        self.pressure = pressure
        self.thrust = thrust
        self.material = m[material]
        self.volume = volume
        self.fluid = fluid 
       

      # Calculate dome_fwd and dome_aft directly within __init__
        self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
        self._dome_aft = Dome(self.outer_radius, self.pressure * 1.1, self.material)
        
        # Calculate cylinder height and create cylinder object
        cylinder_height = (self.volume - self._dome_fwd.inner_volume - self._dome_aft.inner_volume) / (np.pi * self.outer_radius**2)
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
    def mass(self)-> float:
        return self._dome_fwd.mass + self._dome_aft.mass + self._cylinder.mass

    @property
    def height(self) -> float:
        return self._cylinder.height + self._dome_fwd.height + self._dome_aft.height
    
    @property
    def inner_volume(self) -> float:
        return self._dome_fwd.inner_volume() + self._cylinder.inner_volume() + self._dome_aft.inner_volume()


if __name__ in "__main__":
    tank_test = Tank(2.5,5E5,'2219',3E6,300,'water')
    print('DONE')
    print(tank_test._cylinder.thickness)
    print('FINISHED')