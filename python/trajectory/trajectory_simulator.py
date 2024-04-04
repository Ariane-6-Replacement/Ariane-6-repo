import numpy as np
import matplotlib.pyplot as plt

g_0 = 9.81 # [m / s^2]
R_earth = 6_371e3 # [m]
mu_earth = 3.986_004_418e14 # [m^3 / s^-2]

class Trajectory():
    def __init__(self):
        pass

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
        return drag
    
    def get_gamma(self, velocity_z, velocity_x):
        return np.arctan2(velocity_z, velocity_x)
    
    def get_g(self, pos_z):
        return -g_0 * (1 - 2 * pos_z / R_earth)
    
    def get_propellant(self, I_sp_1, delta_V, M_remaining):
        propellant = np.exp(delta_V / (I_sp_1 * g_0)) * (self.m_first_stage_structural + M_remaining) - (self.m_first_stage_structural + M_remaining)
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
    
    def get_required_second_stage_delta_V(self, pos_z, speed):
        altitude = R_earth + pos_z
        v_c1 = np.sqrt(mu_earth / (altitude + R_earth))
        delta_V_circ = v_c1 - speed

        GTO_p = R_earth + 250e3 # [m]
        GTO_a = R_earth + 22_500e3 # [m]

        required_delta_V = delta_V_circ + self.delta_V_circular_to_circular(altitude, GTO_p) + self.delta_V_circular_to_elliptical(GTO_p, GTO_a)

        return required_delta_V
    
    # Based on structures formulation.
    def get_second_stage_structural_mass(self, second_stage_propellant_mass):
        prop_mass_extension = second_stage_propellant_mass - 31_000
        of = 5.8
        mf = prop_mass_extension / (of+1)
        mox = prop_mass_extension - mf
        vf = mf / 70.8
        vox = mox / 1141
        Lf = vf / (np.pi * 2.7 ** 2)
        Lox = vox / (np.pi * 2.7 ** 2)
        struc_mass_extension = (Lf + Lox) * 3000 * np.pi * 5.4 * 5E-3
        mfaring = 2657 #kg
        msyldas = 425 # kg
        mcone = 200 # kg
        mstruc = 4540 * 5.8/4.9 + struc_mass_extension + 385
        second_stage_structural_mass = mfaring + msyldas + mcone + mstruc
        return second_stage_structural_mass

    def setup(self,
              simulation_timestep,
              simulation_time,
              number_of_engines_ascent,
              number_of_engines_landing,
              number_of_engines_reentry,
              thrust,
              I_sp_1,
              I_sp_2,
              kick_angle,
              gamma_change_time,
              m_first_stage_total,
              m_first_stage_structural_frac,
              m_second_stage_propellant,
              m_second_stage_payload,
              delta_V_landing,
              delta_V_reentry,
              Cd_ascent,
              Cd_descent,
              diameter,
              reentry_burn_alt,
              gravity_turn_alt):
        
        self.simulation_timestep = simulation_timestep
        self.simulation_time = simulation_time
        
        self.number_of_engines_ascent = number_of_engines_ascent
        self.number_of_engines_landing = number_of_engines_landing
        self.number_of_engines_reentry = number_of_engines_reentry
       
        self.thrust = thrust
        self.I_sp_1 = I_sp_1
        self.I_sp_2 = I_sp_2
        self.iniate_landing_burn = False 
        self.mass_flowrate = self.thrust / (g_0 * self.I_sp_1)

        self.kick_angle = kick_angle
        self.gamma_change_time = gamma_change_time

        self.m_first_stage = m_first_stage_total

        self.m_first_stage_structural = self.m_first_stage * m_first_stage_structural_frac

        self.m_prop_landing = self.get_propellant(self.I_sp_1, delta_V_landing, 0)
        self.m_prop_reentry = self.get_propellant(self.I_sp_1, delta_V_reentry, self.m_prop_landing)
        
        self.m_first_stage_propellant = self.m_first_stage - (self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry)

        assert self.m_first_stage_propellant > 0, "No propellant available for ascent"

        self.m_second_stage_propellant = m_second_stage_propellant
        # 2nd stage structural mass formula provided by structures.
        self.m_second_stage_structural = self.get_second_stage_structural_mass(self.m_second_stage_propellant) # 9.272e3 kg
        self.m_second_stage_payload = m_second_stage_payload

        self.burntime = self.m_first_stage_propellant / (self.mass_flowrate * self.number_of_engines_ascent)

        self.m_second_stage = self.m_second_stage_structural + self.m_second_stage_propellant + self.m_second_stage_payload
        
        self.m_total = self.m_first_stage + self.m_second_stage

        self.mass = self.m_total
        self.delta_V_first_stage = self.I_sp_1 * g_0 * np.log(self.m_total / (self.m_total - self.m_first_stage_propellant ))
        self.delta_V_second_stage = self.I_sp_2 * g_0 * np.log(self.m_second_stage / (self.m_second_stage - self.m_second_stage_propellant))
        
        print("First stage structural mass:", self.m_first_stage_structural / 1000, "t")
        print("First stage propellant mass:", self.m_first_stage_propellant / 1000, "t")
        print("First stage total mass:", self.m_first_stage / 1000, "t")

        print("Second stage structural mass:", self.m_second_stage_structural / 1000, "t")
        print("Second stage propellant mass:", self.m_second_stage_propellant / 1000, "t")
        print("Second stage total mass:", self.m_second_stage / 1000, "t")
        
        print("Total rocket mass:", self.m_total / 1000, "t")

        self.Cd_ascent = Cd_ascent
        self.Cd_descent = Cd_descent
        self.area = np.pi * diameter ** 2 / 4
        
        self.reentry_burn_alt = reentry_burn_alt
        self.gravity_turn_alt = gravity_turn_alt
        
        self.kick_time = 0
        self.landing_burn_start_time = 0
        self.reentry_burn_start_time = 0
        
        self.pos_x = 0
        self.pos_z = 0
        self.velocity_x = 0
        self.velocity_z = 3
        self.accel_x = 0
        self.accel_z = 0

        self.second_stage_thrust = 180e3 # newtons # From propulsion.

        print("First Stage Delta V:", self.delta_V_first_stage / 1e3, "km / s")
        print("Second Stage Delta V:", self.delta_V_second_stage / 1e3, "km / s")
        print("Total Delta V:", (self.delta_V_first_stage + self.delta_V_second_stage) / 1e3, "km / s")
        print("Burntime:", self.burntime, "s")
        print("Propellant available for ascent:", self.m_first_stage_propellant / 1e3, "t")
        print("Propellant available for re-entry:", self.m_prop_reentry / 1e3, "t")
        print("Propellant available for landing:", self.m_prop_landing / 1e3, "t")
        print("First Stage TWR:", self.thrust*self.number_of_engines_ascent/(g_0*self.m_total))
        print("Second Stage TWR:", self.second_stage_thrust * 1/(g_0*self.m_second_stage))

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

        self.ascent_start_index = 0
        self.coasting_start_index = 0
        self.apogee_index = 0
        self.reentry_start_index = 0
        self.coasting2_start_index = 0
        self.landing_start_index = 0

    def iterate(self, t, dt):
        rho = self.get_density(self.pos_z)

        before_apogee = self.velocity_z >= 0

        Cd = 0
        if before_apogee:
            Cd = self.Cd_ascent
        else:
            Cd = self.Cd_descent

        drag_force = self.get_drag(rho, self.velocity_x, self.velocity_z, self.area, Cd)
        gamma = self.get_gamma(self.velocity_z, self.velocity_x)


        
        impact_time = (np.sqrt(2 * g_0 * self.pos_z + self.velocity_z ** 2) + self.velocity_z) / g_0
        land_accel = self.number_of_engines_landing * self.thrust / (self.m_first_stage_structural + self.m_prop_landing)
        deccel_time = -self.velocity_z / (land_accel - g_0)
        
        
        if deccel_time - 5.3 > impact_time and self.pos_z<10e3 and not before_apogee and not self.iniate_landing_burn :
             self.iniate_landing_burn  = True
             #print( " deccel_time:", deccel_time, "impact time:", impact_time, self.pos_z)
            

        landing = not before_apogee and self.iniate_landing_burn 
        reentering = not before_apogee and self.pos_z < self.reentry_burn_alt

        if landing:
            if self.landing_burn_start_time == 0:
                self.landing_burn_start_time = t
        elif reentering:
            if self.reentry_burn_start_time == 0:
                self.reentry_burn_start_time = t

        # Assume ascent starts at t=0
        ascent_fuel_burned  = np.clip(self.number_of_engines_ascent  * self.mass_flowrate * (t - 0),                            0, self.m_first_stage_propellant)
        landing_fuel_burned = np.clip(self.number_of_engines_landing * self.mass_flowrate * (t - self.landing_burn_start_time), 0, self.m_prop_landing)
        reentry_fuel_burned = np.clip(self.number_of_engines_reentry * self.mass_flowrate * (t - self.reentry_burn_start_time), 0, self.m_prop_reentry)

        ascent_fuel_available = ascent_fuel_burned < self.m_first_stage_propellant
        landing_fuel_available = landing_fuel_burned < self.m_prop_landing
        reentry_fuel_available = reentry_fuel_burned < self.m_prop_reentry

        ascending = before_apogee and ascent_fuel_available

        in_gravity_turn = self.pos_z >= self.gravity_turn_alt

        if in_gravity_turn and self.kick_time == 0:
            self.kick_time = t
        if in_gravity_turn and t <= self.kick_time + self.gamma_change_time:
            gamma = self.kick_angle

        if not ascending and self.coasting_start_index == 0:
            self.coasting_start_index = self.counter
        elif reentering and self.reentry_start_index == 0:
            self.reentry_start_index = self.counter
        elif reentering and not reentry_fuel_available and self.coasting2_start_index == 0:
            self.coasting2_start_index = self.counter
        elif landing and self.landing_start_index == 0:
            self.landing_start_index = self.counter
       
        total_thrust = 0

        if ascending:
            self.mass = self.m_total - ascent_fuel_burned
            total_thrust = self.number_of_engines_ascent * self.thrust
        elif landing and landing_fuel_available:
            self.mass = self.m_first_stage_structural + self.m_prop_landing - landing_fuel_burned
            total_thrust = -self.number_of_engines_landing * self.thrust
        elif reentering and reentry_fuel_available:
            self.mass = self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry - reentry_fuel_burned
            total_thrust = -self.number_of_engines_reentry * self.thrust

        self.thrust_x = np.cos(gamma) * total_thrust / self.mass
        self.thrust_z = np.sin(gamma) * total_thrust / self.mass

        drag_x = -np.cos(gamma) * drag_force / self.mass
        drag_z = -np.sin(gamma) * drag_force / self.mass

        self.accel_x = self.thrust_x + drag_x
        self.accel_z = self.get_g(self.pos_z) + self.thrust_z + drag_z

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

        #if self.pos_x > self.max_barge_distance:
            # print("barge overshot")
            #return False

        below_ground = self.pos_z < -1000

        if below_ground:
            print("Trajectory ends up below ground!")
            #return False
    
        # Previous position was apogee
        if not before_apogee and self.apogee_index == 0:
            self.apogee_index = self.counter
            apogee_z = self.pos_zs[self.apogee_index]
            apogee_velocity_x = self.velocity_xs[self.apogee_index]
            apogee_velocity_z = self.velocity_zs[self.apogee_index]
            apogee_speed = self.get_speed(apogee_velocity_x, apogee_velocity_z)
            required_delta_V = self.get_required_second_stage_delta_V(apogee_z, apogee_speed)
            print("Trajectory reached apogee!")
            print("Required Second Stage Delta V:", required_delta_V / 1000, "km / s")
            # if required_delta_V > self.delta_V_second_stage:
            #     return False
            #if apogee_z > self.max_apogee:
            #    return False
                
        if self.velocity_z > -5 and self.pos_z < 10e3 and not before_apogee:
            print("Landing burn unsuccessful. Impacting ground with", abs(self.velocity_z), "m / s downward velocity")
        
        self.counter += 1
        return True
    
    def add_phase(self, axis, xs, ys, legend_location, start, stop, color, linestyle, label='_'):
        axis.plot(xs[start:stop], ys[start:stop], color=color, linestyle=linestyle, label=label)
        axis.legend(loc=legend_location, prop={'size': 6})

    def add_flight_phases(self, title, xlabel, ylabel, axis, xs, ys, legend_location, lower_y_zero_bound=True, coloring=True):
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_title(title)
        #axis.set_xlim(left=0)
        if lower_y_zero_bound:
            pass
            #axis.set_ylim(bottom=0)
        if coloring:
            # -1 fixes the discontinuity points for graphs with jumps in values.
            self.add_phase(axis, xs, ys, legend_location, self.ascent_start_index, self.coasting_start_index, self.ascent_color, self.ascent_style, self.ascent_label)
            self.add_phase(axis, xs, ys, legend_location, self.coasting_start_index - 1, self.reentry_start_index, self.coasting_color, self.coasting_style, self.coasting_label)
            self.add_phase(axis, xs, ys, legend_location, self.reentry_start_index - 1, self.coasting2_start_index, self.reentry_color, self.reentry_style, self.reentry_label)
            self.add_phase(axis, xs, ys, legend_location, self.coasting2_start_index - 1, self.landing_start_index, self.coasting_color, self.coasting_style)
            self.add_phase(axis, xs, ys, legend_location, self.landing_start_index - 1, -1, self.landing_color, self.landing_style, self.landing_label)
        else:
            axis.plot(xs, ys)

    def plot(self):
        self.ascent_color = 'red'
        self.coasting_color = 'blue'
        self.reentry_color = 'orange'
        self.landing_color = 'black'
        self.ascent_style = 'solid'
        self.coasting_style = 'solid'
        self.reentry_style = 'solid'
        self.landing_style = 'solid'
        self.ascent_label = 'ascent'
        self.coasting_label = 'coasting'
        self.reentry_label = 'reentry'
        self.landing_label = 'landing'

        self.fig, axs = plt.subplots(3, 5, figsize=(10, 8), num="Trajectory Simulation Plots")  # 2x2 grid of subplots

        self.add_flight_phases('Pos X vs Time', 'Time (s)', 'Pos X (km)', axs[0, 0], self.times, self.pos_xs / 1000, 'lower right')
        self.add_flight_phases('Pos Z vs Time', 'Time (s)', 'Pos Z (km)', axs[0, 1], self.times, self.pos_zs / 1000, 'lower center')
        self.add_flight_phases('Atmospheric Density vs Time', 'Time (s)', 'Atmospheric Density (kg/m^3)', axs[0, 2], self.times, self.rhos, 'upper center')
        self.add_flight_phases('Drag vs Time', 'Time (s)', 'Drag (MN)', axs[0, 3], self.times, self.drags / 1e6, 'upper center')
        self.add_flight_phases('Pos Z vs Pos X', 'Pos X (km)', 'Pos Z (km)', axs[0, 4], self.pos_xs / 1000, self.pos_zs / 1000, 'lower center')
        self.add_flight_phases('Velocity X vs Time', 'Time (s)', 'Velocity X (km/s)', axs[1, 0], self.times, self.velocity_xs / 1000, 'lower center')
        self.add_flight_phases('Velocity Z vs Time', 'Time (s)', 'Velocity Z (km/s)', axs[1, 1], self.times, self.velocity_zs / 1000, 'lower left')
        self.add_flight_phases('Flight Path Angle vs Time', 'Time (s)', 'Flight Path Angle (degrees)', axs[1, 2], self.times, self.gammas, 'lower left')
        axs[1, 2].set_ylim(-100, 100)
        self.add_flight_phases('Mass vs Time', 'Time (s)', 'Mass (tonnes)', axs[1, 3], self.times, self.masses / 1000, 'upper center')
        self.add_flight_phases('Speed vs Time', 'Time (s)', 'Speed (km/s)', axs[1, 4], self.times, self.speeds / 1000, 'lower center')
        self.add_flight_phases('Accel X vs Time', 'Time (s)', 'Accel X (g)', axs[2, 0], self.times, self.accel_xs / g_0, 'lower center')
        self.add_flight_phases('Accel Z vs Time', 'Time (s)', 'Accel Z (g)', axs[2, 1], self.times, self.accel_zs / g_0, 'upper center')
        self.add_flight_phases('Thrust X vs Time', 'Time (s)', 'Thrust X (MN)', axs[2, 2], self.times, self.thrust_xs * self.masses / 10e5, 'upper center')
        self.add_flight_phases('Thrust Z vs Time', 'Time (s)', 'Thrust Z (MN)', axs[2, 3], self.times, self.thrust_zs * self.masses / 10e5, 'upper center')
        self.add_flight_phases('Dynamic Pressure vs Time', 'Time (s)', 'Dynamic Pressure (kPa)', axs[2, 4], self.times, 0.5 * self.rhos * self.speeds ** 2 / 1000, 'upper center')

        plt.tight_layout()
        plt.show()

    def run(self):
        self.times = np.array([])
        t = 0
        #self.max_barge_distance = 1000e3 # meters
        #self.max_apogee = 1000e3 # meters
        success = True
        self.counter = 0
        print("Starting trajectory simulation!")
        while t < self.simulation_time:
            t += self.simulation_timestep
            self.times = np.append(self.times, t)
            success = self.iterate(t, self.simulation_timestep)
            if not success:
                break
        if success:
            print("Finished trajectory simulation!")
        else:
            print("Failed to simulate a successful trajectory.")
        
