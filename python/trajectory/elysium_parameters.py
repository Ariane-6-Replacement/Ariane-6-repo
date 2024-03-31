import numpy as np

thrust = 1_000_000 # newtons
burntime = 120.3 # s
# First stage mass at beginning of ascent
M0_1 = 700e3 # kg
# First stage mass at end of ascent
M0 = 80e3
number_of_engines_ascent = 9
number_of_engines_descent = 3
diameter = 5.4 # meters

Cd_ascent = 1
Cd_descent = 1

A = np.pi * diameter ** 2 / 4
burn_alt = 3080 # meters
gravity_turn_alt = 10e3 # meters

kick_angle = np.radians(80)
gamma_change_time = 10 # seconds

mass_flowrate = 12895 / 3.5 # kg / s