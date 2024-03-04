from Tank_class import Tank
class Structure():
    def __init__(self, outer_radius, pressure1, material1, volume1, fluid1, pressure2, material2,volume2, fluid2, thrust,material3):
        self.outer_radius = outer_radius
        self.pressure1 = pressure1
        self.pressure2 = pressure2
        self.thrust = thrust
        self.material1 = material1
        self.material2 = material2
        self.volume1 = volume1
        self.volume2 = volume2
        self.fluid1 = fluid1 
        self.fluid1 = fluid2 
        self.material3 = material3


        self.input = "struc in"
        self.output = 4

        self._tank1 = Tank(self.outer_radius,self.pressure1,self.material1,self.thrust,self.volume1,self.fluid1)
        self._tank2 = Tank(self.outer_radius,self.pressure2,self.material2,self.thrust,self.volume2,self.fluid2)

    
    @property
    def mass(self)-> float:
        return self._tank1.mass + self._tank2.mass

    @property
    def height(self) -> float:
        return self._cylinder.height + self._dome_fwd.height + self._dome_aft.height
    