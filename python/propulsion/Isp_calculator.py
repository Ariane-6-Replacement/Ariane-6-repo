# tries to derive a second estimate for Isp using thermal rocket propulsion formulas
# Calculated value will be compared to historical data, and the current prediction for the prometheus engine
# these three estimates will form the basis for providing an Isp value in other calculations

# IMPORTS
import numpy as np
from volume_mass_calculator import OF_ratio, mass_fuel, mass_ox, mass_total

# INPUTS
g0 = 9.80665


# for the mixture
Cp = 1.2
Cv = 1.0

gamma = Cp/Cv # or other way around
Ra = 8.314 # J/MK

# calculate molar mass of propellant
M_MH4 = 16.04/1000   # kg/mol
M_O2 = 32.00/1000     # kg/mol

n_moles_MH4 = mass_fuel / M_MH4
n_moles_O2 = mass_ox / M_O2

M_prop = mass_total / (n_moles_MH4 + n_moles_O2)



M_prop = ((1 / (1 + R)) * 16.04 ) + ((R / (1 + R)) * 32.00 )


# TRP formula page 112
w = np.sqrt(2*gamma/(gamma-1)*Ra/M*Tc*(1-(pe/pc)**((gamma-1)/gamma)))



Isp = w * g0








