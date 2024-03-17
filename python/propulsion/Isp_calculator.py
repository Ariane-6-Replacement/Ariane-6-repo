# tries to derive another estimate for Isp using thermal rocket propulsion formulas
# Calculated value will be compared to historical data, and the current prediction for the prometheus engine
# these three estimates will form the basis for providing an Isp value in other calculations

# IMPORTS
import numpy as np
from volume_mass_calculator import get_propellant_mass_volume
from inputs import engine, first_stage, propellant

# source: https://www.nextbigfuture.com/2023/07/ariane-test-fires-reusable-prometheus-rocket-engine.html
def get_Isp_source1():
    return 360

# source: paper: 'High-Performance, Partially Reusable Launchers for Europe'
# paper states: estimated Isp for prometheus CH4 variant = 287s (sea level) and 319 (vacuum)
def get_Isp_source2():
    return 287

# source: paper: European Next Reusable Ariane (ENTRAIN): A Multidisciplinary Study on a VTVL and a VTHL Booster Stage
# paper estimates Isp for first stage of reusable booster = 288
def get_Isp_source3():
    return 288


# TODO find representitive historical data
def get_Isp_historical():
    # TODO find representitive historical data
    return 300



# use thermal rocket propulsion equations in order to calculate Isp
def get_Isp_trp(): 
    # INPUTS
    g0 = 9.80665

    # for the mixture
    # Cp = ?   # specific heat at const pressure
    # Cv = ?   # specific heat at const volume
    gamma = 1.2 # Cp/Cv

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

    print('The estimated Isp based on TRP equations is:', Isp, 'for gamma =', gamma)

    return Isp


# tries to find a good estimate for the Isp of prometheus, based on calculations and sources.
def estimate_Isp():
    # calculate Isp based on TRP equations
    Isp_calc = get_Isp_trp()

    # determine Isp based on historical data
    Isp_his = get_Isp_historical()

    # determine Isp based on sources
    Isp1 = get_Isp_source1()
    Isp2 = get_Isp_source2()
    Isp3 = get_Isp_source3()

    Isp_estimated = np.average([Isp_calc, Isp1, Isp2, Isp3])

    return Isp_estimated



Isp_estimated = estimate_Isp()
print(Isp_estimated)









