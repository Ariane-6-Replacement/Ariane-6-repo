from .Tank_class import Tank
from cylinder_class import Cylinder
from ITS_class import Shell
class Structure():
    def __init__(self, outer_radius, pressure1, material, volume1, mass1, pressure2,volume2, mass2, thrust, material3
                 ):
        self.outer_radius = outer_radius
        self.pressure1 = pressure1
        self.pressure2 = pressure2
        self.thrust = thrust
        self.material = material
        self.material3 = material3 
        self.volume1 = volume1
        self.volume2 = volume2
        self.mass1 = mass1
        self.mass2 = mass2
        # self.material3 = material3
        tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.fluid1]
        tank2 =[self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.fluid2]
        
        self.input = "struc in"
        self.output = 4
        if mass1 > mass2:
            self._tank_fwd = Tank(*tank2)
            self._tank_aft = Tank(*tank1)
        else:
            self._tank_fwd = Tank(*tank1)
            self._tank_aft = Tank(*tank2)
            
        # self._ITS_fwd = Cylinder(self.outer_radius,self.material3,0,self.trust*1.2,1)
        # self._ITS_aft = Cylinder(self.outer_radius,self.material3,0,self.trust*2,1.5)
        self._ITS_fwd = Shell(self.outer_radius,self.material3,0.5+self._tank_fwd.dome_fwd.height)
        self._ITS_aft = Shell(self.outer_radius,self.material3,0.5+self._tank_aft.dome_fwd.height+self._tank_fwd.dome_aft.height)
        self._EB = Shell(self.outer_radius,self.material3,2+self._tank_aft.dome_aft.height)

    
    @property
    def mass(self)-> float:
        return self._tank_fwd.mass + self._tank_aft.mass + self._EB.mass + self._ITS_fwd.mass + self._ITS_aft.mass

    @property
    def height(self) -> float:
        return self._tank_fwd.cylinder.height + self._tank_aft.cylinder.height + self._ITS_fwd.height +  self._ITS_aft.height + self._EB.height 
    