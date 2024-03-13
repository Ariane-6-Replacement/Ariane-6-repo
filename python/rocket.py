from aerodynamics.aerodynamics import Aerodynamics
from control.control import Control
from python.propulsion.propulsion import Propulsion
from structure.structure import Structure
from trajectory.trajectory import Trajectory

class Rocket():
    def __init__(self):
        self.aerodynamics = Aerodynamics()
        self.control = Control()
        self.propulsion = Propulsion()
        self.structure = Structure()
        self.trajectory = Trajectory()

    # TEMP
    def print_inputs(self):
        print("Inputs:")
        print("Aerodynamics:", self.aerodynamics.input)
        print("Control:", self.control.input)
        print("Propulsion:", self.propulsion.input)
        print("Structure:", self.structure.input)
        print("Trajectory:", self.trajectory.input)

    # TEMP
    def print_outputs(self):
        print("Outputs:")
        print("Aerodynamics:", self.aerodynamics.output)
        print("Control:", self.control.output)
        print("Propulsion:", self.propulsion.output)
        print("Structure:", self.structure.output)
        print("Trajectory:", self.trajectory.output)
     
    def dry_mass(self):
        return self.aerodynamics.mass + self.propulsion.mass + self.structure.mass + self.trajectory.mass
    
    def iterate(self):
        
        trajectory_points = self.trajectory.points(self.aerodynamics.cd)
        dry_mass = self.dry_mass()
        thrust = self.control.thrust(self.aerodynamics.drag, trajectory_points, dry_mass)
        propellant_mass, propellant_volume, pressure = self.propulsion.propellant(thrust, dry_mass)
        tank_design = self.structure.tank_design(propellant_mass, propellant_volume, pressure, thrust)
        control = self.control.forces_moments(tank_design)
        
        
        
    

