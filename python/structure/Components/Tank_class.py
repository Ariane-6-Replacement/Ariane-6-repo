'''
Code for creating tank object.
'''
from python.structure.Components.dome_class import Dome
from python.structure.Components.cylinder_class import Cylinder
from python.structure.materials import materials as m
import numpy as np
from python.structure.constants import g_0, Km

class Tank:
    def __init__(self, outer_radius, pressure, material, thrust, volume, mass_p):
        self.outer_radius = outer_radius
        self.pressure = pressure
        self.thrust = thrust
        self.material = m[material]
        self.volume = volume
        self.mass_p = mass_p
        '''
        outer radius: tank outer radius [m]
        pressure: MEOP [Pa]
        material: tank material [-]
        thrust: experience maximal thrust [N]
        volume: propellant volume [m^3]
        mass_P: propellant mass [kg]
        '''

      # Calculate dome_fwd and dome_aft directly within __init__
       
        self._dome_fwd = Dome(self.outer_radius, self.pressure, self.material)
        self._dome_aft = Dome(self.outer_radius, self.pressure +self.mass_p*g_0*1.5/(np.pi*self.outer_radius**2), self.material)
        
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
        #NOTE: 1.123 kg/m^2 comes from MER relation from Uniersity of Meryland, 4 *np.pi * self.outer_radius**2 assumes area of a sphere
        return (self._dome_fwd.mass + 1.123 * 4 *np.pi * self.outer_radius**2 + self._dome_aft.mass + self._cylinder.mass + self._cylinder.insulation)*Km

    @property
    def height(self) -> float:
        return self._cylinder.height + self._dome_fwd.height + self._dome_aft.height
    
    @property
    def inner_volume(self) -> float:
        return self._dome_fwd.inner_volume() + self._cylinder.inner_volume() + self._dome_aft.inner_volume()
  
