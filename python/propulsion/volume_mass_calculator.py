# IMPORTS
from inputs import FirstStageRequirements, Prometheus, Fuel

# INPUTS
engine = Prometheus()
first_stage = FirstStageRequirements()
fuel = Fuel()

g0 = 9.80665
thrust = first_stage.Thrust
Isp = engine.Isp
burn_time = first_stage.time_burn_1st
OF_ratio = engine.OF_ratio
rho_ox = fuel.rho_LOX
rho_fuel = fuel.rho_LM


# DEFENITIONS
def calculate_average_fuel_density(fuel_ratio, oxidizer_density, propellant_density):
  """
  Calculates the average fuel density based on the fuel ratio, oxidizer density, and propellant density.

  Args:
      fuel_ratio: Ratio of oxidizer mass to fuel mass.
      oxidizer_density: Density of the oxidizer in kg/m^3.
      propellant_density: Density of the propellant in kg/m^3.

  Returns:
      The average fuel density in kg/m^3.
  """
  
  average_density = (fuel_ratio * propellant_density + oxidizer_density) / (1 + fuel_ratio)

  return average_density


def calculate_propellant_mass_flow_rate(thrust, Isp):
  # calculate mass flow based on Isp equation
  mass_flow = thrust / (Isp*g0)
  return mass_flow


# (checked)
mass_flow = calculate_propellant_mass_flow_rate(thrust, Isp)
total_mass = mass_flow * burn_time

# (checked)
mass_ox = OF_ratio / (1+OF_ratio) * total_mass
mass_fuel = 1 / (1+OF_ratio) * total_mass

# (checked)
volume_ox = mass_ox / rho_ox
volume_fuel = mass_fuel / rho_fuel
total_volume = volume_ox + volume_fuel


print("mass flow:",mass_flow)
print("mass_ox:",mass_ox,"mass_fuel:",mass_fuel,"Total mass:",mass_ox+mass_fuel)
print("Volume_ox:",volume_ox,"Volume_fuel:",volume_fuel,"Total Volume",total_volume)


# IT WORKS :-) !!!

print(rho_fuel, rho_ox)














