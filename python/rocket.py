from aerodynamics.aerodynamics import Aerodynamics
from control.control import Control
from propulsion.propulsion import Propulsion
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

