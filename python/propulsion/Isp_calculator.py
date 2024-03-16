# tries to derive another estimate for Isp using thermal rocket propulsion formulas
# Calculated value will be compared to historical data, and the current prediction for the prometheus engine
# these three estimates will form the basis for providing an Isp value in other calculations

# IMPORTS
import numpy as np
from volume_mass_calculator import get_propellant_mass_volume
from inputs import engine, first_stage, propellant

# INPUTS
g0 = 9.80665

# for the mixture
# Cp = ?   # specific heat at const pressure
# Cv = ?   # specific heat at const volume
# gamma = ~1.2 # Cp/Cv

for gamma in np.linspace(1.1, 1.3, 5):
    Ra = 8.314 # J/MK

    # calculate molar mass of propellant
    thrust = first_stage.Thrust
    burn_time = first_stage.time_burn_1st
    OF_ratio = engine.OF_ratio
    mass_ox, mass_fuel, volume_ox, volume_fuel = get_propellant_mass_volume(thrust, burn_time, OF_ratio)

    # determine molar mass of propellant absed on OF ratio
    n_moles_MH4 = mass_fuel / propellant.M_fuel
    n_moles_O2 = mass_ox / propellant.M_ox
    M_prop = (mass_fuel + mass_ox) / (n_moles_MH4 + n_moles_O2)

    # set combustion chamber temperature (based on sources)
    Tc = 3533  # K [https://space.stackexchange.com/questions/9741/what-is-the-temperature-inside-a-methane-oxygen-rocket-engine]

    # set combustion pressure and nozzle exit pressure (based on sources)
    Pc = 100e5  # Pa [https://en.wikipedia.org/wiki/Prometheus_(rocket_engine)]
    Pe = 0.4e5 # Pa [chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.eucass.eu/doi/EUCASS2017-537.pdf]
    ### second paper is good one, going into quite some detail and showing a graph of Isp vs pressure and mixture ratio. CAN be used as an extra source/reference

    # TRP formula (page 112)
    w = np.sqrt(2*gamma/(gamma-1)*Ra/M_prop*Tc*(1-(Pe/Pc)**((gamma-1)/gamma)))

    # TRP formula (page 14)
    Isp = w / g0

    print('Gamma:', np.round(gamma, 2))
    print('The estimated Isp based on TRP equations is:', Isp)







