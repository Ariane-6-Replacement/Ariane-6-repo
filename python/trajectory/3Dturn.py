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

    def equations_of_motion(self, state, t):
        x, y, z, velocity_x, velocity_y, velocity_z = state 
        rho = self.get_density(z) # 101e3

        # ascending = velocity_z >= 0

        # Cd = 0
        # if ascending:
        #     Cd = Cd_ascent
        # else:
        #     Cd = Cd_descent

        D = self.get_drag(rho, velocity_x, velocity_z, A, Cd_ascent)
        #print("Drag:",D)
        #print("z:", z, "rho:",rho)
        # D = 0

        gamma = self.get_gamma(velocity_z, velocity_x)

        accel_x = 0
        accel_y = 0
        accel_z = 0

        #mass = M0_1
        thrust_x = 0
        thrust_z = 0

        number_of_engines = 1

        if z >= gravity_turn_alt and self.kick_time == 0:
            self.kick_time = t

        if z >= gravity_turn_alt and t <= self.kick_time + gamma_change_time:
            gamma = kick_angle

        if t < burntime:
            number_of_engines = number_of_engines_ascent
        # elif z < burn_alt and not ascending: 
        #     number_of_engines = number_of_engines_descent

        total_thrust = number_of_engines * thrust

        if t < burntime:
            self.mass = M0_1 - mass_flowrate * t
            thrust_x = np.cos(gamma) * total_thrust / self.mass
            thrust_z = np.sin(gamma) * total_thrust / self.mass
    
        # # elif z < burn_alt and not ascending:
        # #     total_thrust = number_of_engines_descent * -thrust
        # #     mass = M0
        # #     thrust_x = np.cos(gamma) * total_thrust / mass
        # #     thrust_z = np.sin(gamma) * total_thrust / mass
        
        # accel_x += thrust_x
        # accel_z += thrust_z
            
        drag_x = -np.cos(gamma) * D / self.mass
        drag_z = -np.sin(gamma) * D / self.mass


        # if D != 0:
        #     accel_x += 
        accel_x += thrust_x + drag_x
        accel_z += -g_0 + thrust_z + drag_z 

        # print("t:", t, "z:", z, "velocity_z", velocity_z, "mass:", self.mass)

        return [velocity_x, velocity_y, velocity_z, accel_x, accel_y, accel_z]

    def run(self):

        # Define initial conditions
        # initial_state = [0, 0, 55e3,1600*2**0.5/2, 0, 1600*2**0.5/2]  # x,y,z,vx,vy,vz
        # initial_state = [0, 0, 100,1600*2**0.5/2, 0, 1600*2**0.5/2]  # x,y,z,vx,vy,vz
        initial_state = [0, 0, 0, 0, 0, 3]  # x,y,z,vx,vy,vz

        # Define time points for integration
        t = np.linspace(0, 700.5, 5000)  # Example: integrate from 0 to 10 seconds with 100 points

        # Solve the equations of motion
        solution = odeint(self.equations_of_motion, initial_state, t)
        print("Finished")

        # Extract position and velocity from the solution
        x, y, z, vx, vy, vz = solution.T

        fig, axs = plt.subplots(3, 3, figsize=(10, 8))  # 2x2 grid of subplots

        self.drags = np.zeros_like(vx)
        self.gammas = np.zeros_like(vx)

        for j in range(len(vx)):
            self.drags[j] = self.get_drag(self.get_density(z[j]), vx[j], vz[j], A, Cd_ascent)
            self.gammas[j] = np.rad2deg(self.get_gamma(vz[j], vx[j]))

        axs[0, 0].plot(t, x / 1000, label='x vs time')
        axs[0, 0].set_xlabel('Time (s)')
        axs[0, 0].set_ylabel('Pos x (km)')
        axs[0, 0].set_title('Pos (x vs time)')
        axs[0, 0].set_xscale('linear')
        axs[0, 0].set_yscale('linear')
        axs[0, 0].legend()

        axs[0, 1].plot(t, z / 1000, label='z vs time')
        axs[0, 1].set_xlabel('Time (s)')
        axs[0, 1].set_ylabel('Pos z (km)')
        axs[0, 1].set_title('Pos (z vs time)')
        axs[0, 1].set_xscale('linear')
        axs[0, 1].set_yscale('linear')
        axs[0, 1].legend()

        axs[1, 0].plot(t, vx / 1000, label='vx')
        axs[1, 0].set_xlabel('Time (s)')
        axs[1, 0].set_ylabel('Velocity x (km/s)')
        axs[1, 0].set_title('Velocity x vs Time')
        axs[1, 0].set_xscale('linear')
        axs[1, 0].set_yscale('linear')
        axs[1, 0].legend()

        axs[1, 1].plot(t, vz / 1000, label='vz')
        axs[1, 1].set_xlabel('Time (s)')
        axs[1, 1].set_ylabel('Velocity z (km/s)')
        axs[1, 1].set_title('Velocity z vs Time')
        axs[1, 1].set_xscale('linear')
        axs[1, 1].set_yscale('linear')
        axs[1, 1].legend()

        axs[0, 2].plot(t, self.drags / 1e6, label='drag')
        axs[0, 2].set_xlabel('Time (s)')
        axs[0, 2].set_ylabel('Drag (MN)')
        axs[0, 2].set_title('Drag vs Time')
        axs[0, 2].set_xscale('linear')
        axs[0, 2].set_yscale('linear')
        axs[0, 2].legend()

        axs[1, 2].plot(t, self.gammas, label='gamma')
        axs[1, 2].set_xlabel('Time (s)')
        axs[1, 2].set_ylabel('Gamma')
        axs[1, 2].set_ylim(-100, 100)
        axs[1, 2].set_title('Gamma vs Time')
        axs[1, 2].set_xscale('linear')
        axs[1, 2].set_yscale('linear')
        axs[1, 2].legend()

        axs[2, 0].plot(x / 1000, z / 1000, label='x')
        axs[2, 0].set_xlabel('Distance x (km)')
        axs[2, 0].set_ylabel('Distance z (km)')
        axs[2, 0].set_title('Z vs X')
        axs[2, 0].set_xscale('linear')
        axs[2, 0].set_yscale('linear')
        axs[2, 0].legend()

        plt.tight_layout()
        plt.show()

trajectory = Trajectory()
trajectory.run()