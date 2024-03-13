# IMPORTS
from inputs import FirstStageRequirements, Prometheus, Propellant

# INPUTS
engine = Prometheus()
first_stage = FirstStageRequirements()
propellant = Propellant()

g0 = 9.80665
thrust = first_stage.Thrust
Isp = engine.Isp
burn_time = first_stage.time_burn_1st
OF_ratio = engine.OF_ratio
density_ox = propellant.density_ox
density_fuel = propellant.density_fuel


# DEFENITIONS
def calculate_propellant_mass_flow_rate(thrust, Isp):
  # calculate mass flow based on Isp equation
  mass_flow = thrust / (Isp*g0)
  return mass_flow


# mass flow rate
mass_flow = calculate_propellant_mass_flow_rate(thrust, Isp)

# mass calculations
mass_total = mass_flow * burn_time
mass_ox = OF_ratio / (1+OF_ratio) * mass_total
mass_fuel = 1 / (1+OF_ratio) * mass_total

# volume calculations
volume_ox = mass_ox / density_ox
volume_fuel = mass_fuel / density_fuel
volume_total = volume_ox + volume_fuel

# density calculations
density_ox = density_ox
density_fuel = density_fuel
density_total = mass_total/volume_total


if __name__ == "__main__":
  # return/print whatever you want
  print("mass flow:",mass_flow)
  print("mass_ox:",mass_ox,"mass_fuel:",mass_fuel,"Total mass:",mass_ox+mass_fuel)
  print("Volume_ox:",volume_ox,"Volume_fuel:",volume_fuel,"Total Volume",volume_total)















