import numpy as np
from scipy.optimize import fsolve


"""
Equations of Motion:
dV_x/dt     = 1/M ( T cos(theta + a_t) - L sin(gamma) - D cos(gamma) )
dV_z/dt     = 1/M ( T sin(theta + a_t) + L cos(gamma) - D sin(gamma) - g )
dTheta/dt   = 1/r dV_p/dt - V_p / r^2 dr/dt

gamma = arctan(Vz / Vx)
theta = gamma + alpha

Control variables:
    - Thrust
    - a_t

Disturbances:
    - Lift
    - Drag
"""


def force_eq(thrust, mass, gravity, ax0=0, ay0=0):
    thrust_x, thrust_z = thrust
    ax = thrust_x / mass - ax0
    az = thrust_z / mass - gravity - ay0
    return ax, az


class Control:
    def __init__(self):
        # Structures inputs
        self.moment_of_inertia = 0
        self.mass = 0
        self.center_of_gravity = 0
        self.center_of_pressure = 0

        # Propulsion inputs
        self.thruster = 0 # propulsion.Thruster()
        self.tvc = 0 # propulsion.TVC()

        self.aerodynamic_loading = []

        self.trajectory_profile = 0 # DesiredFlightPath()

        # Outputs
        self.control_surfaces = 0 # ControlSurfaces()

        self.tvc_forces = [0, 0, 0]
        self.tvc_moments = [0, 0, 0] 

        self.input = [self.moment_of_inertia, self.mass, self.center_of_gravity, self.center_of_pressure]

        self.output = [self.control_surfaces, self.tvc_forces, self.tvc_moments]
        self.state = np.array([0, 0, 0, 0])  # x, z, Vx, Vz

    # Where are we?
    def current_state(self):
        # returns np.array([x, z, Vx, Vz])
        pass

    # Where should we be?
    def desired_state(self):
        pass

    # What to do to get there?
    def control_input(self):
        pass

    def disturbances(self):
        x_disturbance, z_disturbance = np.random.random(2) * self.mass * 9.81
        return x_disturbance, z_disturbance

    def dummy_control_one(self, target_position: np.ndarray, time_array: np.ndarray, gravity: np.ndarray):
        # Check inputs are correct
        assert(np.shape(target_position)[0] == np.size(time_array),
               'target_position needs to be a Nx2 array while time_array is a 1D N-size array')

        for i in range(len(time_array)):
            # Obtain time interval
            dt = time_array[i + 1] - time_array[i]

            # Calculate necessary velocity
            velocity = (target_position - self.state[:2]) / dt

            # Calculate necessary force to arrive
            delta_v = velocity - self.state[2:]
            ax, az = delta_v / dt

            sol = fsolve(force_eq, np.array([1, 1.1 * self.mass * gravity[i]]),
                         args=(self.mass, gravity[i], ax, az))

            # Introduce disturbances
            Fx, Fz = sol - self.disturbances()

            # Update current state
            ax, az = force_eq((Fx, Fz), self.mass, gravity[i])
            self.state[2] += ax * dt
            self.state[3] += az * dt
            self.state[0] += self.state[2] * dt
            self.state[1] += self.state[3] * dt

