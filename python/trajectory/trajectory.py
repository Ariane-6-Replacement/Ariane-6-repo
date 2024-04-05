import numpy as np
import matplotlib.pyplot as plt

# Main class for the trajectory simulator. This class contains all the functions and variables needed to simulate the
# ascent, reentry burn, and landing.

g_0 = 9.81 # [m / s^2]
R_earth = 6_371e3 # [m]
mu_earth = 3.986_004_418e14 # [m^3 / s^-2]

class Trajectory():
    def __init__(self):
        pass

    # Taken from https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
    def get_density(self, h):
        """Calculates atmospheric density at a given altitude.

        Args:
        h: Altitude in meters.

        Returns:
        Atmospheric density in kg/m^3.
        """
        if h < 11_000:
            # Troposphere: Use standard temperature and pressure model
            T = 15.04 - 0.00649 * h  # Temperature in Celsius
            p = 101.29 * ((T + 273.1) / 288.08) ** 5.256  # Pressure in Pa
        elif h < 25_000:
            # Stratosphere: Use constant temperature and exponential pressure model
            T = -56.46  # Temperature in Celsius
            p = 22.65 * np.exp(1.73 - 0.000157 * h)  # Pressure in Pa
        else:
            # Mesosphere and above: Use different temperature and pressure model
            T = -131.21 + 0.00299 * h  # Temperature in Celsius
            p = 2.488 * ((T + 273.1) / 216.6) ** -11.388  # Pressure in Pa

        rho = p / (0.2869 * (T + 273.1))  # Calculate density using ideal gas law
        return rho

    def get_drag(self, rho, velocity_x, velocity_z, A, Cd):
        """Calculates the drag force acting on the object.

        Args:
            rho: Atmospheric density (kg/m^3).
            velocity_x: Velocity in the x-direction (m/s).
            velocity_z: Velocity in the z-direction (m/s).
            A: Reference area of the object (m^2).
            Cd: Drag coefficient (unitless).

        Returns:
            Drag force (N).
        """

        drag = 0.5 * rho * (velocity_x**2 + velocity_z**2) * A * Cd  # Drag force formula
        return drag

    def get_gamma(self, velocity_z, velocity_x):
        """Calculates the flight path angle in radians.

        Args:
            velocity_z: Vertical velocity (m/s).
            velocity_x: Horizontal velocity (m/s).

        Returns:
            Flight path angle (radians).
        """

        return np.arctan2(velocity_z, velocity_x)  # Arctangent function for angle calculation

    def get_g(self, pos_z):
        """Calculates the acceleration due to gravity at a given altitude.

        Args:
            pos_z: Altitude (m).

        Returns:
            Acceleration due to gravity (m/s^2).
        """

        return -g_0 * (1 - 2 * pos_z / R_earth)  # Gravitational acceleration formula with altitude correction

    def get_propellant(self, I_sp_1, delta_V, M_remaining):
        """Calculates the propellant mass needed for a delta-V maneuver.

        Args:
            I_sp_1: Specific impulse of the first stage engine (s).
            delta_V: Desired change in velocity (m/s).
            M_remaining: Remaining mass of the vehicle (kg).

        Returns:
            Propellant mass needed (kg).
        """

        propellant = np.exp(delta_V / (I_sp_1 * g_0)) * (self.m_first_stage_structural + M_remaining) - (self.m_first_stage_structural + M_remaining)  # Rocket equation with exponential term
        return propellant

    def get_speed(self, velocity_x, velocity_z):
        """Calculates the total speed of the object.

        Args:
            velocity_x: Velocity in the x-direction (m/s).
            velocity_z: Velocity in the z-direction (m/s).

        Returns:
            Total speed (m/s).
        """

        return np.sqrt(velocity_x ** 2 + velocity_z ** 2)  # Pythagorean theorem for speed calculation
    
    def delta_V_circularize(self, r_1, r_2):
        """Calculates the delta-V required to circularize an orbit.

        Args:
            r_1: Initial circular orbit radius (m).
            r_2: Final circular orbit radius (m).

        Returns:
            Delta-V required for circularization (m/s).
        """

        # Use vis-viva equation to find circular velocity at r_2
        v_c2 = np.sqrt(mu_earth / r_2)

        # Calculate delta-V to match circular velocity from initial velocity
        delta_V_circularize = v_c2 - np.sqrt(mu_earth / r_1)
        return delta_V_circularize

    def delta_V_circular_to_elliptical(self, r_1, r_2):
        """Calculates the delta-V required to transfer from a circular orbit to an elliptical orbit.

        Args:
            r_1: Initial circular orbit radius (m).
            r_2: Final elliptical orbit apogee radius (m).

        Returns:
            Delta-V required for circular-to-elliptical transfer (m/s).
        """

        # Use vis-viva equation to find transfer orbit velocity at r_1
        v_transfer = np.sqrt(2 * mu_earth / r_1 * (1 - r_1 / r_2))

        # Calculate delta-V to achieve transfer orbit velocity from initial circular velocity
        delta_V_transfer = v_transfer - np.sqrt(mu_earth / r_1)
        return delta_V_transfer

    def delta_V_circular_to_circular(self, r_1, r_2):
        """Calculates the total delta-V required for a Hohmann transfer orbit.

        Args:
            r_1: Initial circular orbit radius (m).
            r_2: Final circular orbit radius (m).

        Returns:
            Total delta-V required for Hohmann transfer (m/s).
        """

        # Calculate delta-V for each burn using previously defined functions
        delta_V_1 = self.delta_V_circular_to_elliptical(r_1, r_2)  # Burn to transfer orbit
        delta_V_2 = self.delta_V_circularize(r_2, r_2)           # Burn to circularize at apogee

        # Total delta-V for the Hohmann transfer
        total_delta_V = delta_V_1 + delta_V_2
        return total_delta_V

    def get_required_second_stage_delta_V(self, pos_z, speed):
        """Calculates the delta-V required for the second stage to achieve GTO.

        Args:
            pos_z: Current altitude (m).
            speed: Current speed (m/s).

        Returns:
            Delta-V required for second stage to reach GTO (m/s).
        """

        # Calculate altitude from position
        altitude = R_earth + pos_z

        # Calculate circular velocity at current altitude
        v_c1 = np.sqrt(mu_earth / (altitude + R_earth))

        # Delta-V needed to circularize at current altitude
        delta_V_circ = v_c1 - speed

        # Define GTO parking orbit and apogee altitudes
        GTO_p = R_earth + 250e3  # GTO parking orbit (m)
        GTO_a = R_earth + 22_500e3 # GTO apogee (m)

        # Total delta-V required for second stage
        required_delta_V = (
            delta_V_circ  # Circularize at current altitude
            + self.delta_V_circular_to_circular(altitude, GTO_p)  # Hohmann transfer to GTO parking orbit
            + self.delta_V_circular_to_elliptical(GTO_p, GTO_a)  # Burn to GTO apogee
        )

        return required_delta_V

    
    def get_second_stage_structural_mass(self, second_stage_propellant_mass):
        """Calculates the structural mass of the second stage based on propellant mass.

        Args:
            second_stage_propellant_mass: Mass of propellant in the second stage (kg).

        Returns:
            Structural mass of the second stage (kg).
        """

        # Propellant mass exceeding base value (assumed for calculation)
        prop_mass_extension = second_stage_propellant_mass - 31_000

        # Overall feed ratio (ratio of oxidizer mass to fuel mass)
        of = 5.8

        # Fuel mass (assuming stoichiometric combustion)
        mf = prop_mass_extension / (of + 1)

        # Oxidizer mass
        mox = prop_mass_extension - mf

        # Fuel tank volume
        vf = mf / 70.8  # (kg / liter) density assumed

        # Oxidizer tank volume
        vox = mox / 1141  # (kg / liter) density assumed

        # Fuel tank radius based on volume
        Lf = vf / (np.pi * (2.7**2))  # Assuming spherical tanks

        # Oxidizer tank radius based on volume
        Lox = vox / (np.pi * (2.7**2))  # Assuming spherical tanks

        # Additional structural mass due to increased propellant
        struc_mass_extension = (Lf + Lox) * 3000 * np.pi * 5.4 * 5E-3  # Material density and tank wall thickness

        # Fixed structural masses (assumed constant)
        mfaring = 2657  # kg (interstage fairing)
        msyldas = 425  # kg (payload adapter)
        mcone = 200  # kg (nose cone)

        # Base structural mass based on reference propellant mass (assumed)
        mstruc = 4540 * (5.8 / 4.9) + 385  # Scaling factor for different propellant mass

        # Total structural mass of the second stage
        second_stage_structural_mass = mfaring + msyldas + mcone + mstruc + struc_mass_extension
        return second_stage_structural_mass

    def setup(self,
        simulation_timestep: float,
        simulation_time: float,
        number_of_engines_ascent: int,
        number_of_engines_landing: int,
        number_of_engines_reentry: int,
        thrust: float,
        I_sp_1: float,
        I_sp_2: float,
        kick_angle: float,
        gamma_change_time: float,
        m_first_stage_total: float,
        m_first_stage_structural_frac: float,
        m_second_stage_propellant: float,
        m_second_stage_payload: float,
        delta_V_landing: float,
        delta_V_reentry: float,
        Cd_ascent: float,
        Cd_descent: float,
        diameter: float,
        reentry_burn_alt: float,
        gravity_turn_alt: float,
        landing_type: str = None):
        """
        This function initializes the rocket object with its properties and performs some mass calculations.

        Args:
            simulation_timestep: Time step for the simulation (seconds).
            simulation_time: Total simulation time (seconds).
            number_of_engines_ascent: Number of engines used during ascent.
            number_of_engines_landing: Number of engines used during landing.
            number_of_engines_reentry: Number of engines used during reentry.
            thrust: Engine thrust (Newtons).
            I_sp_1: Specific impulse of the first stage engine (seconds).
            I_sp_2: Specific impulse of the second stage engine (seconds).
            kick_angle: Kick angle for engine gimbal (radians).
            gamma_change_time: Time to change flight path angle (seconds).
            m_first_stage_total: Total mass of the first stage (kg).
            m_first_stage_structural_frac: Ratio of structural mass to total mass for first stage.
            m_second_stage_propellant: Propellant mass of the second stage (kg).
            m_second_stage_payload: Payload mass of the second stage (kg).
            delta_V_landing: Delta-V required for landing (m/s).
            delta_V_reentry: Delta-V required for reentry (m/s).
            Cd_ascent: Drag coefficient for ascent.
            Cd_descent: Drag coefficient for descent.
            diameter: Diameter of the rocket (meters).
            reentry_burn_alt: Altitude for reentry burn (meters).
            gravity_turn_alt: Altitude for gravity turn maneuver (meters).
            landing_type: Optional string specifying the rocket type (default: None).
        """

        # Set landing type attribute
        self.landing_type = landing_type

        # Simulation parameters
        self.simulation_timestep = simulation_timestep
        self.simulation_time = simulation_time

        # Engine configuration
        self.number_of_engines_ascent = number_of_engines_ascent
        self.number_of_engines_landing = number_of_engines_landing
        self.number_of_engines_reentry = number_of_engines_reentry

        # Engine properties
        self.thrust = thrust
        self.I_sp_1 = I_sp_1
        self.I_sp_2 = I_sp_2
        self.initiate_landing_burn = False  # Flag for landing burn initiation (corrected typo)
        self.mass_flowrate = self.thrust / (g_0 * self.I_sp_1)  # Propellant mass flow rate

        # Flight control parameters
        self.kick_angle = kick_angle
        self.gamma_change_time = gamma_change_time

        # Stage masses (handled differently based on landing type)
        if self.landing_type == "Falcon 9":
            # Predefined values for Falcon 9
            self.m_first_stage_propellant = 395_700  # kg
            self.m_first_stage_structural = 25_600  # kg
            self.m_first_stage = 421_000  # kg
            self.Cd_ascent = 0.4
            self.m_second_stage_structural = 3.9e3  # kg
            self.m_second_stage_propellant = 92e3  # kg
            self.second_stage_thrust = 981e3  # Newtons
            self.landing_burn_alt = 1_000  # meters
        else:
            # Calculate mass based on provided parameters
            self.m_first_stage = m_first_stage_total
            self.m_first_stage_structural = self.m_first_stage * m_first_stage_structural_frac
            self.m_second_stage_propellant = m_second_stage_propellant
            self.second_stage_thrust = 180e3  # Newtons (assumed constant)
            self.m_second_stage_structural = self.get_second_stage_structural_mass(self.m_second_stage_propellant)

        # Propellant for landing and reentry burns (calculated based on Isp and Delta-V)
        self.m_prop_landing = self.get_propellant(self.I_sp_1, delta_V_landing, 0)
        self.m_prop_reentry = self.get_propellant(self.I_sp_1, delta_V_reentry, self.m_prop_landing)

        # Adjust first stage propellant for non-Falcon 9 based on landing and reentry needs
        if self.landing_type != "Falcon 9":
            self.m_first_stage_propellant = self.m_first_stage - (self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry)

        # Assert to ensure sufficient propellant for ascent
        assert self.m_first_stage_propellant > 0, "No propellant available for ascent"

        # Payload mass
        self.m_second_stage_payload = m_second_stage_payload

        # Burn time calculation
        self.burntime = self.m_first_stage_propellant / (self.mass_flowrate * self.number_of_engines_ascent)

        # Total second stage mass
        self.m_second_stage = self.m_second_stage_structural + self.m_second_stage_propellant + self.m_second_stage_payload

        # Total rocket mass
        self.m_total = self.m_first_stage + self.m_second_stage

        # Initial conditions
        self.mass = self.m_total
        self.delta_V_first_stage = self.I_sp_1 * g_0 * np.log(self.m_total / (self.m_total - self.m_first_stage_propellant))
        self.delta_V_second_stage = self.I_sp_2 * g_0 * np.log(self.m_second_stage / (self.m_second_stage - self.m_second_stage_propellant))


        # Aerodynamic properties
        self.Cd_ascent = Cd_ascent
        self.Cd_descent = Cd_descent
        self.area = np.pi * diameter ** 2 / 4

        # Flight control parameters
        self.reentry_burn_alt = reentry_burn_alt
        self.gravity_turn_alt = gravity_turn_alt

        # Initialize timing variables (all zero initially)
        self.kick_time = 0
        self.landing_burn_start_time = 0
        self.reentry_burn_start_time = 0

        # Initial state vector (position and velocity)
        self.pos_x = 0
        self.pos_z = 0
        self.velocity_x = 0
        self.velocity_z = 3  # Small initial vertical velocity to prevent rocket from hitting ground immediately.
        self.accel_x = 0
        self.accel_z = 0

        # Initialize storage arrays for simulation data (all empty initially)
        self.times = np.array([])
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

        # Initialize index variables for various phases of flight (for plotting color purposes) (all 0 initially)
        self.ascent_start_index = 0
        self.coasting_start_index = 0
        self.apogee_index = 0
        self.reentry_start_index = 0
        self.coasting2_start_index = 0
        self.landing_start_index = 0

        #self.max_barge_distance = 1000e3 # meters
        #self.max_apogee = 1000e3 # meters

        self.print_rocket_info = True

        # User can decide if trajectory simulation prints value estimates
        if self.print_rocket_info:
            # Print statements for initial mass breakdown
            print("First stage structural mass:", self.m_first_stage_structural / 1000, "t")
            print("First stage propellant mass:", self.m_first_stage_propellant / 1000, "t")
            print("First stage total mass:", self.m_first_stage / 1000, "t")

            print("Second stage structural mass:", self.m_second_stage_structural / 1000, "t")
            print("Second stage propellant mass:", self.m_second_stage_propellant / 1000, "t")
            print("Second stage total mass:", self.m_second_stage / 1000, "t")
            
            print("Total rocket mass:", self.m_total / 1000, "t")
            
            # Print statements for initial Delta-V, burn time, and propellant
            print("First Stage Delta V:", self.delta_V_first_stage / 1e3, "km / s")
            print("Second Stage Delta V:", self.delta_V_second_stage / 1e3, "km / s")
            print("Total Delta V:", (self.delta_V_first_stage + self.delta_V_second_stage) / 1e3, "km / s")
            print("Estimated Burntime:", self.burntime, "s")
            print("Propellant available for ascent:", self.m_first_stage_propellant / 1e3, "t")
            print("Propellant available for re-entry:", self.m_prop_reentry / 1e3, "t")
            print("Propellant available for landing:", self.m_prop_landing / 1e3, "t")
            print("Estimated First Stage TWR:", self.thrust*self.number_of_engines_ascent/(g_0*self.m_total))
            print("Estimated Second Stage TWR:", self.second_stage_thrust * 1/(g_0*self.m_second_stage))

    def iterate(self, t, dt):
        """
        This function performs a single simulation step for the rocket, updating its state based on 
        forces,  aerodynamics, and engine burns.

        Args:
            t: Current simulation time (seconds).
            dt: Simulation timestep (seconds).
        """

        # Get atmospheric density (assumed to depend only on altitude)
        rho = self.get_density(self.pos_z)

        # Check if the rocket has passed its apogee (highest point)
        before_apogee = self.velocity_z >= 0

        # Determine drag coefficient based on flight phase (ascent or descent)
        Cd = self.Cd_ascent if before_apogee else self.Cd_descent

        # Calculate drag force considering air density, velocity, and drag coefficient
        drag_force = self.get_drag(rho, self.velocity_x, self.velocity_z, self.area, Cd)

        # Calculate flight path angle based on vertical and horizontal velocities
        gamma = self.get_gamma(self.velocity_z, self.velocity_x)

        # Landing logic (specific to Falcon 9)
        if self.landing_type == "Falcon 9":
            landing = not before_apogee and self.pos_z < self.landing_burn_alt
        else:
            # Landing logic for non-Falcon 9 rockets (based on altitude and ground impact)
            if self.pos_z >= 0:
                impact_time = (np.sqrt(2 * g_0 * self.pos_z + self.velocity_z ** 2) + self.velocity_z) / g_0
            else:
                impact_time = 2 * self.velocity_z / g_0

            # Calculate deceleration time due to landing engines
            land_accel = self.number_of_engines_landing * self.thrust / (self.m_first_stage_structural + self.m_prop_landing)
            deccel_time = -self.velocity_z / (land_accel - g_0)

            # Initiate landing burn based on predicted impact time and descent conditions
            landing = not before_apogee and (deccel_time > impact_time and self.pos_z < 10e3 and self.iniate_landing_burn is False)
            self.iniate_landing_burn = landing  # Update flag for landing burn

        # Re-entry burn logic (similar to landing)
        reentering = not before_apogee and self.pos_z < self.reentry_burn_alt

        # Update burning state based on burn initiation time
        if landing:
            if self.landing_burn_start_time == 0:
                self.landing_burn_start_time = t
        elif reentering:
            if self.reentry_burn_start_time == 0:
                self.reentry_burn_start_time = t

        # Calculate fuel burned for each engine stage based on burn time and mass flow rate
        ascent_fuel_burned = np.clip(self.number_of_engines_ascent * self.mass_flowrate * (t - 0), 0, self.m_first_stage_propellant)
        landing_fuel_burned = np.clip(self.number_of_engines_landing * self.mass_flowrate * (t - self.landing_burn_start_time), 0, self.m_prop_landing)
        reentry_fuel_burned = np.clip(self.number_of_engines_reentry * self.mass_flowrate * (t - self.reentry_burn_start_time), 0, self.m_prop_reentry)

        # Check for available fuel for each engine stage
        ascent_fuel_available = ascent_fuel_burned < self.m_first_stage_propellant
        landing_fuel_available = landing_fuel_burned < self.m_prop_landing
        reentry_fuel_available = reentry_fuel_burned < self.m_prop_reentry

        # Determine current flight phase based on apogee and fuel availability
        ascending = before_apogee and ascent_fuel_available

        in_gravity_turn = self.pos_z >= self.gravity_turn_alt

        # Check for gravity turn maneuver initiation
        in_gravity_turn = self.pos_z >= self.gravity_turn_alt
        if in_gravity_turn and self.kick_time == 0:
            self.kick_time = t  # Initiate gravity turn at specified altitude
        if in_gravity_turn and t <= self.kick_time + self.gamma_change_time:
            gamma = self.kick_angle  # Apply engine gimbal for gravity turn

        # Total thrust considering active engines and current flight phase
        total_thrust = 0
        if ascending:
            self.mass = self.m_total - ascent_fuel_burned
            total_thrust = self.number_of_engines_ascent * self.thrust
        elif landing and landing_fuel_available:
            self.mass = self.m_first_stage_structural + self.m_prop_landing - landing_fuel_burned
            total_thrust = -self.number_of_engines_landing * self.thrust  # Negative thrust for landing burn (flipped velocity vector)
        elif reentering and reentry_fuel_available:
            self.mass = self.m_first_stage_structural + self.m_prop_landing + self.m_prop_reentry - reentry_fuel_burned
            total_thrust = -self.number_of_engines_reentry * self.thrust  # Negative thrust for re-entry burn (flipped velocity vector)
        
        # Print statements for tracking coasting and burning phases
        if not ascending and self.coasting_start_index == 0:
            if self.print_rocket_info:
                print("Rocket mass at start of coast phase:", self.mass / 1000, "t")
            self.coasting_start_index = self.counter
        elif reentering and self.reentry_start_index == 0:
            if self.print_rocket_info:
                print("Rocket mass at start of reentry phase:", self.mass / 1000, "t")
            self.reentry_start_index = self.counter
        elif reentering and not reentry_fuel_available and self.coasting2_start_index == 0:
            if self.print_rocket_info:
                print("Rocket mass at end of reentry phase:", self.mass / 1000, "t")
            self.coasting2_start_index = self.counter
        elif landing and self.landing_start_index == 0:
            if self.print_rocket_info:
                print("Rocket mass at start of landing phase:", self.mass / 1000, "t")
            self.landing_start_index = self.counter

        # Calculate thrust components in x (horizontal) and z (vertical) directions
        self.thrust_x = np.cos(gamma) * total_thrust / self.mass
        self.thrust_z = np.sin(gamma) * total_thrust / self.mass

        # Calculate drag components in x and z directions
        drag_x = -np.cos(gamma) * drag_force / self.mass
        drag_z = -np.sin(gamma) * drag_force / self.mass

        # Calculate total acceleration from thrust, drag, and gravity
        self.accel_x = self.thrust_x + drag_x
        self.accel_z = self.get_g(self.pos_z) + self.thrust_z + drag_z

        # Update velocities using accelerations and timestep
        self.velocity_x += self.accel_x * dt
        self.velocity_z += self.accel_z * dt

        # Update positions using velocities and timestep
        self.pos_x += self.velocity_x * dt
        self.pos_z += self.velocity_z * dt

        # Calculate speed from horizontal and vertical velocities
        speed = self.get_speed(self.velocity_x, self.velocity_z)

        # Store simulation data in arrays for later analysis
        # Ensure these are appended before any of the potential trajectory simulation exit conditions are called. 
        self.times = np.append(self.times, t)
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

        # Check for exceeding a maximum barge distance (removed for fully customizable IDM)
        # Set self.max_barge_distance in trajectory setup if this functionality is desired.
        #if self.pos_x > self.max_barge_distance:
            # print("Barge overshot!")
            #return False
    
         # Identify apogee and print details
        if not before_apogee and self.apogee_index == 0:
            print("Trajectory reached apogee!")
            self.apogee_index = self.counter
            apogee_z = self.pos_zs[self.apogee_index]
            apogee_velocity_x = self.velocity_xs[self.apogee_index]
            apogee_velocity_z = self.velocity_zs[self.apogee_index]
            apogee_speed = self.get_speed(apogee_velocity_x, apogee_velocity_z)

            # Optionally add a minimum required second stage delta V condition for the rocket.
            #required_delta_V = self.get_required_second_stage_delta_V(apogee_z, apogee_speed)
            #print("Required Second Stage Delta V:", required_delta_V / 1000, "km / s")
            # if required_delta_V > self.delta_V_second_stage:
            #     return False

            # Optionally add a maximum apogee condition for the rocket.
            # Set self.max_apogee in trajectory setup if this functionality is desired.
            #if apogee_z > self.max_apogee:
            #    return False
                
        # Check for safe landing conditions based on velocity and altitude
        if self.velocity_z > -5 and self.pos_z < 2e3 and not before_apogee:
            print("Trajectory landing burn may be unsuccessful due to uncertainties.")
            return False
        
        # Check if rocket goes below ground level
        below_ground = self.pos_z < -1000 # 1000 meters below ground chosen because large simultion time steps may "tunnel" through the ground.
        if below_ground:
            print("Trajectory may end up below ground due to uncertainties in landing burn altitude.")
            return False

        # Increment counter for simulation steps
        self.counter += 1
        return True
    
    # Function to add a single phase (flight segment) to a plot
    def add_phase(self, axis, xs, ys, legend_location, start, stop, color, linestyle, label='_'):
        """
        This function plots a segment of data (xs[start:stop], ys[start:stop]) on the provided axis (e.g., matplotlib). 

        Args:
            axis: The matplotlib axis object to add the plot to.
            xs: The list of x-axis data points.
            ys: The list of y-axis data points.
            legend_location: The location of the legend entry for this phase (e.g., 'upper left').
            start: The index to start plotting from the xs and ys lists.
            stop: The index to stop plotting (exclusive) from the xs and ys lists.
            color: The color of the line for this phase.
            linestyle: The line style (e.g., 'solid', 'dashed') for this phase.
            label: The label for this phase in the legend (optional, defaults to '_').
        """

        # Plot the data segment with specified color, linestyle, and label
        axis.plot(xs[start:stop], ys[start:stop], color=color, linestyle=linestyle, label=label)

        # Set legend properties (optional)
        axis.legend(loc=legend_location, prop={'size': 6})  # Set legend font size to 6

    # Function to add multiple flight phases to a plot
    def add_flight_phases(self, title, xlabel, ylabel, axis, xs, ys, legend_location, lower_y_zero_bound=True, coloring=True):
        """
        This function adds multiple flight phases (segments) to a plot, along with axis labels and title.

        Args:
            title: The title of the plot.
            xlabel: The label for the x-axis.
            ylabel: The label for the y-axis.
            axis: The matplotlib axis object to add the plot to.
            xs: The list of x-axis data points.
            ys: The list of y-axis data points.
            legend_location: The location of the legend (e.g., 'upper left').
            lower_y_zero_bound: If True, sets the lower y-axis limit to zero (optional).
            coloring: If True, colors the different flight phases (ascent, coasting, etc.) using predefined colors (optional).
        """

        # Set axis labels and title
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_title(title)

        # Optionally set lower y-axis limit to zero (commented out for customization)
        # if lower_y_zero_bound:
        #   axis.set_ylim(bottom=0)

        # Optionally set coloring for different flight phases
        if coloring:
            # Define color and linestyle for each flight phase
            self.add_phase(axis, xs, ys, legend_location, self.ascent_start_index, self.coasting_start_index, self.ascent_color, self.ascent_style, self.ascent_label)
            self.add_phase(axis, xs, ys, legend_location, self.coasting_start_index - 1, self.reentry_start_index, self.coasting_color, self.coasting_style, self.coasting_label)
            self.add_phase(axis, xs, ys, legend_location, self.reentry_start_index - 1, self.coasting2_start_index, self.reentry_color, self.reentry_style, self.reentry_label)
            self.add_phase(axis, xs, ys, legend_location, self.coasting2_start_index - 1, self.landing_start_index, self.coasting_color, self.coasting_style)
            self.add_phase(axis, xs, ys, legend_location, self.landing_start_index - 1, -1, self.landing_color, self.landing_style, self.landing_label)
        else:
            # If coloring is disabled, plot the entire data set without separation
            axis.plot(xs, ys)

    def setup_plot(self):
        """
        This function generates a grid of subplots and visualizes various aspects of the rocket simulation.
        """

        # Define colors and linestyles for different flight phases (ascent, coasting, etc.)
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

        # Create a figure with a 3x5 grid of subplots (15 total) and set the figure size
        fig, axs = plt.subplots(3, 5, figsize=(10, 8), layout="constrained")

        # -------- Plot Position vs Time --------
        # Plot position X vs time (converted to km for readability)
        self.add_flight_phases('Pos X vs Time', 'Time (s)', 'Pos X (km)', axs[0, 0], self.times, self.pos_xs / 1000, 'lower right')
        # Plot position Z vs time (converted to km for readability)
        self.add_flight_phases('Pos Z vs Time', 'Time (s)', 'Pos Z (km)', axs[0, 1], self.times, self.pos_zs / 1000, 'lower center')

        # -------- Plot Environmental Properties --------
        # Plot atmospheric density vs time
        self.add_flight_phases('Atmospheric Density vs Time', 'Time (s)', 'Atmospheric Density (kg/m^3)', axs[0, 2], self.times, self.rhos, 'upper center')
        # Plot drag force vs time (converted to MN for readability)
        self.add_flight_phases('Drag vs Time', 'Time (s)', 'Drag (MN)', axs[0, 3], self.times, self.drags / 1e6, 'upper center')
        # Plot position Z vs position X (trajectory)
        self.add_flight_phases('Pos Z vs Pos X', 'Pos X (km)', 'Pos Z (km)', axs[0, 4], self.pos_xs / 1000, self.pos_zs / 1000, 'lower center')

        # -------- Plot Velocity and Flight Path Angle --------
        # Plot velocity X vs time (converted to km/s for readability)
        self.add_flight_phases('Velocity X vs Time', 'Time (s)', 'Velocity X (km/s)', axs[1, 0], self.times, self.velocity_xs / 1000, 'lower center')
        # Plot velocity Z vs time (converted to km/s for readability)
        self.add_flight_phases('Velocity Z vs Time', 'Time (s)', 'Velocity Z (km/s)', axs[1, 1], self.times, self.velocity_zs / 1000, 'lower left')
        # Plot flight path angle vs time
        self.add_flight_phases('Flight Path Angle vs Time', 'Time (s)', 'Flight Path Angle (degrees)', axs[1, 2], self.times, self.gammas, 'lower left')
        # Set y-axis limits for flight path angle plot (-100 to 100 degrees)
        axs[1, 2].set_ylim(-100, 100)

        # -------- Plot Mass, Speed, and Acceleration --------
        # Plot mass vs time (converted to tonnes for readability)
        self.add_flight_phases('Mass vs Time', 'Time (s)', 'Mass (tonnes)', axs[1, 3], self.times, self.masses / 1000, 'upper center')
        # Plot speed vs time (converted to km/s for readability)
        self.add_flight_phases('Speed vs Time', 'Time (s)', 'Speed (km/s)', axs[1, 4], self.times, self.speeds / 1000, 'lower center')

        # Plot acceleration X vs time (normalized by g_0 for g-force units)
        self.add_flight_phases('Accel X vs Time', 'Time (s)', 'Accel X (g)', axs[2, 0], self.times, self.accel_xs / g_0, 'lower center')
        # Plot acceleration Z vs time (normalized by g_0 for g-force units)
        self.add_flight_phases('Accel Z vs Time', 'Time (s)', 'Accel Z (g)', axs[2, 1], self.times, self.accel_zs / g_0, 'upper center')

        # -------- Plot Thrust Forces --------
        # Plot thrust in X direction vs time (scaled by mass for total force)
        self.add_flight_phases('Thrust X vs Time', 'Time (s)', 'Thrust X (MN)', axs[2, 2], self.times, self.thrust_xs * self.masses / 10e5, 'upper center')
        # Plot thrust in Z direction vs time (scaled by mass for total force)
        self.add_flight_phases('Thrust Z vs Time', 'Time (s)', 'Thrust Z (MN)', axs[2, 3], self.times, self.thrust_zs * self.masses / 10e5, 'upper center')

        # -------- Plot Dynamic Pressure --------
        # Plot dynamic pressure vs time (converted to kPa for readability)
        self.add_flight_phases('Dynamic Pressure vs Time', 'Time (s)', 'Dynamic Pressure (kPa)', axs[2, 4], self.times, 0.5 * self.rhos * self.speeds ** 2 / 1000, 'upper center')

        return fig

    def run(self):
        """
        This function runs the main simulation loop for the rocket trajectory.
        """

        # Current simulation time (starts at 0)
        t = 0

        # Flag to track simulation success (defaults to True)
        success = True

        # Counter for simulation steps
        self.counter = 0

        # Print starting message
        print("Starting trajectory simulation!")

        # Calculate total number of simulation frames based on simulation time and timestep
        frames = self.simulation_time / self.simulation_timestep

        # Counter for completed simulation tenths (for progress updates)
        completed_tenths = 0

        # Main simulation loop that iterates until simulation time is reached
        while t < self.simulation_time:
            # Check if progress update is needed (every 10% completion)
            if int(self.counter / frames * 100) >= 10 * completed_tenths:
                completed_tenths += 1
                # Print progress update (e.g., "Completed 10% of trajectory simulation")
                print("Completed {:.0%} of trajectory simulation".format(completed_tenths * 10 / 100))

            # Update simulation time by the timestep
            t += self.simulation_timestep

            # Perform a single simulation step and update success flag
            success = self.iterate(t, self.simulation_timestep)
            # Exit the loop if simulation reaches an exit condition set by the IDM user.
            if not success:
                break

        # Print ending message
        print("Completed {:.0%} of trajectory simulation".format(1))
        
