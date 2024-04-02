import numpy as np
import matplotlib.pyplot as plt

g_0 = 9.81 # [m / s^2]
R_earth = 6_371e3 # [m]
mu_earth = 3.986_004_418e14 # [m^3 / s^-2]

simulation_timestep = 0.01 # seconds
simulation_time = 900 # seconds

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
        return drag # 0
    
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
    
    def get_second_stage_available_delta_V(self):
        second_stage_initial_mass = self.m_second_stage_structural + self.m_second_stage_propellant + self.m_second_stage_payload
        second_stage_final_mass = self.m_second_stage_structural + self.m_second_stage_payload

        available_delta_v = g_0 * self.I_sp_2 * np.log(second_stage_initial_mass / second_stage_final_mass)
        return available_delta_v
    
    def get_required_second_stage_delta_V(self, pos_z, speed):
        altitude = R_earth + pos_z
        v_c1 = np.sqrt(mu_earth / (altitude + R_earth))
        delta_V_circ = v_c1 - speed

        GTO_p = R_earth + 250e3 # [m]
        GTO_a = R_earth + 22_500e3 # [m]

        required_delta_V = delta_V_circ + self.delta_V_circular_to_circular(altitude, GTO_p) + self.delta_V_circular_to_elliptical(GTO_p, GTO_a)

        return required_delta_V

    def setup(self,
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
              m_second_stage_structural,
              m_second_stage_propellant,
              m_second_stage_payload,
              delta_V_landing,
              delta_V_reentry,
              Cd_ascent,
              Cd_descent,
              diameter,
              reentry_burn_alt,
              landing_burn_alt,
              gravity_turn_alt):
        

        self.printflag = 0
        self.number_of_engines_ascent = number_of_engines_ascent
        self.number_of_engines_landing = number_of_engines_landing
        self.number_of_engines_reentry = number_of_engines_reentry
        
        self.thrust = thrust
        self.I_sp_1 = I_sp_1
        self.I_sp_2 = I_sp_2
        self.mass_flowrate = self.thrust / (g_0 * self.I_sp_1)
        self.kick_angle = kick_angle
        self.gamma_change_time = gamma_change_time

        self.m_first_stage_structural= m_first_stage_total * m_first_stage_structural_frac # kg
        self.m_prop_landing = self.get_propellant(self.I_sp_1, delta_V_landing, 0)
        self.m_prop_reentry = self.get_propellant(self.I_sp_1, delta_V_reentry, self.m_prop_landing)
        

        
        self.m_first_stage_propellant= m_first_stage_total-self.m_first_stage_structural-self.m_prop_landing-self.m_prop_reentry# kg
        self.m_second_stage_structural = m_second_stage_structural
        self.m_second_stage_propellant = m_second_stage_propellant
        print("first stage prop:" ,self.m_first_stage_propellant)
        self.m_second_stage_payload = m_second_stage_payload
        self.burntime = self.m_first_stage_propellant / (self.mass_flowrate * self.number_of_engines_ascent)

 
        
        self.m_second_stage = self.m_second_stage_structural + self.m_second_stage_propellant + self.m_second_stage_payload
        self.m_first_stage = self.m_first_stage_propellant + self.m_first_stage_structural
        
       
        
        self.mass = self.m_first_stage + self.m_second_stage + self.m_prop_landing + self.m_prop_reentry
        
        self.delta_V_first_stage = self.I_sp_1 * g_0 * np.log(self.mass / (self.mass - self.m_first_stage_propellant))
        self.delta_V_second_stage = self.get_second_stage_available_delta_V()
        
        self.Cd_ascent = Cd_ascent
        self.Cd_descent = Cd_descent
        self.area = np.pi * diameter ** 2 / 4
        
        self.m_second_stage_structural = m_second_stage_structural
        self.m_second_stage_propellant = m_second_stage_propellant
        self.m_second_stage_payload = m_second_stage_payload
        
        self.reentry_burn_alt = reentry_burn_alt
        self.landing_burn_alt = landing_burn_alt
        self.gravity_turn_alt = gravity_turn_alt
        
        self.kick_time = 0
        
        self.pos_x = 0
        self.pos_z = 0
        self.velocity_x = 0
        self.velocity_z = 3
        self.accel_x = 0
        self.accel_z = 0

        print("First Stage Delta V:", self.delta_V_first_stage)
        print("Second Stage Delta V:", self.delta_V_second_stage)
        print("Total Delta V:", self.delta_V_first_stage + self.delta_V_second_stage)
        print("Burntime:", self.burntime)
        print("Propellant available for re-entry:", self.m_prop_reentry)
        print("Propellant available for landing:", self.m_prop_landing)

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

    
    def iterate(self, t, dt):
       
        rho = self.get_density(self.pos_z)

        ascending = self.velocity_z >= 0

        Cd = 0
        if ascending:
            Cd = self.Cd_ascent
        else:
            Cd = self.Cd_descent

        drag_force = self.get_drag(rho, self.velocity_x, self.velocity_z, self.area, Cd)
        gamma = self.get_gamma(self.velocity_z, self.velocity_x)

        self.thrust_x = 0
        self.thrust_z = 0

        number_of_engines = 1

        if self.pos_z >= self.gravity_turn_alt and self.kick_time == 0:
            self.kick_time = t

        if self.pos_z >= self.gravity_turn_alt and t <= self.kick_time + self.gamma_change_time:
            gamma = self.kick_angle

        if ascending and t < self.burntime:
            number_of_engines = self.number_of_engines_ascent
        elif not ascending:
            if self.pos_z < self.landing_burn_alt: 
                number_of_engines = self.number_of_engines_landing
                if self.landing_burn_start_time == 0:
                    self.landing_burn_start_time = t
                    
            elif self.pos_z < self.reentry_burn_alt:
                number_of_engines = self.number_of_engines_reentry
                if self.reentry_burn_start_time == 0:
                    self.reentry_burn_start_time = t
                
        total_thrust = number_of_engines * self.thrust


        
        impact_time = (np.sqrt(2*g_0*self.pos_z + self.velocity_z**2)+self.velocity_z)/g_0
        land_accel = self.number_of_engines_landing*self.thrust/(self.mass)
        deccel_time = -self.velocity_z/(land_accel-g_0)
        iniate_landing_burn = False 
        
        if deccel_time > impact_time and self.pos_z<10e3 and not ascending:
             iniate_landing_burn = True
             
             if self.printflag == 0:
                print( " deccel_time:", deccel_time, "impact time:", impact_time, self.pos_z)
                self.printflag = 1
             if self.landing_burn_start_time == 0:
                    self.landing_burn_start_time = t
                    
                    

        if t < self.burntime:
            m_first_stage_propellant_burned = number_of_engines * self.mass_flowrate * t
            self.mass = self.m_first_stage + self.m_second_stage + self.m_prop_landing + self.m_prop_reentry - m_first_stage_propellant_burned
            self.thrust_x = np.cos(gamma) * total_thrust / self.mass
            self.thrust_z = np.sin(gamma) * total_thrust / self.mass

        if not ascending:
            self.mass = self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry # kg
            reentering = self.pos_z < self.reentry_burn_alt
            landing = self.pos_z < self.landing_burn_alt
            
            if iniate_landing_burn:
                # print("Burning at :", self.pos_z)
                burn_time_so_far = t - self.landing_burn_start_time-22
                #print(burn_time_so_far)
                # if burn_time_so_far < 1:
                #     # print("landing alt:", self.pos_z)
                fuel_burned = number_of_engines * self.mass_flowrate * burn_time_so_far
                fuel_burned = np.clip(fuel_burned, 0, self.m_prop_landing)

                self.mass = self.m_first_stage_structural + self.m_prop_landing - fuel_burned

                propellant_available = fuel_burned < self.m_prop_landing
                if propellant_available:
                    
                    # print("landing burn at ", self.velocity_z, "at alt", self.pos_z)
                    self.thrust_x = -np.cos(gamma) * total_thrust / self.mass
                    self.thrust_z = -np.sin(gamma) * total_thrust / self.mass
                    
            elif reentering:
                burn_time_so_far = t - self.reentry_burn_start_time
                fuel_burned = number_of_engines * self.mass_flowrate * burn_time_so_far
                fuel_burned = np.clip(fuel_burned, 0, self.m_prop_reentry)

                self.mass = self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry - fuel_burned

                propellant_available = fuel_burned < self.m_prop_reentry

                if propellant_available:
                    self.thrust_x = -np.cos(gamma) * total_thrust / self.mass
                    self.thrust_z = -np.sin(gamma) * total_thrust / self.mass

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

        if self.pos_z < 0: #and not ascending and abs(self.velocity_z) < 0.1
            return False
        return True

    def run(self):

        dt = simulation_timestep

        times = np.array([])

        t_max = simulation_time
        t = 0

        while t < t_max:
            t += dt
            times = np.append(times, t)
            success = self.iterate(t, dt)
            if not success:
                break

        # print("Finished")

        apogee_index = np.argmax(self.pos_zs)

        apogee_z = self.pos_zs[apogee_index]
        apogee_velocity_x = self.velocity_xs[apogee_index]
        apogee_velocity_z = self.velocity_zs[apogee_index]
        apogee_speed = self.get_speed(apogee_velocity_x, apogee_velocity_z)
        required_delta_V = self.get_required_second_stage_delta_V(apogee_z, apogee_speed)
        print("Required Second Stage Delta V:", required_delta_V)

        if self.velocity_zs[-1]<0:
            print("crashed going: ", self.velocity_zs[-1] )
        # print("Final Velocity Z:", self.velocity_zs[-1])
        # print("Final Z:", self.pos_zs[-1])
        print("Final Mass:", self.masses[-1])   
        print("Propellant Mass Remaining:", self.masses[-1] - self.m_first_stage_structural)

        fig, axs = plt.subplots(3, 5, figsize=(10, 8))  # 2x2 grid of subplots

        axs[0, 0].plot(times, self.pos_xs / 1000)
        axs[0, 0].set_xlabel('Time (s)')
        axs[0, 0].set_ylabel('Pos x (km)')
        axs[0, 0].set_title('Pos (x vs time)')

        axs[0, 1].plot(times, self.pos_zs / 1000)
        axs[0, 1].set_xlabel('Time (s)')
        axs[0, 1].set_ylabel('Pos z (km)')
        axs[0, 1].set_title('Pos (z vs time)')

        axs[0, 2].plot(times, self.rhos)
        axs[0, 2].set_xlabel('Time (s)')
        axs[0, 2].set_ylabel('Rho (kg/m^3)')
        axs[0, 2].set_title('Rho vs Time')
        
        axs[1, 3].plot(times, self.masses / 1000)
        axs[1, 3].set_xlabel('Time (s)')
        axs[1, 3].set_ylabel('Mass (tonnes)')
        axs[1, 3].set_title('Mass vs Time')

        axs[0, 3].plot(times, self.drags / 1e6)
        axs[0, 3].set_xlabel('Time (s)')
        axs[0, 3].set_ylabel('Drag (MN)')
        axs[0, 3].set_title('Drag vs Time')

        axs[1, 0].plot(times, self.velocity_xs / 1000)
        axs[1, 0].set_xlabel('Time (s)')
        axs[1, 0].set_ylabel('Velocity x (km/s)')
        axs[1, 0].set_title('Velocity x vs Time')

        axs[1, 1].plot(times, self.velocity_zs / 1000)
        axs[1, 1].set_xlabel('Time (s)')
        axs[1, 1].set_ylabel('Velocity z (km/s)')
        axs[1, 1].set_title('Velocity z vs Time')
        
        axs[2, 0].plot(times, self.accel_xs / g_0)
        axs[2, 0].set_xlabel('Time (s)')
        axs[2, 0].set_ylabel('Accel x (g)')
        axs[2, 0].set_title('Accel x vs Time')

        axs[2, 1].plot(times, self.accel_zs / g_0)
        axs[2, 1].set_xlabel('Time (s)')
        axs[2, 1].set_ylabel('Accel z (g)')
        axs[2, 1].set_title('Accel z vs Time')
        
        axs[2, 2].plot(times, self.thrust_xs * self.masses / 10e5)
        axs[2, 2].set_xlabel('Time (s)')
        axs[2, 2].set_ylabel('Thrust x (MN)')
        axs[2, 2].set_title('Thrust x vs Time')

        axs[2, 3].plot(times, self.thrust_zs * self.masses / 10e5)
        axs[2, 3].set_xlabel('Time (s)')
        axs[2, 3].set_ylabel('Thrust z (MN)')
        axs[2, 3].set_title('Thrust z vs Time')

        axs[1, 2].plot(times, self.gammas)
        axs[1, 2].set_xlabel('Time (s)')
        axs[1, 2].set_ylabel('Gamma')
        axs[1, 2].set_ylim(-100, 100)
        axs[1, 2].set_title('Gamma vs Time')
        
        axs[0, 4].plot(self.pos_xs / 1000, self.pos_zs / 1000)
        axs[0, 4].set_xlabel('X pos (km)')
        axs[0, 4].set_ylabel('Z pos (km)')
        # axs[0, 4].set_ylim(0, 125)
        # axs[0, 4].set_xlim(0, 125)
        axs[0, 4].set_title('Z pos vs X pos')

        axs[1, 4].plot(times, self.speeds / 1000)
        ax2 = axs[1, 4].twinx()
        ax2.plot(times, self.pos_zs / 1000, color= "purple")
        axs[1, 4].set_xlabel('Time (s)')
        axs[1, 4].set_ylabel('Speed (km/s)')
        axs[1, 4].set_title('Speed vs Time')

        axs[2, 4].plot(times, 0.5 * self.rhos * self.speeds ** 2 / 1000)
        axs[2, 4].set_xlabel('Time (s)')
        axs[2, 4].set_ylabel('Dynamic Pressure (kPa)')
        axs[2, 4].set_title('Dynamic Pressure vs Time')

        plt.tight_layout()
        plt.show()

