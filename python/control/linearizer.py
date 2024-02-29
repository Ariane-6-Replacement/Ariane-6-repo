import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline


def moment_eq(thrust, thrust_offset, moment_arm, mass_MOI):
    # Neglect aerodynamic forces for now
    M = -thrust * np.sin(thrust_offset) * moment_arm
    return M / mass_MOI


def force_eq(thrust, mass, gravity, theta, thrust_offset):
    dVxdt = 1 / mass * thrust * np.cos(theta + thrust_offset)
    dVzdt = 1 / mass * thrust * np.sin(theta + thrust_offset) - gravity
    return dVxdt, dVzdt


def gamma_derivative(Vx, Vz, thrust, mass, gravity, theta, thrust_offset):
    dVxdt, dVzdt = force_eq(thrust, mass, gravity, theta, thrust_offset)
    return (dVzdt * Vx - dVxdt * Vz) / (Vx**2 + Vz**2)


"""
Assumptions:
    - Rocket is always aligned with the velocity (theta = gamma)
        This could be achieved by thrusters on the upper part countering the moment
        or through clever manipulation of the aerodynamic forces
"""


# Define boundaries
thrust_offset_max = np.radians(15)
thrust_offset_min = np.radians(-15)
a_t = np.linspace(thrust_offset_min, thrust_offset_max, 100)

# Initial conditions
M = 900e3
g = 9.81
T = 5 * M * g
flight_path = np.linspace(np.radians(5), np.radians(85), 9)


# Linearize the system
ax = {}
az = {}
ax_at = {}
az_at = {}
for angle in flight_path:
    acceleration_x, acceleration_z = force_eq(T, M, g, angle, a_t)
    ax[angle] = acceleration_x
    az[angle] = acceleration_z

    axAt = CubicSpline(a_t, acceleration_x)  # Acceleration in x given a thrust offset
    azAt = CubicSpline(a_t, acceleration_z)  # Acceleration in z given a thrust offset
    ax_at[angle] = axAt
    az_at[angle] = azAt

if __name__ == '__main__':
    for i in range(len(flight_path)):
        plt.plot(np.degrees(a_t), ax[flight_path[i]], label=f'{np.round(np.degrees(flight_path[i]))}')
    plt.xlabel('Thrust offset [deg]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.legend()
    plt.title(r'Effect of thrust offset ($\pm$15 deg) on x-acceleration')
    plt.savefig('Effect of thrust offset on x-acceleration.pdf')
    plt.show()

    for i in range(len(flight_path)):
        plt.plot(np.degrees(a_t), az[flight_path[i]], label=f'{np.round(np.degrees(flight_path[i]))}')
    plt.xlabel('Thrust offset [deg]')
    plt.ylabel(r'Acceleration [m/s$^2$]')
    plt.legend()
    plt.title(r'Effect of thrust offset ($\pm$15 deg) on z-acceleration')
    plt.savefig('Effect of thrust offset on z-acceleration.pdf')
    plt.show()
