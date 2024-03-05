import geometry
import  isogrid_stress import critical_stress
from elastic_properties import isotropic_isogrid_stiffened_cylinders
from constants import FOSY 
class Shell:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 thrust: float,
                 height:float,
                 ):
        """
        Cylinder object, containing all relevant parameters. Cylinder coordinate system is defined with the origin at the
        center of the bottom edge. The z_c axis moves along the cylinder's axis in the direction from aft to forward.
        :param outer_radius: in m
        :param thickness: in m
        :param height: in m
        :param material: dictionary object from materials database
        """

        # These are the parameters that are passed to the class:
        self.outer_radius = outer_radius
        self.material = material
        self.height = height
        self.thrust =thrust


   




    @property
    def height(self):
        return 1.5
    

    @property
    def mass(self):
