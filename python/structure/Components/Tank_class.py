'''
Code for creating tank object.
'''
from python.structure.Components.dome_class import Dome
from python.structure.Components.cylinder_class import Cylinder
from python.structure.materials import materials as m
import numpy as np
from python.structure.constants import g_0, Km, Mi, Ku

class Tank:
    def __init__(self, outer_radius, pressure, material, thrust, volume, mass_p):
        self.outer_radius = outer_radius
        self.pressure = pressure
        self.thrust = thrust
        self.material = m[material]
        self.volume = volume
        self.mass_p = mass_p
        '''
        Tank object, containing all relevant parameters. 

        :param outer_radius: in m
        :param pressure: in Pa
        :param material: dictionary object from materials database (databases/materials.py)
        '''

        #NOTE:
        '''
        The hydrostatic pressure effect caused by propellant is accounted by multiplying by the
        highest estiamted T/W ration and divided by cross-section area
        For common bulkhead to account for compressive stress form the concave side of the dome additioanl factor of 2.0 is included
        This is deemded sufficient if the the convex side is pressurized first;
        '''
        self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
        self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_p*g_0*2.0/(np.pi*self.outer_radius**2), self.material)
        
        # Calculate cylinder height and create cylinder object
        cylinder_height = round((self.volume * Ku - self._dome_fwd.inner_volume - self._dome_aft.inner_volume) / (np.pi * self.outer_radius**2),3)
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
        return (self._dome_fwd.mass + Mi * 4 *np.pi * self.outer_radius**2 + self._dome_aft.mass + self._cylinder.mass + self._cylinder.insulation)*Km

    @property
    def height(self) -> float:
        return self._cylinder.height + self._dome_fwd.height + self._dome_aft.height
    
    @property
    def inner_volume(self) -> float:
        return self._dome_fwd.inner_volume + self._cylinder.inner_volume + self._dome_aft.inner_volume
  
