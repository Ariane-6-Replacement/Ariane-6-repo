import python.structure.geometry as geometry
import python.structure.Loading.ellipse_stress as es
import numpy as np

class Dome:
    def __init__(self,
                 outer_radius: float,
                 pressure: float,
                 material: dict):
        """
        Dome object, containing all relevant parameters. Dome coordinate system is defined with the origin at the center,
        in the plane of the connection with the cylinder. The z_d axis moves along the dome's axis in the direction of
        decreasing radius. Hence, for the aft dome, the coordinate system points in the direction opposite to the
        global coordinate system for the tank configuration.

        :param outer_radius: in m
        :param material: dictionary object from materials database (databases/materials.py)
       
        """

        self.outer_radius = outer_radius
        self.pressure = pressure
        self.material = material
        self.parent_configuration = None

        
        # if self.height / self.outer_radius > 0.707 and self.type_ == "semi-ellipsoidal": raise ValueError(
        #     f"Semi ellipsoidal ratio exceeds critical value ({self.height / self.outer_radius} > 0.707).")
    
    @property
    def height(self) -> float:
            #Critical ratio for the lowest dome height
            return self.outer_radius * 0.707
   
    @property
    def thickness(self) -> float:
         t=  es.t_ellipsoid(self.outer_radius, self.height, self.pressure, self.material['yield_stress'])
         return round(t, 4)
         
    @property
    def inner_radius(self) -> float:
        return self.outer_radius - self.thickness

    @property
    def inner_diameter(self) -> float:
        return 2 * self.inner_radius

    @property
    def outer_diameter(self) -> float:
        return 2 * self.outer_radius


    @property
    def inner_volume(self) -> float:
            return geometry.semi_ellipsoid_V(self.inner_radius, self.height)
       

    @property
    def outer_volume(self) -> float:
        return geometry.semi_ellipsoid_V(self.outer_radius, self.height)
        
    @property
    def mass(self) -> float:
        material_volume = self.outer_volume - self.inner_volume
        return material_volume * self.material["density"]


    # def z_d_to_section_radius(self, z_d: float) -> float:
    #     """
    # `   Finds the sectional radius of the dome section at a given height, using the local dome coordinate system (z_d).
    #     :param z_d: in m
    #     :return: radius in m
    #     """
  
    #     return self.outer_radius * np.sqrt(1 - (z_d / self.height) ** 2)
      

    # def stress_state(self, z_d: float, loads: dict) -> tuple:
    #     """
    #     Finds the stress state of the dome at a given height, using the local dome coordinate system (z_d).
    #     :param z_d: in m
    #     :return: (sigma_meridional, sigma_circumferential)
    #     """
    #     # Hydrostatic pressure for aft dome
    #     if self.parent_configuration.aft_dome == self:
    #         hydrostatic_pressure = pressure.find_hydrostatic_pressure(rho=self.parent_configuration.fluid["density"],
    #                                                                   h=self.parent_configuration.height,
    #                                                                   a=loads["a_axial"])
    #     else:
    #         hydrostatic_pressure = 0

    #         local_radius = self.z_d_to_section_radius(z_d=z_d)
    #         phi = np.arctan(local_radius / z_d)
    #         s_mer_press, s_circ_press = ellipse_stress.stress_position(
    #             effective_internal_pressure=self.parent_configuration.internal_pressure + hydrostatic_pressure,
    #             phi=phi,
    #             major_axis=(self.inner_radius + self.outer_radius) / 2,
    #             minor_axis=self.height,
    #             thickness=self.thickness)
    #         return s_mer_press, s_circ_press

        
            