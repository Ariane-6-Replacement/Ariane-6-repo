import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import plotting_functions as pf
import sat_math_funcs as sm


def pressure(h):
    # Taken from https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html

    if h < 11000:
        T = 15.04 - 0.00649 * h
        p = 101.29 * ((T + 273.1) / 288.08) ** 5.256

    elif h > 25000:  # Changed to elif
        T = -131.21 + 0.00299 * h
        p = 2.488 * ((T + 273.1) / 216.6) ** (-11.388)

    else:
        T = -56.46
        p = 22.65 * np.exp(1.73 - 0.000157 * h)

    rho = p / (0.2869 * (T + 273.1))

    return rho

Me = 80e3
thrust = 1e6 
Nengines = 3
max_accel = Nengines*thrust/Me
Burn_alt = 3000 # [m]



def equations_of_motion(state, t):
    # Unpack state variables
    x, y, z, vx, vy, vz = state 
    
    # Define parameters (mass, gravitational constant, etc.)
    # You can define these according to your specific problem
    d = 5.4
    #rho = 101e3
    rho = pressure(z)
    Cd = 1
    A = np.pi * d**2/4  
    # D = (0.5* rho*sm.norm([vx,vy,vz]) * A * Cd)
    D = (0.5* rho*(vx**2+vz**2) * A * Cd)
    #D = 0

    gamma = np.arctan2(vz,vx)
    print(np.cos(gamma),np.sin(gamma))

    # Define derivatives of state variables
    dxdt = vx
    dydt = vy 
    dzdt = vz 
    dvxdt = -np.cos(gamma)*D/Me # Example: acceleration in x-direction
    dvydt = 0  # Example: acceleration in y-direction 
    dvzdt = -9.81 + np.sin(-gamma)*D/Me # Example: constant acceleration in z-direction due to gravity


    # print(gamma)
    return [dxdt, dydt, dzdt, dvxdt, dvydt, dvzdt]

# Define initial conditions
initial_state = [0, 0, 55e3,1600*2**0.5/2, 0, 1600*2**0.5/2]   # x,y,z,vx,vy,vz

# Define time points for integration
t = np.linspace(0, 300, 50000)  # Example: integrate from 0 to 10 seconds with 100 points

# Solve the equations of motion
solution = odeint(equations_of_motion, initial_state, t)

# Extract position and velocity from the solution
x, y, z, vx, vy, vz = solution.T


hitground = np.where(z<0)[0][0]
suicideburn = np.where(z<Burn_alt)[0][0]
t,x, y, z, vx, vy, vz = t[:hitground],x[:hitground], y[:hitground], z[:hitground], vx[:hitground], vy[:hitground], vz[:hitground]

x_suicide,z_suicide = x[suicideburn]/1000,z[suicideburn]/1000

# vx = sm.to_km_list(vx)
# vy = sm.to_km_list(vy)
# vz = sm.to_km_list(vz)

v_abs = np.empty([len(vx)])

for j in range(len(vx)):
    v_abs[j] = sm.norm([vx[j],vy[j],vz[j]])

print(v_abs[140])
print("downrange:", x[140])

fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # 2x2 grid of subplots

# Plot data on subplot 1
axs[0, 0].plot(t, sm.to_km_list((vx**2 + vz**2)**0.5), label='Speed')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Speed (km/s)')
axs[0, 0].set_title('Speed vs Time')
axs[0, 0].legend()

# Plot data on subplot 2
axs[0, 1].plot(t, sm.to_km_list(vx), label='vx')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Velocity x (km/s)')
axs[0, 1].set_title('Velocity x vs Time')
axs[0, 1].legend()

# Plot data on subplot 3
axs[1, 0].plot(sm.to_km_list(x), sm.to_km_list(z), label='z vs x')
axs[1, 0].set_xlabel('Distance x (km)')
axs[1, 0].set_ylabel('Distance z (km)')
axs[1, 0].plot(x_suicide,z_suicide, marker='o', markersize=8, color='red')
# axs[1, 0].set_xlim(0, 400e3)
# axs[1, 0].set_ylim(0, 100e3)
axs[1, 0].set_title('Trajectory (z vs x)')
axs[1, 0].legend()

# Plot data on subplot 4
axs[1, 1].plot(t, sm.to_km_list(vz), label='vz')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Velocity z (km/s)')
axs[1, 1].set_title('Velocity z vs Time')
axs[1, 1].legend()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()




# def plot1():
#     fig, axs = pf.creatfig(1,1,(10,5))
#     # axs.plot(sm.to_km_list(x),v_abs)
#     axs.plot(sm.to_km_list(x),sm.to_km_list(z))
#     # axs.plot(t,sm.to_km_list(z))
#     axs.set_xlabel("downrange [km]")
#     axs.set_ylabel("altitude [km]")
#     plt.ylim(0,110)
#     plt.xlim(0,500)
#
#     plt.show()
# plot1()
# pass

# Now x, y, z, vx, vy, vz contain the positions and velocities at each time step
