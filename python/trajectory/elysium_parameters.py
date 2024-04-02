import numpy as np

thrust = 1_000_000 # newtons
burntime = 100 # s
# First stage mass at beginning of ascent
M0_1 = 700e3 # kg
# Empty mass
M_empty = 40e3 # kg

number_of_engines_ascent = 9
number_of_engines_descent = 3
diameter = 5.4 # meters

struct_coeff_2nd_stage = 0.75
I_sp_1 = 357 # s
I_sp_2 = 457
delta_V_landing = 1_500 # [m / s]

Cd_ascent = 0.3
Cd_descent = 1

A = np.pi * diameter ** 2 / 4
burn_alt = 1_250 # meters
gravity_turn_alt = 10e3 # meters

kick_angle = np.radians(45)
gamma_change_time = 10 # seconds

mass_flowrate = 409 # kg / s