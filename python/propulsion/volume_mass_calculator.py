from python.propulsion.inputs import engine as engine
from python.propulsion.inputs import first_stage as first_stage
from python.propulsion.inputs import Propellant

# determines propellant mass flow rate
def calculate_mass_flow_rate(thrust, Isp):
  # calculate mass flow based on Isp equation
  g0 = 9.80665
  mass_flow = thrust / (Isp * g0)
  print("mass flow",mass_flow)
  return mass_flow

# determine oxidiser and fuel mass and volume
def get_propellant_mass_volume(thrust, burn_time, of_ratio,t_fuel,t_ox,p_ox,p_fuel):
  # INPUTS
  g0 = 9.80665  # sea level gravitational parameter
  propellant = Propellant(t_ox,t_fuel,p_ox,p_fuel)


  Isp = engine.get_Isp(of_ratio)  # specific impulse
  density_ox = propellant.density_ox  # oxidiser density for input Temperature and Pressure (calculated using thermodynamic NIST database)
  density_fuel = propellant.density_fuel  # fuel density for input Temperature and Pressure (calculated using thermodynamic NIST database)

  # mass flow rate
  mass_flow = calculate_mass_flow_rate(thrust, Isp)

  # mass calculations
  mass_total = mass_flow * burn_time
  mass_ox = of_ratio / (1+of_ratio) * mass_total
  mass_fuel = 1 / (1+of_ratio) * mass_total

  # volume calculations
  volume_ox = mass_ox / density_ox
  volume_fuel = mass_fuel / density_fuel
  volume_total = volume_ox + volume_fuel

  # density calculations
  density_ox = density_ox
  density_fuel = density_fuel
  density_total = mass_total/volume_total

  # return what is required for the Propulsion() class
  return mass_ox, mass_fuel, volume_ox, volume_fuel


if __name__ == "__main__":
  thrust = first_stage.Thrust
  burn_time = first_stage.time_burn_1st
  of_ratio = 350
  mass_ox, mass_fuel, volume_ox, volume_fuel = get_propellant_mass_volume(thrust, burn_time, of_ratio)

  # return/print whatever you want
  print("mass_ox:",mass_ox,"mass_fuel:",mass_fuel,"Total mass:",mass_ox+mass_fuel)
  print("Volume_ox:",volume_ox,"Volume_fuel:",volume_fuel,"Total Volume",volume_ox+volume_fuel)















