
from python.structure.Loading.isogrid_stress import critical_stress
from python.structure.materials import materials as m
from python.structure.geometry import cylindrical_shell_I
from python.structure.Loading.axial_stress import s_axial
from python.structure.constants import FOS_ITS
import numpy as np

class Shell:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 height:float,
                 thrust:float
                 ):
        """
        Inter Tank Stage object, containing all relevant parameters.
        :param outer_radius: in m
        :param height: in m
        :param thrust: in N
        :param material: dictionary object from materials database
        """

        self.outer_radius = outer_radius
        self.material = m[material]
        self.height = height
        self.thrust = thrust

        

    @property
    def mass(self):
      
        s_crit=0   #Initial Critical Buckling Stress
        t=0.002   #Inital Shell thickness - 
        s_max = 1
        while s_crit / s_max < FOS_ITS:

            if t>0.025:

                raise ValueError #Check for excessive thickness of the ITS
            
            s_crit, t_mass = critical_stress(t, self.outer_radius, self.material['youngs_modulus'])

            I = cylindrical_shell_I(self.outer_radius, t_mass) 

            #NOTE: Moment magnitude is assumed to be 2/3 of the thrust magnitude; If better modelling is available, change of this value is recommneded; 
            s_max = (s_axial(t_mass, self.outer_radius,1.0,self.thrust) + self.thrust*(2/3) * self.outer_radius / I)

            t += 0.0005
        
        return 2 * self.outer_radius * np.pi * self.height * t_mass * self.material['density']

  
#NOTE: UNIT TESTING 
# if __name__ == "__main__":
#     tank_test = Shell(2.5, '2195',2, 10E9)
#     print('DONE')
#     print('Output: ',tank_test.mass)
#     print('FINISHED')