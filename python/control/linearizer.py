import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline, griddata


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
a_t = np.linspace(thrust_offset_min, thrust_offset_max, 180)

# Initial conditions
M = 900e3
g = 9.81
T = 5 * M * g
flight_path = np.linspace(0, np.pi/2, 180)


### Linearize the system ###
a_grid, gamma_grid = np.meshgrid(a_t, flight_path)
ax = 1 / M * T * np.cos(gamma_grid + a_grid)
az = 1 / M * T * np.sin(gamma_grid + a_grid) - g

# linearized_system_x = griddata((a_grid.flatten(), gamma_grid.flatten()), ax.flatten(), (a_grid, gamma_grid), method='cubic')
# linearized_system_z = griddata((a_grid.flatten(), gamma_grid.flatten()), az.flatten(), (a_grid, gamma_grid), method='cubic')



if __name__ == '__main__':
    plt.imshow(ax, cmap='seismic', vmax=np.max(np.abs(ax)), vmin=-np.max(np.abs(ax)))
    # Adapt x axis
    locs, labels = plt.xticks()
    labs = np.linspace(np.round(np.degrees(np.min(a_t))), np.round(np.degrees(np.max(a_t))), len(locs), dtype=int)
    plt.xticks(np.linspace(0, 180, len(locs), dtype=int), labs)
    # Adapt y axis
    locs, labels = plt.yticks()
    labs = np.linspace(np.round(np.degrees(np.min(flight_path))), np.round(np.degrees(np.max(flight_path))), len(locs), dtype=int)
    plt.yticks(np.linspace(0, 180, len(locs), dtype=int), labs)
    plt.xlabel('Thrust offset [deg]')
    plt.ylabel('Flight path angle [deg]')
    plt.colorbar()
    plt.title(r'Horizontal acceleration [m/s$^2$]')
    plt.savefig('Effect of thrust offset on x-acceleration.pdf')
    plt.show()

    plt.imshow(az, cmap='seismic', aspect='equal', vmax=np.max(np.abs(az)), vmin=-np.max(np.abs(az)))
    # Adapt x axis
    locs, labels = plt.xticks()
    labs = np.linspace(np.round(np.degrees(np.min(a_t))), np.round(np.degrees(np.max(a_t))), len(locs), dtype=int)
    plt.xticks(np.linspace(0, 180, len(locs), dtype=int), labs)
    # Adapt y axis
    locs, labels = plt.yticks()
    labs = np.linspace(np.round(np.degrees(np.min(flight_path))), np.round(np.degrees(np.max(flight_path))), len(locs),
                       dtype=int)
    plt.yticks(np.linspace(0, 180, len(locs), dtype=int), labs)
    plt.xlabel('Thrust offset [deg]')
    plt.ylabel('Flight path angle [deg]')
    plt.colorbar()
    plt.title(r'Vertical acceleration [m/s$^2$]')
    plt.savefig('Effect of thrust offset on z-acceleration.pdf')
    plt.show()
