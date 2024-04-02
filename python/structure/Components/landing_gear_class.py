import numpy as np
class LG:
    def __init__(self,
                 outer_radius: float,
                 mass: float,
                 cg: float):

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
        alpha = 23# Ask Thomas for source deg
        I = self.mass * (self.outer_radius)**2 
        
        while np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) > np.sqrt(H0**2 + Lfp**2) - H0:
            print(f'Left {np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) }')
            print(f'Right {np.sqrt(H0**2 + Lfp**2) - H0}')
            Lfp+=0.1
            print(f'Left2 {np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) }')
        return Lfp




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


    @property
    def mass_gear(self) -> float:
        rho= 13.91187 * 1.2


        mass_p = rho * self.LG_geometry[0]
        mass_s = rho * self.LG_geometry[1]

        return (mass_p + 2 * mass_s + 250) * 4
    
# test bit 
# if __name__ == "__main__":
#     mass = 330000
#     test = LG(2.7,mass, 15)
#     print(f'Lg.mass {test.Lfp}')
