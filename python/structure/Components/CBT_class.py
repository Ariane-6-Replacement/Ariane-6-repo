'''
Code for creating common bulkhead tank object.
'''
from python.structure.Components.cylinder_class import Cylinder
from python.structure.Components.dome_class import Dome
from python.structure.materials import materials as m
import numpy as np 
from python.structure.constants import g_0, Km, Ku, Mi
class CBT:
  def __init__(self, outer_radius, pressure, material, thrust,
                volume_ox, mass_ox, volume_f, mass_f):
    self.outer_radius = outer_radius
    self.pressure = pressure
    self.thrust = thrust
    self.material = m[material]
    self.volume_ox = volume_ox
    self.volume_f = volume_f
    self.mass_ox = mass_ox
    self.mass_f = mass_f
    """
        Common Bulkhead Tank object, containing all relevant parameters.
        :param outer_radius: in m
        :param pressure: in Pa
        :param thrust: in N
        :param volume_ox: in m^3
        :param volume_f: in m^3
        :param mass_ox: in kg
        "param mass_f: in kg 
        :param material: dictionary object from materials database
        """
    #NOTE:Assumption - heavier tank is on the bottom for ladning stability purposes.

    if mass_ox > mass_f:
      self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)

      #NOTE:
      '''
      The hydrostatic pressure effect caused by propellant is accounted by multiplying by the
      highest estiamted T/W ration and divided by cross-section area
      For common bulkhead to account for compressive stress form the concave side of the dome additioanl factor of 2.0 is included
      This is deemded sufficient if the the convex side is pressurized first;
      '''
      self._dome_mid = Dome(self.outer_radius, (self.pressure +self.mass_f*g_0*2.0/(np.pi*self.outer_radius**2))*2.0 , self.material)
      self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_ox*g_0*2.0/(np.pi*self.outer_radius**2), self.material)
      cylinder_height_fwd = round((self.volume_f * Ku - self._dome_fwd.inner_volume - self._dome_mid.inner_volume) / (np.pi * self.outer_radius**2),3)
      cylinder_height_aft = round((self.volume_ox * Ku - self._dome_aft.inner_volume + self._dome_mid.outer_volume) / (np.pi * self.outer_radius**2),3)
      self._cylinder_fwd = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_fwd)
      self._cylinder_aft = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_aft)

    else:

      self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
      self._dome_mid = Dome(self.outer_radius, self.pressure +self.mass_ox*g_0*2.0/(np.pi*self.outer_radius**2) , self.material)
      self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_f*g_0*2.0/(np.pi*self.outer_radius**2), self.material)
      cylinder_height_fwd = round((self.volume_ox * Ku - self._dome_fwd.inner_volume - self._dome_mid.inner_volume) / (np.pi * self.outer_radius**2),3)
      cylinder_height_aft = round((self.volume_f * Ku - self._dome_aft.inner_volume + self._dome_mid.outer_volume) / (np.pi * self.outer_radius**2),3)
      self._cylinder_fwd = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_fwd)
      self._cylinder_aft = Cylinder(self.outer_radius, self.material, self.pressure, self.thrust, cylinder_height_aft)

    
  @property
  def mass(self)-> float:
      return (self._dome_fwd.mass + self._dome_aft.mass + self._dome_mid.mass  +
               self._cylinder_aft.mass + self._cylinder_fwd.mass + self._cylinder_aft.insulation + self._cylinder_fwd.insulation +  Mi * 4 *np.pi * self.outer_radius**2)*Km

  @property
  def height(self) -> float:
      return self._cylinder_aft.height + self._cylinder_fwd.height 

        
      
    