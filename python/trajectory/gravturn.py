import numpy as np
import sat_math_funcs as sm
from scipy.integrate import odeint

# constants  
g = 9.81 # m/s^2

def norm(r):
    return np.linalg.norm(r) 

def norm_array(r):
    r_norm = np.empty([len(r),1])
    for i in range(len(r)):
        r_norm[i] = norm(r[i])
    return r_norm

def gravity_accel(r):
    mu = 3.986004418*10**5
    r_norm = norm(r)
    r = np.array(r)
    A = (-mu/r_norm**3)*r
    A_mag = norm(A)
    return A,A_mag

#variables 
T = 20e6# thrust [N]
ISP = 400 # seconds
M = 565e3 # mass [kg]
psi = T/M*g #thrust load 

lat,lon,h =  5.167713, -52.683994, 0

r = sm.latlonhtoxyzwgs84(lat,lon,h)
vx = 0
vy = 1
vz = 10


init_state = [r[0],r[1],r[2],vx,vy,vz]





def system_of_odes(s, t, ISP, T,M0):
    r, v = s
    dmdt = -T/ISP
    M = M0
    M = M+dmdt 
    #D = 1/2 (rho *sm.norm(v)**2 * A * Cd )/m - v
    D = 0
    
    rx = r[0]
    ry = r[1]
    rz = r[2]

    vx = r[3]
    vy = r[4]
    vz = r[5]

    ax = sm.gravity_accel(r)[0]*rx+ T/M*vx + D
    ay = sm.gravity_accel(r)[0]*ry+ T/M*vy + D
    az = sm.gravity_accel(r)[0]*rz+ T/M*vz + D
    
    #a = sm.gravity_accel(r)[0]+ T/M*v + D
    
    return vx,vy,vz,ax,ay,az


time_points = np.linspace(0, 1, 180)

solutions = odeint(system_of_odes, s=init_state, t=time_points, args=(T, ISP, M))
rx_sol = solutions[:, 0]
ry_sol = solutions[:, 1]
rz_sol = solutions[:, 2]

vx_sol = solutions[:, 3]
vy_sol = solutions[:, 4]
vz_sol = solutions[:, 5]







x_dot_sol = solutions[:, 1]

import matplotlib.pyplot as plt 

plt.plot(time_points, ry_sol)
plt.plot(rx_sol, ry_sol)

plt.plot(time_points, x_dot_sol)