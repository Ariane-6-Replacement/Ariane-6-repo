import numpy as np
class LG:
    def __init__(self,
                 outer_radius: float,
                 mass: float,
                 cg: float):

        self.outer_radius = outer_radius
        self.mass = mass
        self.cg = cg
        """
        Landing gear object, containing all relevant parameters. 

        :param outer_radius: in m
        :param mass: in Pa
        :param material: dictionary object from materials database (databases/materials.py)
       
        """
    @property
    def Lfp(self) -> float:

        '''H0 - height of the center of gravity with respect to the ground in m
        alpha - turn over angle in deg
        Lfp - landing gear radius in m
        '''
        Lfp = 0.1
        Dh = 2.0 # Analyzing landing gear from Falcon 9 
        H0 = self.cg + 1.8 + Dh
        alpha = 35
        I = self.mass * (self.outer_radius)**2 
        
        while np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) > np.sqrt(H0**2 + Lfp**2) - H0:
            Lfp+=0.1
        print(f'Lfp {Lfp}')
        return Lfp




    @property
    def LG_geometry(self) -> tuple:
        '''Lw - width of the lander
        tau_p - primary strut angle
        x - width beyond the LV frame
        Lp - length of the primary strut
        Ls - length of the secondary strut
        drop_h - vertical stroke limit '''
        Dh = 2.0 # Analyzing landing gear from Falcon 9 
        x = self.Lfp - self.outer_radius
        drop_h = 0.2
        ys = 1.8+ drop_h + Dh
        Ls = np.sqrt(x**2 + ys**2)
        tau_p = 25 #deg

        yp = x / np.tan( np.radians( tau_p ) )

        Lp = np.sqrt(x**2 + yp**2)
        # print(f'Lp {Lp}, Ls {Ls}')
        return Lp, Ls


    @property
    def mass_gear(self) -> float:
        rho= 13.91187 * 1.2
        mass_p = rho * self.LG_geometry[0]
        mass_s = rho * self.LG_geometry[1]
        return (mass_p + 2 * mass_s + 250) * 4
    
# test bit 
# if __name__ == "__main__":
#     mass = 6258.0080096848815

#     cg=  5.273065608372961

#     test = LG(2.5,mass,cg)
#     print(f'Lg.mass {test.LG_geometry}, {test.Lfp}, {test.mass_gear}')
