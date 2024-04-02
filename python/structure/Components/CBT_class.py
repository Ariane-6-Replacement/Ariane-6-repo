from python.structure.Components.cylinder_class import Cylinder
from python.structure.Components.dome_class import Dome
from python.structure.materials import materials as m
import numpy as np 
from python.structure.constants import g_0, Km
class CBT:
  def __init__(self, outer_radius, pressure, material, thrust, 
              #  moment,
                volume_ox, mass_ox, volume_f, mass_f):
    self.outer_radius = outer_radius
    self.pressure = pressure
    self.thrust = thrust
    self.material = m[material]
    self.volume_ox = volume_ox
    self.volume_f = volume_f
    self.mass_ox = mass_ox
    self.mass_f = mass_f
    # self.moment = moment 

    if mass_ox > mass_f:
      self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
      self._dome_mid = Dome(self.outer_radius, (self.pressure +self.mass_f*g_0*1.5/(np.pi*self.outer_radius**2))*2.0 , self.material)
      self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_ox*g_0*1.5/(np.pi*self.outer_radius**2), self.material)
      cylinder_height_fwd = round((self.volume_f * 1.05 - self._dome_fwd.inner_volume - self._dome_mid.inner_volume) / (np.pi * self.outer_radius**2),3)
      cylinder_height_aft = round((self.volume_ox * 1.05 - self._dome_aft.inner_volume + self._dome_mid.outer_volume) / (np.pi * self.outer_radius**2),3)
      self._cylinder_fwd = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_fwd)
      self._cylinder_aft = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_aft)
    else:
      self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
      self._dome_mid = Dome(self.outer_radius, self.pressure +self.mass_ox*g_0*1.5/(np.pi*self.outer_radius**2) , self.material)
      self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_f*g_0*1.5/(np.pi*self.outer_radius**2), self.material)
      cylinder_height_fwd = round((self.volume_ox * 1.05 - self._dome_fwd.inner_volume - self._dome_mid.inner_volume) / (np.pi * self.outer_radius**2),3)
      cylinder_height_aft = round((self.volume_f * 1.05 - self._dome_aft.inner_volume + self._dome_mid.outer_volume) / (np.pi * self.outer_radius**2),3)
      self._cylinder_fwd = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_fwd)
      self._cylinder_aft = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_aft)

    
  @property
  def mass(self)-> float:
      return (self._dome_fwd.mass + self._dome_aft.mass + self._dome_mid.mass  +
               self._cylinder_aft.mass + self._cylinder_fwd.mass + self._cylinder_aft.insulation + self._cylinder_fwd.insulation +  1.123 * 4 *np.pi * self.outer_radius**2)*Km

  @property
  def height(self) -> float:
      return self._cylinder_aft.height + self._cylinder_fwd.height 

    

# if __name__ == "__main__":
#   test = CBT(2.7,7E5,'2195',11E6,328, 440E3,273,126E3) 
#   print('DONE')
#   print('Mass: ', test.mass)
#   print(f"Height {test.height}")
#   print(f'M1 {test._dome_fwd.mass} M2 {test._dome_mid.mass} M3 {test._dome_aft.mass}')
        
      
    