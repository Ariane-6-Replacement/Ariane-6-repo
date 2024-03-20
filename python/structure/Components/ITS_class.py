
from python.structure.Loading.isogrid_stress import critical_stress
from python.structure.materials import materials as m
from python.structure.geometry import cylindrical_shell_I
from python.structure.Loading.axial_stress import s_axial
from python.structure.constants import FOSY
import numpy as np

class Shell:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 height:float,
                 thrust:float
                 #moment:float
                 ):
        """
        Cylinder object, containing all relevant parameters. Cylinder coordinate system is defined with the origin at the
        center of the bottom edge. The z_c axis moves along the cylinder's axis in the direction from aft to forward.
        :param outer_radius: in m
        :param thickness: in m
        :param height: in m
        :param material: dictionary object from materials database
        """

        # These are the parameters that are passed to the class:
        self.outer_radius = outer_radius
        self.material = m[material]
        self.height = height
        self.thrust = thrust
       # self.moment = moment
        
    @property
    def insulation(self):
        return self.height * self.outer_radius * 2 * np.pi * 1.123

    @property
    def mass(self):
        s=0
        t=0.002
        loop_limit = 100_000
        i = 0
        while s / self.material['yield_stress'] < 2.0 and i < loop_limit:
            t += 0.0005
            s, t_mass = critical_stress(t, self.outer_radius, self.material['youngs_modulus'])
            I = cylindrical_shell_I(self.outer_radius, t_mass)
            s = s_axial(t_mass, self.outer_radius,FOSY, self.thrust) + self.thrust/2 * self.outer_radius / I
            i += 1
        return 2 * self.outer_radius * np.pi * self.height * t_mass * self.material['density']
    # +self.insulation
  

if __name__ == "__main__":
    tank_test = Shell(2.5, '2195', 2, 11E6)
    print('DONE')
    print('Output: ',tank_test.mass)
    print('FINISHED')