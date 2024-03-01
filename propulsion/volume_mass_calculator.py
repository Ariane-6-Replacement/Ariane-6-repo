from inputs import FirstStageRequirements, Prometheus, Fuel


engine = Prometheus()
first_stage = FirstStageRequirements()
fuel = Fuel()

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


mass_flow = first_stage.Thrust / (engine.Isp*9.80665)
burn_time = first_stage.time_burn_1st

Total_mass = mass_flow * burn_time

OF_ratio = engine.OF_ratio
mass_ox = OF_ratio / (1+OF_ratio) * Total_mass
mass_fuel = 1 / (1+OF_ratio) * Total_mass
rho_ox = fuel.rho_LOX
rho_fuel = fuel.rho_LM
volume_ox = mass_ox / rho_ox
volume_fuel = mass_fuel / rho_fuel

Total_volume = volume_ox + volume_fuel
print(Total_volume)
# VERIFY THAT IT WORKS!!!



# average_density = calculate_average_fuel_density(OF_ratio, fuel.rho_LOX, fuel.rho_LM)
# Total_volume = Total_mass/average_density
# print(Total_volume)













