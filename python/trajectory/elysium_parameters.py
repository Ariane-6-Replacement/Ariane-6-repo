import numpy as np
from python.propulsion.propulsion import propulsion


thrust = 980e3 # newtons
burntime = 140.3 # s
# First stage mass at beginning of ascent
M0_1 = 700e3 # kg
# Empty mass
M_empty = 40e3 # kg

number_of_engines_ascent = 9
number_of_engines_landing = 1
number_of_engines_reentry = 3
diameter = 5.4 # meters

struct_coeff_2nd_stage = 0.75
I_sp_1 = 306 # s
I_sp_2 = 457
delta_V_landing = 200 # [m / s]
delta_V_reentry = 1_300 # [m / s]

Cd_ascent = 0.3
Cd_descent = 1

A = np.pi * diameter ** 2 / 4
reentry_burn_alt = 55_000 # meters
landing_burn_alt = 800 # meters
gravity_turn_alt = 10_000 # meters

kick_angle = np.radians(45)
gamma_change_time = 10 # seconds

mass_flowrate = 333 # kg / s