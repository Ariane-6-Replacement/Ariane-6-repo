import python.structure.geometry as geometry
from python.structure.Loading import buckling, pressure_loading, bending, axial_stress
from python.structure.constants import FOSY, Mi
import numpy as np

class Cylinder:
    def __init__(self,
                 outer_radius: float,
                 material: dict,
                 pressure: float,
                 thrust: float,
                 height:float):
        """
        Cylinder object, containing all relevant parameters. 
        :param outer_radius: in m
        :param pressure: in Pa
        :param thrust: in N
        :param material: dictionary object from materials database
        """

        self.outer_radius = outer_radius
        self.pressure = pressure
        self.material = material
        self.height = height
        self.thrust = thrust
    
        



    
    @property
    def section_Ixx(self) -> float:
        return geometry.cylindrical_shell_I(self.outer_radius, self.thickness)


    @property
    def thickness(self) -> float:

        #NOTE: Assumption thin walled, hoop stress >> longitudinal stress; Yielding is not acceptable during operations; Torsion effect is negligable comapred to bending and axial force;

        #Calculate Hoop Stress Thickness: 
        t_p= pressure_loading.t_hoop_stress(self.material['yield_stress'], self.outer_radius, FOSY, self.pressure)
        # Calculate Axial Stress Thickness:
        t_a = axial_stress.t_axial(self.material['yield_stress'], self.outer_radius, FOSY, self.thrust)
        # Calcualte critical Buckling stress
        if t_a>t_p:
            t=t_a
        else:
            t=t_p

        #Unpressurized buckling condition check
        N_buckling_stat = buckling.critical_cylinder_buckling(0, self.outer_radius,  t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])

        #Factor 1.5 - lowest possible T/W 
        while N_buckling_stat/FOSY < self.thrust/1.5:
            t+=0.0005
            N_buckling_stat = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])

        #Pressuirzed buckling condition check
        N_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,
                                                         t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])
                                                 
    
        while N_buckling/self.thrust < FOSY :
            t+=0.0005
            N_buckling = buckling.critical_cylinder_buckling(self.pressure, self.outer_radius,t, self.height, self.material['youngs_modulus'],self.material['poisson_ratio'])
    
        Ixx = geometry.cylindrical_shell_I(self.outer_radius, t)

        #Buckling due to bending moment
        M_buckling = bending.critical_cylinder_bending(self.outer_radius, t, self.pressure, self.material['youngs_modulus'],self.material['poisson_ratio'], Ixx)
     
        #NOTE: Moment magnitude is assumed to be half of the thrust magnitude; If better modelling is available, change of this value is recommneded; 
        while M_buckling / (self.thrust / 2) < FOSY:
            if t>0.02:
                raise ValueError
            t += 0.0005
            Ixx = geometry.cylindrical_shell_I(self.outer_radius, t)
            M_buckling = bending.critical_cylinder_bending(self.outer_radius, t 
            ,self.pressure, self.material['youngs_modulus'],self.material['poisson_ratio'], Ixx)
        return round(t, 4)
    
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
        return self.area*Mi
    
   