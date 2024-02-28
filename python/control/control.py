#from trajectory.trajectory import DesiredFlightPath
#from surfaces import ControlSurfaces
#import propulsion

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

    # Where are we?
    def current_state(self):
        flight_path_angle = [] # x, y, z

        return flight_path_angle

    # Where should we be?
    def desired_state(self):
        pass

    # What to do to get there?
    def control_input(self):
        pass