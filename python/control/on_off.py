import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.interpolate import CubicSpline


def force_eq(thrust, mass, gravity, ax0=0, ay0=0):
    thrust_x, thrust_z = thrust
    ax = thrust_x / mass - ax0
    az = thrust_z / mass - gravity - ay0
    return ax, az


def trajectory(t):
    x = t**2/6
    z = 20*np.log(x + 1)
    return x, z


# Define the trajectory
dt = 0.01
t = np.arange(0, 120, dt)
x, z = trajectory(t)
target_trajectory = CubicSpline(x, z)
# gamma = np.arctan(target_trajectory.derivative())

# Properties
mass = 100
g = 9.81

# Initial conditions
x_coord = [0]
z_coord = [0]
vx = 0
vz = 0
thrust = np.array([0, 0])
for i in range(len(t)-1):
    # Where do we want to go?
    target_position = np.array([x[i+1], z[i+1]])

    # What velocity do we need to get there in dt seconds?
    velocity = (target_position - np.array([x_coord[-1], z_coord[-1]])) / dt

    # What is the force we need to apply to get there?
    delta_v = velocity - np.array([vx, vz])
    ax, az = delta_v / dt

    sol = fsolve(force_eq, np.array([1, 1.1*mass*g]), args=(mass, g, ax, az))
    Tx, Tz = sol

    # Introduce disturbances

    # Update current condition
    ax, az = force_eq((Tx, Tz), mass, g)
    vx += ax * dt
    vz += az * dt
    x_coord.append(x_coord[-1] + vx * dt)
    z_coord.append(z_coord[-1] + vz * dt)

    thrust = np.vstack((thrust, np.array([Tx, Tz])))

thrust = np.hstack((thrust, np.hstack((np.linalg.norm(thrust, axis=1).reshape(-1, 1),
                                       np.arctan(thrust[:, 1]/thrust[:, 0]).reshape(-1, 1)))))

plt.plot(x, z, 'r--')
plt.plot(x_coord, z_coord, 'b-')
plt.legend(['Target', 'Real'])
plt.show()

plt.plot(t, thrust[:, :-1])
plt.legend([r'T$_x$', r'T$_z$', r'T$_{total}$'])
plt.xlabel('Time [s]')
plt.ylabel('Thrust [N]')
plt.show()


