
class Tank:
    def __init__(self, cylinder, dome_fwd, dome_aft, internal_pressure, fluid_volume) -> None:
        self.cylinder = cylinder
        self.dome_fwd = dome_fwd
        self.dome_aft = dome_aft
        self.fluid_volume = fluid_volume
        self.internal_pressure = internal_pressure
        @property
        def cylinder(self):
            return self._cylidner
        
        @property
        def dome_fwd(self):
            return self._dome_fwd
        
        @property
        def dome_fwd(self):
            return self._dome_aft
        
        @property
        def mass(self)-> float:
            return self.dome_fwd.mass + self.dome_aft.mass + self.cylinder.mass
        @property
        def height(self) -> float:
        # Ignores skirts and welds for now
           return self.cylinder.height + self.dome_fwd.height + self.dome_aft.height
        @property
        def inner_volume(self) -> float:
        # Ignores skirts and welds for now
        return self.dome_fwd.inner_volume + self.cylinder.inner_volume + self.dome_aft.inner_volume

        