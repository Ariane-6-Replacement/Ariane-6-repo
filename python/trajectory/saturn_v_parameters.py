import numpy as np

thrust = 33_375_000 # newtons
burntime = 152 # s
# First stage mass at beginning of ascent
M0_1 = 2_776_100 # kg
# First stage mass at end of ascent
M0 = 80e3
number_of_engines_ascent = 1
number_of_engines_descent = 1
diameter = 10.1

Cd_ascent = 0.2
Cd_descent = 1

A = np.pi * diameter ** 2 / 4
burn_alt = 3080 # meters
gravity_turn_alt = 10e3 # meters

kick_angle = np.radians(80)
gamma_change_time = 10 # seconds

mass_flowrate = 12895 # kg / s