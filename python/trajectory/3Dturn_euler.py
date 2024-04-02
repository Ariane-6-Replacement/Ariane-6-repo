import numpy as np
import matplotlib.pyplot as plt
from elysium_parameters import thrust, burntime, M0_1, number_of_engines_ascent, number_of_engines_landing, number_of_engines_reentry, diameter, Cd_ascent, Cd_descent, A, reentry_burn_alt, landing_burn_alt, gravity_turn_alt, kick_angle, gamma_change_time, mass_flowrate, M_empty, struct_coeff_2nd_stage, I_sp_1, I_sp_2, delta_V_landing, delta_V_reentry
#from saturn_v_parameters import thrust, burntime, M0_1, number_of_engines_ascent, number_of_engines_descent, diameter, Cd_ascent, Cd_descent, A, burn_alt, gravity_turn_alt, kick_angle, gamma_change_time, mass_flowrate

g_0 = 9.81 # [m / s^2]
R_earth = 6_371e3 # [m]
mu_earth = 3.986_004_418e14 # [m^3 / s^-2]

class Trajectory():
    def __init__(self):
        self.kick_time = 0
        self.mass = M0_1
        self.orbits = {
            'LEO': 300e3
        }

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
    
    def get_propellant(self, I_sp_1, delta_V, M_remaining):
        propellant = np.exp(delta_V / (I_sp_1 * g_0)) * (M_empty + M_remaining) - (M_empty + M_remaining)
        return propellant
    
    def get_speed(self, velocity_x, velocity_z):
        return np.sqrt(velocity_x ** 2 + velocity_z ** 2)
    
    def delta_V_circularize(self, r_1, r_2):
        return np.sqrt(mu_earth / r_2) * (1 - np.sqrt(2 * r_1 / (r_1 + r_2)))

    def delta_V_circular_to_elliptical(self, r_1, r_2):
        return np.sqrt(mu_earth / r_1) * (np.sqrt(2 * r_2 / (r_1 + r_2)) - 1)

    def delta_V_circular_to_circular(self, r_1, r_2):
        delta_V_1 = self.delta_V_circular_to_elliptical(r_1, r_2)
        delta_V_2 = self.delta_V_circularize(r_1, r_2)
        return delta_V_1 + delta_V_2
    
    def get_delta_V_total(self, pos_z, speed):
        altitude = R_earth + pos_z
        v_c1 = np.sqrt(mu_earth / (altitude + R_earth))
        delta_V_circ = v_c1 - speed

        available_delta_v = g_0 * I_sp_2 * np.log(1 / (1 - struct_coeff_2nd_stage))

        print("Available Delta V:", available_delta_v)

        GTO_p = R_earth + 250e3 # [m]
        GTO_a = R_earth + 22_500e3 # [m]

        required_delta_V = delta_V_circ + self.delta_V_circular_to_circular(altitude, GTO_p) + self.delta_V_circular_to_elliptical(GTO_p, GTO_a)

        print("Required Delta V:", required_delta_V)

        return required_delta_V

    def setup(self):
        self.pos_x = 0
        self.pos_z = 0
        self.velocity_x = 0
        self.velocity_z = 3
        self.accel_x = 0
        self.accel_z = 0
        self.M_prop_landing = self.get_propellant(I_sp_1, delta_V_landing, 0)
        self.M_prop_reentry = self.get_propellant(I_sp_1, delta_V_reentry, self.M_prop_landing)

        print("Propellant available for re-entry:", self.M_prop_reentry)
        print("Propellant available for landing:", self.M_prop_landing)

        self.landing_burn_start_time = 0
        self.reentry_burn_start_time = 0

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

        if ascending and t < burntime:
            number_of_engines = number_of_engines_ascent
        elif not ascending:
            if self.pos_z < landing_burn_alt: 
                number_of_engines = number_of_engines_landing
                if self.landing_burn_start_time == 0:
                    self.landing_burn_start_time = t
            elif self.pos_z < reentry_burn_alt:
                number_of_engines = number_of_engines_reentry
                if self.reentry_burn_start_time == 0:
                    self.reentry_burn_start_time = t
                
        total_thrust = number_of_engines * thrust

        if t < burntime:
            self.mass = M0_1 - number_of_engines * mass_flowrate * t
            self.thrust_x = np.cos(gamma) * total_thrust / self.mass
            self.thrust_z = np.sin(gamma) * total_thrust / self.mass

        if not ascending:
            self.mass = M_empty + self.M_prop_landing + self.M_prop_reentry # kg
            reentering = self.pos_z < reentry_burn_alt
            landing = self.pos_z < landing_burn_alt
            
            if landing:
                burn_time_so_far = t - self.landing_burn_start_time
                fuel_burned = number_of_engines * mass_flowrate * burn_time_so_far
                fuel_burned = np.clip(fuel_burned, 0, self.M_prop_landing)

                self.mass = M_empty + self.M_prop_landing - fuel_burned

                propellant_available = fuel_burned < self.M_prop_landing

                if propellant_available:
                    self.thrust_x = -np.cos(gamma) * total_thrust / self.mass
                    self.thrust_z = -np.sin(gamma) * total_thrust / self.mass
                    
            elif reentering:
                burn_time_so_far = t - self.reentry_burn_start_time
                fuel_burned = number_of_engines * mass_flowrate * burn_time_so_far
                fuel_burned = np.clip(fuel_burned, 0, self.M_prop_reentry)

                self.mass = M_empty + self.M_prop_landing + self.M_prop_reentry - fuel_burned

                propellant_available = fuel_burned < self.M_prop_reentry

                if propellant_available:
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

        speed = self.get_speed(self.velocity_x, self.velocity_z)

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

        t_max = 600
        t = 0

        while t < t_max:
            t += dt
            times = np.append(times, t)
            success = self.iterate(t, dt)
            if not success:
                break

        print("Finished")

        apogee_index = np.argmax(self.pos_zs)

        apogee_z = self.pos_zs[apogee_index]
        apogee_velocity_x = self.velocity_xs[apogee_index]
        apogee_velocity_z = self.velocity_zs[apogee_index]
        apogee_speed = self.get_speed(apogee_velocity_x, apogee_velocity_z)
        delta_V_total = self.get_delta_V_total(apogee_z, apogee_speed)

        print("Final Velocity Z:", self.velocity_zs[-1])
        print("Final Z:", self.pos_zs[-1])
        print("Final Mass:", self.masses[-1])
        print("Propellant Mass Remaining:", self.masses[-1] - M_empty)

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
        
        axs[2, 2].plot(times, self.thrust_xs* self.masses/10e5, label='tx')
        axs[2, 2].set_xlabel('Time (s)')
        axs[2, 2].set_ylabel('Thrust x (MN)')
        axs[2, 2].set_title('Thrust x vs Time')
        axs[2, 2].set_xscale('linear')
        axs[2, 2].set_yscale('linear')
        axs[2, 2].legend()

        axs[2, 3].plot(times, self.thrust_zs* self.masses/10e5, label='tz')
        axs[2, 3].set_xlabel('Time (s)')
        axs[2, 3].set_ylabel('Thrust z (MN)')
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

        axs[1, 4].plot(times, self.speeds/1000, label='speed')
        axs[1, 4].set_xlabel('Time (s)')
        axs[1, 4].set_ylabel('Speed (km/s)')
        axs[1, 4].set_title('Speed vs Time')
        axs[1, 4].set_xscale('linear')
        axs[1, 4].set_yscale('linear')
        axs[1, 4].legend()

        axs[2, 4].plot(times, 1/2*self.rhos*(self.speeds)**2/1000, label='Dynamic Pressure')
        axs[2, 4].set_xlabel('Time (s)')
        axs[2, 4].set_ylabel('Dynamic Pressure (kPa)')
        axs[2, 4].set_title('Dynamic Pressure vs Time')
        axs[2, 4].set_xscale('linear')
        axs[2, 4].set_yscale('linear')
        axs[2, 4].legend()

        plt.tight_layout()
        plt.show()

trajectory = Trajectory()
trajectory.run()