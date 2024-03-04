import geometry
from NASA_SP8007 import buckling, pressure_loading, buckling_coeff, bending, axial_stress

from Others.constants import FOSY 
class Cylinder:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 pressure: float,
                 thrust: float,
                #  stiffening_elastic_constants: tuple,
                 height:float,
                #  stiffening_volume: float
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
        self.thickness = pressure
        self.material = material
        self.height = height
        self.thrust =thrust
        # self.stiffening_elastic_constants = stiffening_elastic_constants
        # self.stiffening_volume = stiffening_volume



    
    @property
    def section_Ixx(self) -> float:
        return geometry.cylindrical_shell_I(self.outer_radius, self.thickness)


    @property
    def thickness(self) -> float:
        #Calcualte Basic Thickness:
        t_p= pressure_loading.t_hoop_stress(self.material['yield_stress'], self.outer_radius, FOSY, self.pressure)
        #Caclculate Axial Stress Thickness:
        t_a = axial_stress.t_axial(self.material['yield_stress'], self.outer_radius, FOSY, self.thrust)
        #Calcualte critical Buckling stress
        if t_a>t_p:
            t=t_a
        else:
            t=t_p
        s_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,
                                                         self.thickness, self.height, 
                                                   self.material['youngs_modulus'],self.material['poisson_ratio'])
        
        while s_buckling/FOSY >= self.material['yield_stress']:
            t+=0.001
            s_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,
                                                         self.thickness, self.height, 
                                                   self.material['youngs_modulus'],self.material['poisson_ratio'])
        s_bending = bending.critical_cylinder_bending(self.outer_radius, t ,self.pressure, self.material['youngs_modulus'],
                                           self.material['poisson_ratio'], self.section_Ixx)
        #NOTE Fact check this assumption 
        while s_bending/FOSY >= self.material['yield_stress']:
            t+=0.001
            s_bending = bending.critical_cylinder_bending(self.outer_radius, t 
            ,self.pressure, self.material['youngs_modulus'],self.material['poisson_ratio'], self.section_Ixx)
        return t
    
    def inner_volume(self) -> float:
        return geometry.cylinder_V(self.outer_radius-self.thickness, self.height)

    @property
    def outer_volume(self) -> float:
        return geometry.cylinder_V(self.outer_radius, self.height)

    @property
    def section_Iyy(self) -> float:
        return self.section_Ixx

    @property
    def mass(self) -> float:
        material_volume = self.outer_volume - self.inner_volume
        return self.material["density"] * material_volume


    @property
    def sectional_area(self) -> float:
        return geometry.cylindrical_shell_A(self.outer_radius, self.thickness)
    


    # @property
    # def stiffening_elastic_constants(self):
    #     return self._stiffening_elastic_constants

    # @stiffening_elastic_constants.setter
    # def stiffening_elastic_constants(self, value):
    #     self._stiffening_elastic_constants = value

    
    #  @property
    # def section_Iyy(self) -> float:
    #     # TODO: Adjust for stiffeners
    #     return self.section_Ixx

    # @property
    # def mass(self) -> float:
    #     # TODO: Adjust for stiffeners
    #     material_volume = self.outer_volume - self.inner_volume
    #     material_volume += self.stiffening_volume
    #     return self.material["density"] * material_volume

    # @property
    # def sectional_area(self) -> float:
    #     # TODO: Adjust for stiffeners
    #     return geometry.cylindrical_shell_A(self.outer_radius, self.thickness)


