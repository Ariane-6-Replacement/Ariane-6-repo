from python.structure.Tank_class import Tank
from python.structure.cylinder_class import Cylinder
from python.structure.ITS_class import Shell
class Structure():
    def __init__(self, outer_radius,material, pressure_ox, pressure_fuel, material3):
        self.outer_radius = outer_radius
        self.pressure1 = pressure_ox
        self.pressure2 = pressure_fuel

        self.material = material
        self.material3 = material3 

        # self.material3 = material3
    def calc(self,  volume_ox, mass_ox,  volume_fuel, mass_fuel, thrust):
        self.thrust = thrust
        self.volume1 = volume_ox
        self.volume2 = volume_fuel
        self.mass1 = mass_ox
        self.mass2 = mass_fuel
        tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
        tank2 =[self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]

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

    def mass_engine_structure(self, engine_number, thrust):
        return 0
    def mass_landing_gear(self, mass_e, mass_p, mass_t, mass_es):
        return 0
    @property
    def mass_total_tank(self)-> float:
        return self._tank_fwd.mass + self._tank_aft.mass + self._EB.mass + self._ITS_fwd.mass + self._ITS_aft.mass

    @property
    def height_total(self) -> float:
        return self._tank_fwd.cylinder.height + self._tank_aft.cylinder.height + self._ITS_fwd.height +  self._ITS_aft.height + self._EB.height 



if __name__ in "__main__":
    test = Structure(2.7,7E5,'2219',328, 440E3, 7E5, 273, 126E3, 20E6,'2195')
    print('DONE')
    print('#####################OUTPUT##############')
    print('Mass:', test.mass_total)
    print('Height: ', test.height_total)
    print('#############TANK FWD####################')
    print('Tank mass:', test._tank_fwd.mass,'height: ',test._tank_fwd.height)
    print('Cylinder mass: ',test._tank_fwd.cylinder.mass,' heigh:',test._tank_fwd.cylinder.height,' thickenss:',test._tank_fwd.cylinder.thickness)
    print('Dome mass aft: ',test._tank_fwd.dome_aft.mass,'heigh: ',test._tank_fwd.dome_aft.height,'thickness: ',test._tank_fwd.dome_aft.thickness)
    print('ITS 1 height:',test._ITS_fwd.height,'mass: ',test._ITS_fwd.mass )
    print('#############TANK AFT####################')
    print('Tank mass:', test._tank_aft.mass,'height: ',test._tank_aft.height)
    print('Cylinder mass: ',test._tank_aft.cylinder.mass,' heigh:',test._tank_aft.cylinder.height,' thickenss:',test._tank_aft.cylinder.thickness)
    print('Dome mass aft: ',test._tank_aft.dome_aft.mass,'heigh: ',test._tank_aft.dome_aft.height,'thickness: ',test._tank_aft.dome_aft.thickness)
    print('ITS 2 height:',test._ITS_aft.height,'mass: ',test._ITS_aft.mass )
    print('#############Engine Bay####################')
    print('EB height:',test._EB.height,'mass: ',test._EB.mass )