if __name__ == "__main__":

    trajectory = "Elysium" # "Falcon 9" # "Elysium"

    if trajectory == "Elysium":
        print("Running Elysium trajectory...")
        elysium_trajectory = Trajectory()
        
        first_stage_ascent_prop_margin = 1.02
        first_stage_landing_prop_margin = 1.1
        first_stage_reentry_prop_margin = 1.05

        elysium_trajectory.setup(
            simulation_timestep = 0.01, # seconds
            simulation_time = 900, # seconds
            number_of_engines_ascent=9, # input
            number_of_engines_landing=1, # input
            number_of_engines_reentry=3, # input
            thrust=1_000_000, # newtons # self.engine.Thrust
            I_sp_1=306, # seconds # self.propulsion.Isp
            I_sp_2=457, # seconds # self.isp2, 
            kick_angle=np.radians(68), # degrees input
            gamma_change_time=10, # seconds input
            m_first_stage_total=400e3 * first_stage_ascent_prop_margin, # self.mass
            m_first_stage_structural_frac=0.0578, # self.dry_masses[0] / self.mass
            #m_second_stage_structural=9.272e3, # kg
            m_second_stage_propellant=80e3, # kg # self.prop_masses[1]
            m_second_stage_payload=11.5e3, # kg # self.payload
            delta_V_landing=909 * first_stage_landing_prop_margin, # m / s input
            delta_V_reentry=1905 * first_stage_reentry_prop_margin, # m / s input
            Cd_ascent=0.3, # self.cd
            Cd_descent=1.0, # assumed constant
            diameter=5.4, # meters # self.diameter
            reentry_burn_alt=55_000, # meters input
            gravity_turn_alt=10_000 # meters input
        )
        elysium_trajectory.run()
        elysium_trajectory.plot()
    elif trajectory == "Falcon 9":
        print("Running Falcon 9 trajectory...")
        falcon_9_trajectory = Trajectory()
        falcon_9_trajectory.setup(
            simulation_timestep = 0.01, # seconds
            simulation_time = 900, # seconds
            number_of_engines_ascent=9,
            number_of_engines_landing=1,
            number_of_engines_reentry=3,
            thrust=805_000 * 1, # newtons
            I_sp_1=283, # seconds
            I_sp_2=348, # seconds   
            kick_angle=np.radians(75.5), # radians
            gamma_change_time=8, # seconds
            m_first_stage_total = 421e3,
            m_first_stage_structural_frac= 0.045, #0.0578,
            m_second_stage_propellant=92e3, # kg
            m_second_stage_payload=13.1e3,
            delta_V_landing=200, # m / s
            delta_V_reentry=2_000, # m / s
            Cd_ascent=0.4,
            Cd_descent=1.0,
            diameter=3.7, # meters
            reentry_burn_alt=55_000, # meters
            #landing_burn_alt=1_000, # meters
            gravity_turn_alt=1.5e3 # meters
        )
        falcon_9_trajectory.run()
        falcon_9_trajectory.plot()