# This block of code only executes if the script is run directly (not imported as a module)
if __name__ == "__main__":

    # Select the trajectory to simulate (either "Elysium" or "Falcon 9")
    trajectory = "Elysium"  # Choose between "Elysium" or "Falcon 9"

    if trajectory == "Elysium":
        print("Running Elysium trajectory...")

        # Create a Trajectory object for the Elysium simulation
        elysium_trajectory = Trajectory()

        # Define parameters specific to the Elysium trajectory
        first_stage_ascent_prop_margin = 1.02  # Propellant margin for ascent stage (1.02 means 2% extra propellant)
        first_stage_landing_prop_margin = 1.1  # Propellant margin for landing stage (1.1 means 10% extra propellant)
        first_stage_reentry_prop_margin = 1.05  # Propellant margin for reentry stage (1.05 means 5% extra propellant)

        # Configure the Elysium trajectory with various parameters
        elysium_trajectory.setup(
            # Simulation settings
            simulation_timestep=0.01,  # Time step for each simulation step in seconds
            simulation_time=900,        # Total simulation time in seconds

            # Engine configuration
            number_of_engines_ascent=9,  # Number of engines used during ascent stage
            number_of_engines_landing=1,  # Number of engines used during landing stage
            number_of_engines_reentry=3,  # Number of engines used during reentry stage

            # Engine performance
            thrust=1_000_000,           # Engine thrust in Newtons
            I_sp_1=306,                   # Specific impulse (efficiency) of engine 1 in seconds
            I_sp_2=457,                   # Specific impulse (efficiency) of engine 2 in seconds

            # Launch profile
            kick_angle=np.radians(68),  # Launch angle in radians
            gamma_change_time=10,          # Time taken to transition to desired flight path angle in seconds

            # Vehicle mass properties
            m_first_stage_total=400e3 * first_stage_ascent_prop_margin,  # Total mass of first stage (including propellant) in kg
            m_first_stage_structural_frac=0.0578,  # Ratio of structural mass to total mass for first stage
            m_second_stage_propellant=80e3,  # Propellant mass of second stage in kg
            m_second_stage_payload=11.5e3,  # Payload mass of second stage in kg

            # Landing and reentry parameters
            delta_V_landing=909 * first_stage_landing_prop_margin,  # Required delta-V for landing in m/s (adjusted by propellant margin)
            delta_V_reentry=1905 * first_stage_reentry_prop_margin,  # Required delta-V for reentry in m/s (adjusted by propellant margin)
            Cd_ascent=0.3,                 # Drag coefficient for ascent stage
            Cd_descent=1.0,                # Drag coefficient for descent stage
            diameter=5.4,                 # Rocket diameter in meters
            reentry_burn_alt=55_000,       # Altitude for reentry burn in meters
            gravity_turn_alt=10_000        # Altitude for gravity turn maneuver in meters
        )

        # Run the simulation for the Elysium trajectory
        elysium_trajectory.run()

        # Plot the results of the Elysium trajectory simulation
        elysium_trajectory.setup_plot()
        plt.show()

    elif trajectory == "Falcon 9":
        print("Running Falcon 9 trajectory...")

        # Create a Trajectory object for the Falcon 9 simulation
        falcon_9_trajectory = Trajectory()

        # Configure the Falcon 9 trajectory with various parameters
        falcon_9_trajectory.setup(
            # Simulation parameters
            simulation_timestep=0.01,  # Time step for each simulation step in seconds
            simulation_time=900,        # Total simulation time in seconds

            # Engine configuration
            number_of_engines_ascent=9,  # Number of engines used during ascent stage
            number_of_engines_landing=1,  # Number of engines used during landing stage
            number_of_engines_reentry=3,  # Number of engines used during reentry stage

            # Engine performance
            thrust=805_000 * 1,           # Engine thrust in Newtons (1 here likely means nominal thrust)
            I_sp_1=283,                   # Specific impulse (efficiency) of engine 1 in seconds
            I_sp_2=348,                   # Specific impulse (efficiency) of engine 2 in seconds (might not be used for Falcon 9)

            # Launch profile
            kick_angle=np.radians(75.5),  # Launch angle in radians
            gamma_change_time=8,          # Time taken to transition to desired flight path angle in seconds

            # Vehicle mass properties
            m_first_stage_total=421e3,     # Total mass of first stage (including propellant) in kg
            m_first_stage_structural_frac=0.045,  # Ratio of structural mass to total mass for first stage
            m_second_stage_propellant=92e3,  # Propellant mass of second stage in kg
            m_second_stage_payload=13.1e3,  # Payload mass of second stage in kg

            # Landing and reentry parameters
            delta_V_landing=200,           # Required delta-V for landing in m/s
            delta_V_reentry=2_000,         # Required delta-V for reentry in m/s
            Cd_ascent=0.4,                 # Drag coefficient for ascent stage
            Cd_descent=1.0,                # Drag coefficient for descent stage
            diameter=3.7,                 # Rocket diameter in meters
            reentry_burn_alt=55_000,       # Altitude for reentry burn in meters
            gravity_turn_alt=1.5e3,        # Altitude for gravity turn maneuver in meters

            # Additional parameter specific to Falcon 9 landing
            landing_type="Falcon 9"
        )

        # Run the simulation for the Falcon 9 trajectory
        falcon_9_trajectory.run()

        # Plot the results of the Falcon 9 trajectory simulation
        falcon_9_trajectory.setup_plot()
        plt.show()