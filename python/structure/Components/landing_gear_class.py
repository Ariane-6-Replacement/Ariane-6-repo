'''
Code for creating landing gear object.
'''
import numpy as np
from python.structure.constants import Km
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
       
        Approach used is elaborated in detailed in DSE project raport "Cryogenic H2 and O2 propellant refuelling & transfer infrastructure in space" from 2022
        """
    @property
    def Lfp(self) -> float:
        #NOTE: Calculated using Two-Dimensional Inelastic Impact Theory
        Lfp = 0.1 #Radius of landing gear 
        Dh = 2.0 #Distance between the end of nozzle and the ground, from analyzing landing gear from Falcon 9 
        H0 = self.cg + 1.8 + Dh #Distance of the CG from the ground, assumption: engine sticks out 1.8 meters from the engine bay;
        alpha = 35 #Tip over angle for lunar landers of Apollo Missions, source: NASA 

        I = self.mass * (self.outer_radius)**2 #Conservative assumption: Rocket is a solid rod 
        
        while np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(self.mass + (2*Lfp**2+H0**2))/I) > np.sqrt(H0**2 + Lfp**2) - H0:
            Lfp+=0.1

        return Lfp




    @property
    def LG_geometry(self) -> tuple:
        Dh = 2.0 #Distance between the end of nozzle and the ground, from analyzing landing gear from Falcon 9 
        x = self.Lfp - self.outer_radius #Horizonatal distance between the leg and the edge of the LV
        drop_h = 0.2 #Maximal veritcal stroke of the suspenion, assumed
        ys = 1.8 + drop_h + Dh #Height of the attachment point of the secondary strut with the leg deplopyed, fully extended (0 stroke)
        Ls = np.sqrt(x**2 + ys**2) #Length of the secondary strut
        tau_p = 25 #Primary strut angle from "PRELIMINARY DESIGN OF REUSABLE LUNAR LANDER LANDING SYSTEM" by Rusty Goh Weixiong

        yp = x / np.tan( np.radians( tau_p ) ) #Height of the attachment point of the primary strut with the leg deplopyed, fully extended (0 stroke)

        Lp = np.sqrt(x**2 + yp**2) #Length of the primary strut
     
        return Lp, Ls


    @property
    def mass_gear(self) -> float:
        rho= 13.91187 * Km #The value was calulated using data provided by Almatec - a company designign landing gear for Themis Project
        mass_p = rho * self.LG_geometry[0]
        mass_s = rho * self.LG_geometry[1]

        #NOTE:
        '''
        Assumption: the hydraulic system + all metal components per leg weight 250 kg max; If better data is available, it is recommended;
        Design Decision: Tripod landing gear configuration with 4 legs
        '''
        return (mass_p + 2 * mass_s + 250) * 4
    

