import geometry
class Cylinder:
    def __init__(self,
                 outer_radius: float,
                 thickness: float,
                 height: float,
                 material: dict,
                 stiffening_elastic_constants: tuple,
                 stiffening_volume: float):
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
        self.thickness = thickness
        self.height = height
        self.material = material
        self.stiffening_elastic_constants = stiffening_elastic_constants
        self.stiffening_volume = stiffening_volume
        self.parent_configuration = None

        if not self.is_thin_walled: raise ValueError(f"Cylinder is not thin walled (OD: {self.outer_diameter}, H: {self.height}), t: {self.thickness})")

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
        return geometry.cylinder_V(self.inner_radius, self.height)

    @property
    def outer_volume(self) -> float:
        return geometry.cylinder_V(self.outer_radius, self.height)

    @property
    def section_Ixx(self) -> float:
        return geometry.cylindrical_shell_I(self.outer_radius, self.thickness)

    @property
    def section_Iyy(self) -> float:
        return self.section_Ixx

    @property
    def mass(self) -> float:
        material_volume = self.outer_volume - self.inner_volume
        return self.material["density"] * material_volume

    @property
    def is_thin_walled(self) -> bool:
        return (self.thickness < 0.1 * self.outer_diameter) and (self.thickness < 0.1 * self.height)

    @property
    def sectional_area(self) -> float:
        return geometry.cylindrical_shell_A(self.outer_radius, self.thickness)
    
    @property
    def stiffening_elastic_constants(self):
        return self._stiffening_elastic_constants

    @stiffening_elastic_constants.setter
    def stiffening_elastic_constants(self, value):
        self._stiffening_elastic_constants = value

    
     @property
    def section_Iyy(self) -> float:
        # TODO: Adjust for stiffeners
        return self.section_Ixx

    @property
    def mass(self) -> float:
        # TODO: Adjust for stiffeners
        material_volume = self.outer_volume - self.inner_volume
        material_volume += self.stiffening_volume
        return self.material["density"] * material_volume

    @property
    def sectional_area(self) -> float:
        # TODO: Adjust for stiffeners
        return geometry.cylindrical_shell_A(self.outer_radius, self.thickness)


