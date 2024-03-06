
from isogrid_stress import critical_stress
import numpy as np
from materials import materials as m
class Shell:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 height:float
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
    @property
    def insulation(self):
        return self.height*self.outer_radius*2*np.pi*1.123

    @property
    def mass(self):
        s=0
        t=0.002
        while s/self.material['yield_stress']<3:
            print('IN')
            t+=0.0005
            s, t_mass = critical_stress(t, self.outer_radius, self.material['youngs_modulus'])

        print('Tmass', t_mass)
        return 2*self.outer_radius*np.pi*self.height*t_mass*self.material['density']
    # +self.insulation
  

# if __name__ in "__main__":
#     tank_test = Shell(2.5,'2195',2)
#     print('DONE')
#     print('Output: ',tank_test.mass)
#     print('FINISHED')