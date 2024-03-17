import python.structure.geometry as geometry
import  python.structure.buckling as buckling
import python.structure.pressure_loading as pressure_loading
import python.structure.bending as bending
import python.structure.axial_stress as axial_stress
from python.structure.constants import FOSY
import numpy as np
class Cylinder:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 pressure: float,
                 thrust: float,
                #  moment:float,
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
        self.pressure = pressure
        self.material = material
        self.height = height
        self.thrust =thrust
    
        



    
    @property
    def section_Ixx(self) -> float:
        return geometry.cylindrical_shell_I(self.outer_radius, self.thickness)


    @property
    def thickness(self) -> float:
        #Calcualte Basic Thickness:
        t_p= pressure_loading.t_hoop_stress(self.material['yield_stress'], self.outer_radius, FOSY, self.pressure)
        #Caclculate Axial Stress Thickness:
        t_a = axial_stress.t_axial(self.material['yield_stress'], self.outer_radius, FOSY, self.thrust)
        # Calcualte critical Buckling stress
        if t_a>t_p:
            t=t_a
        else:
            t=t_p
        print('Intermediate t: ', t)
        #NOTE: Extra condition on unpressurized buckling, check the ratio of dry to wet mass
        s_buckling_stat = buckling.critical_cylinder_buckling(0, self.outer_radius,  t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])
        while s_buckling_stat/FOSY < self.thrust/1.5:
            t+=0.0005
            s_buckling_stat = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])

        s_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,
                                                         t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])
                                                 
    
        while s_buckling/self.thrust < FOSY :
            t+=0.0005
            s_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])
    
        Ixx = geometry.cylindrical_shell_I(self.outer_radius, t)
        s_bending = bending.critical_cylinder_bending(self.outer_radius, t 
            ,self.pressure, self.material['youngs_modulus'],self.material['poisson_ratio'], Ixx)
        print("Test s_bending: ",s_bending)
        #NOTE Fact check this assumption 
        while s_bending/(0.8*41603151.4) < FOSY:
            t+=0.0005
            Ixx = geometry.cylindrical_shell_I(self.outer_radius, t)
            s_bending = bending.critical_cylinder_bending(self.outer_radius, t 
            ,self.pressure, self.material['youngs_modulus'],self.material['poisson_ratio'], Ixx)
        return round(t,4)
    @property
    def area(self)->float:
        return self.height * 2 * np.pi * self.outer_radius
    @property
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
    

    @property
    def insulation(self)->float:
        return self.area*1.123
    
   