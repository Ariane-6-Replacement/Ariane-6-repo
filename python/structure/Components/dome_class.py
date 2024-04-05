import python.structure.geometry as geometry
import python.structure.Loading.ellipse_stress as es
import numpy as np

class Dome:
    def __init__(self,
                 outer_radius: float,
                 pressure: float,
                 material: dict):
        """
        Dome object, containing all relevant parameters. 

        :param outer_radius: in m
        :param pressureL in Pa
        :param material: dictionary object from materials database (databases/materials.py)
       
        """

        self.outer_radius = outer_radius
        self.pressure = pressure
        self.material = material


    
    @property
    def height(self) -> float:
            #Critical ratio for the lowest dome height from Analysis of Stress at Several Junctions in Pressiurzed Shells, Johns et al., 1963;
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



        
            