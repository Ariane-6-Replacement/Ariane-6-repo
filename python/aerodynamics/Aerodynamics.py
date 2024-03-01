# -*- coding: utf-8 -*-
import numpy as np

class Aerodynamics:
    def __init__(self, noses_input, fins_input, gridfins_input, parachutes_input, moments):
        #Input variables are 2D matrices with all variables in columns so rows = number of structures
        fairing = nose(noses_input[0,0],noses_input[0,1])
        structures_ascent = [fairing]
        structures_descent = []
        for i in range(1, len(noses_input)):
            structures_ascent.append(nose(noses_input[i,0],noses_input[i,1]))
        for i in range(len(fins_input)):
            structures_ascent.append(fin(fins_input[i,0],fins_input[i,1],fins_input[i,2],fins_input[i,3],fins_input[i,4],fins_input[i,5],fins_input[i,6]))
        for i in range(len(gridfins_input)):
            structures_descent.append(gridfin(gridfins_input[i,0],gridfins_input[i,1]))
        for i in range(len(parachutes_input)):
            structures_descent.append(parachute(parachutes_input[i,0]))
        self.structures_ascent = structures_ascent
        self.structures_descent = structures_descent
            
        
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
    
    def drag(self, h,v, descent = True):
        rho = self.pressure(h)
        F = 0
        for struc in self.structures_ascent:
            F += struc.drag(v, rho)
        if descent == True:
            for struc in self.structures_descent:
                F += struc.drag(v, rho)
        return F
        

class nose:
    def __init__(self, D, cd):
        self.cd = cd #0.2 https://www.researchgate.net/figure/Drag-coefficient-C-D-of-blunt-nose-upper-part-and-rounded-nose-lower-part_fig2_275887347
        self.A = 0.25 * np.pi * D**2

    def drag(self,v, rho):
       
        F = 0.5 * self.A * self.cd  * rho * v**2
        return F            
        
class fin:
    def __init__(self, t, w, h, Cla, Cd, n, arm):
        self.t = t #Thickness
        self.w = w #Length along body
        self.h = h #Length sticking out
        self.Cla = Cla
        self.Cd  = Cd
        self.arm = arm
    
    def drag(self, v, rho):
        F = 0.5 * self.t * self.h * self.cd  * rho * v**2
        return F
    
    def moment(self, AoA):
        pass
    
class parachute:
    def __init__(self,r):
        self.A = np.pi * r**2
        self.cd = 1.75 #https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/rktvrecv.html#:~:text=The%20air%20density%20has%20a,produces%20a%20lower%20terminal%20velocity.
        
    def drag(self,rho,v):
        F = 0.5 * self.A* self.cd  * rho * v**2
        return F
    
class speedbrake:
    def __init__(self,w,h,a):
        self.A = w * h * np.sin(a)
        self.cd = 1.5 #Estimation, need to add w/h dependency
        
    def drag(self,rho,v):
        F = 0.5 * self.A* self.cd  * rho * v**2
        return F 
    
class gridfin: ##TBD
    def __init__(self,w,h,a):
        self.A = w * h * np.sin(a)
        self.cd = 1.5 #Estimation, need to add w/h dependency
        
    def drag(self,rho,v):
        F = 0.5 * self.A* self.cd  * rho * v**2
        return F      
             
        
        