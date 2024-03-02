# -*- coding: utf-8 -*-
import numpy as np

class Aerodynamics:
    def __init__(self):
        pass

    
    def drag_noses(self,v, h):
        p, rho = self.pressure(h)
        F_f = 0.5 * self.A_fairing * self.cd_fairing  * rho * v**2
        F_n = 0.5 * self.A_nose * self.cd_nose * p * rho * v**2
        F = F_f + self.n_boosters * F_n
        return F
    
    def pressure(self,h):
        #Taken from https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
        
        if h < 11000:
            T = 15.04 - 0.00649 * h
            p = 101.29 * ((T+273.1)/288.08)**5.256
        
        if h > 25000:
            T = -131.21 + 0.00299 * h
            p = 2.488 * ((T+273.1)/216.6)**(-11.388)
            
        else:
            T = -56.46
            p = 22.65 * np.exp(1.73 - 0.000157 * h)
            
        rho = p / (0.2869 * (T + 273.1))
        return rho
    
    def set_noses(self,cd_fairing, D_upper, cd_nose, D_booster, n_boosters):
        self.cd_nose = cd_nose
        self.A_nose = 0.25 * np.pi * D_booster**2
        self.n_boosters = n_boosters
        self.cd_fairing = cd_fairing
        self.A_fairing = 0.25 * np.pi * D_upper**2
        
        
class fins:
    def __init__(self, t, w, h, Cla, Cd, n, arm):
        self.t = t
        self.w = w
        self.h = h
        self.Cla = Cla
        self.Cd  = Cd
        self.arm = arm
    
    def drag(self):
        pass
    
    def moment(self, AoA):
        pass
    
        
        
        