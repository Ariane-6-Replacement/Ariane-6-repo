import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import plotting_functions as pf
import sat_math_funcs as sm
from elysium_parameters import thrust, burntime, M0_1, M0, number_of_engines_ascent, number_of_engines_descent, diameter, Cd_ascent, Cd_descent, A, burn_alt, gravity_turn_alt, kick_angle, gamma_change_time, mass_flowrate
#from saturn_v_parameters import thrust, burntime, M0_1, M0, number_of_engines_ascent, number_of_engines_descent, diameter, Cd_ascent, Cd_descent, A, burn_alt, gravity_turn_alt, kick_angle, gamma_change_time, mass_flowrate

g_0 = 9.81 # [m / s^2]

class Trajectory():
    def __init__(self):
        self.kick_time = 0
        self.mass = M0_1

    # Taken from https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
    def get_density(self, h):
        if h < 11_000:
            T = 15.04 - 0.00649 * h
            p = 101.29 * ((T + 273.1) / 288.08) ** 5.256
        elif h < 25_000:
            T = -56.46
            p = 22.65 * np.exp(1.73 - 0.000157 * h)
        else:
            T = -131.21 + 0.00299 * h
            p = 2.488 * ((T + 273.1) / 216.6) ** -11.388

        rho = p / (0.2869 * (T + 273.1))
        return rho

    def get_drag(self, rho, velocity_x, velocity_z, A, Cd):
        drag = 0.5 * rho * (velocity_x ** 2 + velocity_z ** 2) * A * Cd
        return drag # 0
    
    def get_gamma(self, velocity_z, velocity_x):
        return np.arctan2(velocity_z, velocity_x)
    
    def get_speed(self):
        return np.sqrt(self.velocity_x ** 2 + self.velocity_z ** 2)

    def setup(self):
        self.pos_x = 0
        self.pos_z = 0
        self.velocity_x = 0
        self.velocity_z = 3
        self.accel_x = 0
        self.accel_z = 0

        self.pos_xs = np.array([])
        self.pos_zs = np.array([])
        self.velocity_xs = np.array([])
        self.velocity_zs = np.array([])
        self.accel_xs = np.array([])
        self.accel_zs = np.array([])
        self.thrust_xs = np.array([])
        self.thrust_zs = np.array([])
        self.rhos = np.array([])
        self.drags = np.array([])
        self.gammas = np.array([])
        self.masses = np.array([])
        self.speeds = np.array([])

        #c_eff = T / m
        #delta_V = c_eff * np.log(M0 / Me)

    def iterate(self, t, dt):
        rho = self.get_density(self.pos_z)

        ascending = self.velocity_z >= 0

        Cd = 0
        if ascending:
            Cd = Cd_ascent
        else:
            Cd = Cd_descent

        drag_force = self.get_drag(rho, self.velocity_x, self.velocity_z, A, Cd)
        gamma = self.get_gamma(self.velocity_z, self.velocity_x)

        self.thrust_x = 0
        self.thrust_z = 0

        number_of_engines = 1

        if self.pos_z >= gravity_turn_alt and self.kick_time == 0:
            self.kick_time = t

        if self.pos_z >= gravity_turn_alt and t <= self.kick_time + gamma_change_time:
            gamma = kick_angle

        if t < burntime:
            number_of_engines = number_of_engines_ascent
        elif self.pos_z < burn_alt and not ascending: 
            number_of_engines = number_of_engines_descent

        total_thrust = number_of_engines * thrust

        if t < burntime:
            self.mass = M0_1 - mass_flowrate * t
            self.thrust_x = np.cos(gamma) * total_thrust / self.mass
            self.thrust_z = np.sin(gamma) * total_thrust / self.mass

        if not ascending:
            self.mass = 80e3 # kg
            if self.pos_z < burn_alt:
                # TODO: Decrease mass when doing burn
                #self.mass =
                self.thrust_x = -np.cos(gamma) * total_thrust / self.mass
                self.thrust_z = -np.sin(gamma) * total_thrust / self.mass

        drag_x = -np.cos(gamma) * drag_force / self.mass
        drag_z = -np.sin(gamma) * drag_force / self.mass

        self.accel_x = self.thrust_x + drag_x
        self.accel_z = -g_0 + self.thrust_z + drag_z

        self.velocity_x += self.accel_x * dt
        self.velocity_z += self.accel_z * dt

        self.pos_x += self.velocity_x * dt
        self.pos_z += self.velocity_z * dt

        speed = self.get_speed()

        self.pos_xs = np.append(self.pos_xs, self.pos_x)
        self.pos_zs = np.append(self.pos_zs, self.pos_z)
        self.velocity_xs = np.append(self.velocity_xs, self.velocity_x)
        self.velocity_zs = np.append(self.velocity_zs, self.velocity_z)
        self.accel_xs = np.append(self.accel_xs, self.accel_x)
        self.accel_zs = np.append(self.accel_zs, self.accel_z)
        self.thrust_xs = np.append(self.thrust_xs, self.thrust_x)
        self.thrust_zs = np.append(self.thrust_zs, self.thrust_z)
        self.rhos = np.append(self.rhos, rho)
        self.drags = np.append(self.drags, drag_force)
        self.gammas = np.append(self.gammas, np.rad2deg(gamma))
        self.masses = np.append(self.masses, self.mass)
        self.speeds = np.append(self.speeds, speed)

        if self.pos_z < 0 or not ascending and abs(self.velocity_z) < 0.1:
            return False
        return True

    def run(self):

        self.setup()

        dt = 0.01

        times = np.array([])

        t_max = 500
        t = 0

        while t < t_max:
            t += dt
            times = np.append(times, t)
            success = self.iterate(t, dt)
            if not success:
                break

        print("Finished")

        fig, axs = plt.subplots(3, 5, figsize=(10, 8))  # 2x2 grid of subplots

        axs[0, 0].plot(times, self.pos_xs / 1000, label='x vs time')
        axs[0, 0].set_xlabel('Time (s)')
        axs[0, 0].set_ylabel('Pos x (km)')
        axs[0, 0].set_title('Pos (x vs time)')
        axs[0, 0].set_xscale('linear')
        axs[0, 0].set_yscale('linear')
        axs[0, 0].legend()

        axs[0, 1].plot(times, self.pos_zs / 1000, label='z vs time')
        axs[0, 1].set_xlabel('Time (s)')
        axs[0, 1].set_ylabel('Pos z (km)')
        axs[0, 1].set_title('Pos (z vs time)')
        axs[0, 1].set_xscale('linear')
        axs[0, 1].set_yscale('linear')
        axs[0, 1].legend()

        axs[0, 2].plot(times, self.rhos, label='rho')
        axs[0, 2].set_xlabel('Time (s)')
        axs[0, 2].set_ylabel('Rho (kg/m^3)')
        axs[0, 2].set_title('Rho vs Time')
        axs[0, 2].set_xscale('linear')
        axs[0, 2].set_yscale('linear')
        axs[0, 2].legend()
        
        axs[1, 3].plot(times, self.masses / 1000, label='mass')
        axs[1, 3].set_xlabel('Time (s)')
        axs[1, 3].set_ylabel('Mass (tonnes)')
        axs[1, 3].set_title('Mass vs Time')
        axs[1, 3].set_xscale('linear')
        axs[1, 3].set_yscale('linear')
        axs[1, 3].legend()

        axs[0, 3].plot(times, self.drags / 1e6, label='drag')
        axs[0, 3].set_xlabel('Time (s)')
        axs[0, 3].set_ylabel('Drag (MN)')
        axs[0, 3].set_title('Drag vs Time')
        axs[0, 3].set_xscale('linear')
        axs[0, 3].set_yscale('linear')
        axs[0, 3].legend()

        axs[1, 0].plot(times, self.velocity_xs / 1000, label='vx')
        axs[1, 0].set_xlabel('Time (s)')
        axs[1, 0].set_ylabel('Velocity x (km/s)')
        axs[1, 0].set_title('Velocity x vs Time')
        axs[1, 0].set_xscale('linear')
        axs[1, 0].set_yscale('linear')
        axs[1, 0].legend()

        axs[1, 1].plot(times, self.velocity_zs / 1000, label='vz')
        axs[1, 1].set_xlabel('Time (s)')
        axs[1, 1].set_ylabel('Velocity z (km/s)')
        axs[1, 1].set_title('Velocity z vs Time')
        axs[1, 1].set_xscale('linear')
        axs[1, 1].set_yscale('linear')
        axs[1, 1].legend()

        
        axs[2, 0].plot(times, self.accel_xs, label='ax')
        axs[2, 0].set_xlabel('Time (s)')
        axs[2, 0].set_ylabel('Accel x (m/s2)')
        axs[2, 0].set_title('Accel x vs Time')
        axs[2, 0].set_xscale('linear')
        axs[2, 0].set_yscale('linear')
        axs[2, 0].legend()

        axs[2, 1].plot(times, self.accel_zs, label='az')
        axs[2, 1].set_xlabel('Time (s)')
        axs[2, 1].set_ylabel('Accel z (m/s2)')
        axs[2, 1].set_title('Accel z vs Time')
        axs[2, 1].set_xscale('linear')
        axs[2, 1].set_yscale('linear')
        axs[2, 1].legend()
        
        axs[2, 2].plot(times, self.thrust_xs, label='tx')
        axs[2, 2].set_xlabel('Time (s)')
        axs[2, 2].set_ylabel('Thrust x (m/s2)')
        axs[2, 2].set_title('Thrust x vs Time')
        axs[2, 2].set_xscale('linear')
        axs[2, 2].set_yscale('linear')
        axs[2, 2].legend()

        axs[2, 3].plot(times, self.thrust_zs, label='tz')
        axs[2, 3].set_xlabel('Time (s)')
        axs[2, 3].set_ylabel('Thrust z (m/s2)')
        axs[2, 3].set_title('Thrust z vs Time')
        axs[2, 3].set_xscale('linear')
        axs[2, 3].set_yscale('linear')
        axs[2, 3].legend()

        axs[1, 2].plot(times, self.gammas, label='gamma')
        axs[1, 2].set_xlabel('Time (s)')
        axs[1, 2].set_ylabel('Gamma')
        axs[1, 2].set_ylim(-100, 100)
        axs[1, 2].set_title('Gamma vs Time')
        axs[1, 2].set_xscale('linear')
        axs[1, 2].set_yscale('linear')
        axs[1, 2].legend()
        
        axs[0, 4].plot(self.pos_xs / 1000, self.pos_zs / 1000, label='z')
        axs[0, 4].set_xlabel('X pos (km)')
        axs[0, 4].set_ylabel('Z pos (km)')
        axs[0, 4].set_title('Z pos vs X pos')
        axs[0, 4].set_xscale('linear')
        axs[0, 4].set_yscale('linear')
        axs[0, 4].legend()

        axs[1, 4].plot(times, self.speeds, label='speed')
        axs[1, 4].set_xlabel('Time (s)')
        axs[1, 4].set_ylabel('Speed (km/s)')
        axs[1, 4].set_title('Speed vs Time')
        axs[1, 4].set_xscale('linear')
        axs[1, 4].set_yscale('linear')
        axs[1, 4].legend()

        # axs[2, 0].plot(self.pos_xs / 1000, self.pos_zs / 1000, label='x')
        # axs[2, 0].set_xlabel('Distance x (km)')
        # axs[2, 0].set_ylabel('Distance z (km)')
        # axs[2, 0].set_title('Z vs X')
        # axs[2, 0].set_xscale('linear')
        # axs[2, 0].set_yscale('linear')
        # axs[2, 0].legend()

        plt.tight_layout()
        plt.show()

trajectory = Trajectory()
trajectory.run()