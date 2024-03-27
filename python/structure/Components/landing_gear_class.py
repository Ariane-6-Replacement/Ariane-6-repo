import  numpy  as np
class LG:
    def __init__(self,
                 outer_radius: float,
                 mass: float,
                 cg: float):
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
        self.mass = mass
        self.cg = cg

    @property
    def Lfp(self) -> float:
        '''H0 - height of the center of gravity with respect to the ground in m
        alpha - turn over angle in deg
        Lfp - landing gear radius in m
        '''
        # print('alpha', np.radians(alpha))
        Lfp = 0.1
        Dh = 2.0 # Analyzing landing gear from Falcon 9 
        H0 = self.cg + 1.8 + Dh
        alpha = 17 # Ask Thomas for source deg
        while np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) > np.sqrt(H0**2 + Lfp**2) - H0:
            Lfp+=0.1
        return Lfp

# test bit 
# if __name__ == "__main__":
#     H0 = 6.5
#     alpha = 40
#     mass = 33000
#     I = 2500000
#     Lfp = LG_stability(H0,alpha,mass,I)
#     print("LFP: ", Lfp)



    @property
    def LG_geometry(self) -> tuple:
        '''Lw - width of the lander
        tau_p - primary strut angle
        tau_s - secondary strut angle
        x - width beyonf the lander frame
        z - height of the top attachemnt point 
        Lp - length of the primary strut
        hH - height of the primary strut with respect to the lander
        Ls - length of the secondary strut
        drop_h - vertical stroke limit '''
        Lfp = 0.1
        Dh = 2.0 # Analyzing landing gear from Falcon 9 
        x = self.Lfp - self.outer_radius
        ys = 1.8 + Dh
        # H0 = self.cg 
        Ls = np.sqrt(x**2 + ys**2)
        tau_p = 25

        yp = x / np.tan( np.radians( tau_p ) )

        Lp = np.sqrt(x**2 + yp**2)

        # hP = np.sin(np.radians( tau_s - tau_p)) * Lp / 2 * 1/ np.sin(np.radians(tau_s))

        
        # S_p_max = Lp - (z - drop_h) / np.cos(np.radians(tau_p))

        # #SHADY SHIT as fuck 
        # S_s_max = 0.2 * Ls

        return Lp, Ls
