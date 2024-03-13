import numpy as np
import matplotlib.pyplot as plt


def eom(effective_thrust, mass, gamma, v):
    g0 = 9.81
    dVdt = effective_thrust / mass - 9.81 * np.sin(gamma)
    dGdt = 1 / v * -g0 * np.cos(gamma)
    return dVdt, dGdt



# Data
g0 = 9.81
c_eff = 400 * g0
dt = 1e-2
thrust = 22e6



# Initial condition
gamma = [np.radians(80)]
position = np.array([[0, 1e4]])
velocity = 340 * np.array([[np.cos(gamma[-1]), np.sin(gamma[-1])]])

safety_factor = 1.5
total_prop = 565e3
landing_fraction = 0.15
propellant_mass = (1-landing_fraction)*total_prop
dry_mass = safety_factor*(45e3 + 0.1*total_prop)
total_mass = propellant_mass + dry_mass

burn_time = c_eff / (thrust / total_mass) * (1 - 1 / (total_mass/dry_mass))
dm = propellant_mass / burn_time

burnout = False
while gamma[-1] > 0:
    dV, dG = eom(effective_thrust=thrust,
                 mass=total_mass,
                 gamma=gamma[-1],
                 v=np.linalg.norm(velocity[-1]))

    gamma.append(gamma[-1] + dG * dt)
    new_v = np.linalg.norm(velocity[-1]) + dV * dt
    velocity = np.vstack((velocity, new_v * np.array([np.cos(gamma[-1]), np.sin(gamma[-1])]).flatten()))
    position = np.vstack((position, position[-1] + velocity[-1] * dt))

    if propellant_mass - dm * dt > 0:
        propellant_mass -= dm * dt
        total_mass -= dm * dt
    elif not burnout:
        print('Burnout position = ', position[-1] / 1e3)
        print('Velocity = ', np.linalg.norm(velocity[-1]) / 1e3)
        print('Orientation = ', np.degrees(gamma[-1]))
        thrust = 0
        burnout = True


print('Propellant mass = ', propellant_mass)
print('Velocity = ', np.linalg.norm(velocity[-1]) / 1e3)
plt.plot(position[:, 0] / 1e3, position[:, 1] / 1e3)
plt.xlabel('X position [km]')
plt.ylabel('Z position [km]')
plt.tight_layout()
plt.show()



plt.plot(position[:, 0] / 1e3, np.linalg.norm(velocity, axis=1).reshape(-1, 1) / 1e3)
plt.xlabel('X position [km]')
plt.ylabel('Velocity [km/s]')
plt.tight_layout()
plt.show()