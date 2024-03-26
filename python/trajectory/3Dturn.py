import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import plotting_functions as pf
import sat_math_funcs as sm

def pressure(h):
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






def equations_of_motion(state, t):
    # Unpack state variables
    x, y, z, vx, vy, vz = state 
    
    # Define parameters (mass, gravitational constant, etc.)
    # You can define these according to your specific problem
    d = 5.4
    rho = 101e3
    rho = pressure(z)
    Cd = 0.2
    A = np.pi * d**2/4  
    D = (0.5* rho*sm.norm([vx,vy,vz]) * A * Cd)


    gamma = np.arctan2(vx,vz)

    # Define derivatives of state variables
    dxdt = vx
    dydt = vy 
    dzdt = vz 
    dvxdt = -np.cos(gamma)*D/768e3 # Example: acceleration in x-direction
    dvydt = 0  # Example: acceleration in y-direction 
    dvzdt = -9.81 - np.sin(gamma)*D/768e3 # Example: constant acceleration in z-direction due to gravity
    
    return [dxdt, dydt, dzdt, dvxdt, dvydt, dvzdt]

# Define initial conditions
initial_state = [0, 0, 100e3, 2.5e3, 0, 0]  # x,y,z,vx,vy,vz

# Define time points for integration
t = np.linspace(0, 200, 1000)  # Example: integrate from 0 to 10 seconds with 100 points

# Solve the equations of motion
solution = odeint(equations_of_motion, initial_state, t)

# Extract position and velocity from the solution
x, y, z, vx, vy, vz = solution.T

# vx = sm.to_km_list(vx)
# vy = sm.to_km_list(vy)
# vz = sm.to_km_list(vz)

v_abs = np.empty([len(vx)])

for j in range(len(vx)):
    v_abs[j] = sm.norm([vx[j],vy[j],vz[j]])

#print(v)
def plot1():
    fig, axs = pf.creatfig(1,1,(20,5))
    #axs.plot(sm.to_km_list(x),v_abs)
    axs.plot(sm.to_km_list(x),sm.to_km_list(z))
    axs.set_xlabel("downrange [km]")
    axs.set_ylabel("altitude [km]")
    plt.ylim(0,110)
   

    plt.show()
plot1()

# Now x, y, z, vx, vy, vz contain the positions and velocities at each time step