trajectory = "Elysium" # "Falcon 9"

if trajectory == "Elysium":
    print("running Elysium")
    elysium_trajectory = Trajectory()
    elysium_trajectory.setup(
        number_of_engines_ascent=9,
        number_of_engines_landing=3,
        number_of_engines_reentry=3,
        thrust=1_000_000, # newtons
        I_sp_1=306, # seconds
        I_sp_2=457, # seconds
        kick_angle=np.radians(45), # radians
        gamma_change_time=10, # seconds
        m_first_stage_total = 500e3,
        m_first_stage_structural_frac= 0.0578,
        m_second_stage_structural=9.272e3, # kg
        m_second_stage_propellant=85e3, # kg
        m_second_stage_payload=11.5e3, # kg
        delta_V_landing=500, # m / s
        delta_V_reentry=1_500, # m / s
        Cd_ascent=0.3,
        Cd_descent=1.0,
        diameter=5.4, # meters  
        reentry_burn_alt=55_000, # meters
        landing_burn_alt=5000, # meters
        gravity_turn_alt=10_000, # meters
    )
    elysium_trajectory.run()
elif trajectory == "Falcon 9":
    print("running Falcon9")
    falcon_9_trajectory = Trajectory()
    falcon_9_trajectory.setup(
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
        m_second_stage_structural=3.9e3, #3.9e3, # kg
        m_second_stage_propellant=92e3, # kg
        m_second_stage_payload=13.1e3,
        delta_V_landing=200, # m / s
        delta_V_reentry=2_000, # m / s
        Cd_ascent=0.4,
        Cd_descent=1.0,
        diameter=3.7, # meters
        reentry_burn_alt=55_000, # meters
        landing_burn_alt=1_000, # meters
        gravity_turn_alt=1.5e3 # meters
    )
    falcon_9_trajectory.run()