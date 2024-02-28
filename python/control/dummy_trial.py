from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np


"""
Equations of motion:
dV_x/dt     = 1/M ( T cos(theta + a_t) - L sin(gamma) - D cos(gamma) )
dV_z/dt     = 1/M ( T sin(theta + a_t) + L cos(gamma) - D sin(gamma) - g )
dTheta/dt   = 1/r dV_p/dt - V_p / r^2 dr/dt

gamma = arctan(Vz / Vx)
theta = gamma + alpha

Assumptions:
    - alpha = 0
    - L = 0
    - D = 0
    - constant T
    - constant g
    - constant mass
    - constant speed

EoM:
dV_x/dt = 1/M * T cos(theta + a_t) 
dV_z/dt = 1/M * T sin(theta + a_t) - g 
"""


def desired_trajectory(x):
    return 20*np.log(x+1)


def gamma_trajectory(t):
    return np.arctan(120 / (t + 6))


def gamma_traj_der(t):
    return -120 / (t**2 + 12*t + 14436)


def gamma_derivative(x, t, mass, g, thrust, theta, Vx, Vz):
    dVxdt = 1 / mass * thrust * np.cos(theta + x)
    dVzdt = 1 / mass * thrust * np.sin(theta + x) - g

    dGdt = 1 / (1 + theta**2) * (dVxdt * Vz - Vx * dVzdt) / Vz**2
    return dGdt


# Initial conditions
Vx = 0
Vz = 0
g = 9.81
mass = 9e5
theta = np.pi/2
thrust = 5 * mass * g

# Control variable
at = 0
time = np.linspace(0, 600, 1000)
for i in range(len(time)):




x = np.linspace(0, 100, 1000)
z = desired_trajectory(x)
G = gamma_trajectory(time)

# Plot results
fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(x, z, label='trajectory')
ax1.set_xlabel('x')
ax1.set_ylabel('z')
ax2.plot(time, x, label=r'V$_x$')
ax2.plot(time, z, label=r'V$_z$')
ax2.legend()
ax2.set_xlabel('t')
ax2.set_ylabel('coord')
ax3.plot(time, np.degrees(G), 'g', label=r'$\gamma$')
# ax3.plot(time, gamma_traj_der(time), label=r'd$\gamma$/dt')
ax3.plot()
ax3.set_xlabel('t')
ax3.set_ylabel(r'$\gamma$')
ax3.legend()
plt.show()


