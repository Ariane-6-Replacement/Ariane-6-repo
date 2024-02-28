from scipy.integrate import odeint
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np


"""
Assumptions:
    - Neglect aerodynamic forces (only thrust and weight)
    - Consider thrust and mass constant in magnitude
    - Constant gravity

Control variable:
    - Thrust offset
    
Momentum equilibrium:
    I d^2 (theta) / dt^2 = -T * sin(at)

Force equilibrium:
    M dV_x/dt = T * cos(theta - at)
    M dV_y/dt = T * sin(theta - at) - M * g
    
Other equations:
    gamma = Vz / Vx
"""


def angular_acceleration(at, thrust, I):
    return -thrust / I * np.sin(at)


# Time considered
dt = 1e-2
time = np.arange(0, 100, dt)

# Target value
theta_target = np.ones(len(time)) * np.pi / 4  # Assume we want to fly straight at a 45 deg angle for now

# Initial conditions
theta = [np.pi / 2]                 # rocket orientation
w = 0                               # anugular speed
at = 0                              # thrust offset
mass = 100                          # mass
gravity = 9.81                      # gravity
moment_of_inertia = 10              # mass moment of inertia
thrust = 5 * gravity * mass         # thrust

Vz = (thrust / mass - gravity) * dt
Vx = Vz / np.tan(np.radians(80))    # Initial gamma = 80 deg
gamma = [np.arctan(Vz / Vx)]        # flight-path angle

# Start simulation
Kp = 0.5
Ki = 0.0
Kd = 0.0
for i in range(len(time)):
    error = theta_target[i] - theta[i]
    at -= error * Kp * dt

    a = angular_acceleration(at, thrust, moment_of_inertia)
    w += a * dt
    theta.append(theta[i] + w * dt)

    Vx += thrust * np.cos(theta[i] - at) * dt
    Vz += thrust * np.sin(theta[i] - at) * dt
    gamma.append(np.arctan(Vz / Vx))

plt.plot(time, gamma[1:], 'b-')
plt.plot(time, theta[1:], 'g-')
plt.plot(time, theta_target, 'r:')
plt.show()
