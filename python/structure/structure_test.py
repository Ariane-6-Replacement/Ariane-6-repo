from Tank_class import Tank
from cylinder_class import Cylinder
from ITS_class import Shell
from CBT_class import CBT
class Structure():
    def __init__(self,type, outer_radius, pressure1, material, volume1, mass1, pressure2,volume2, mass2, thrust, material3
                 ):
        self.type = type 
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

        if type == "DUAL":
            tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
            tank2 =[self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]
            
            # self.input = "struc in"
            # self.output = 4
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
        
        
        elif type == 'CBT':
            #NOTE: 1 - oxidizer, 2 - fuel, possibly add moment 
            self._CBT = CBT(outer_radius, pressure1, material ,thrust, volume1, mass1, volume2, mass2)



          

    def mass_engine_structure(self, engine_number, thrust):
        return 0
    def mass_landing_gear(self, mass_e, mass_p, mass_t, mass_es):
        return 0
    @property
    def mass_total(self)-> float:
        if self.type == 'CBT':
            return self._CBT.mass + self._EB.mass + self._ITS_fwd.mass 
        else: 
            return self._tank_fwd.mass + self._tank_aft.mass + self._EB.mass + self._ITS_fwd.mass + self._ITS_aft.mass

    @property
    def height_total(self) -> float:
        if self.type == 'CBT':
            return self._CBT.height + self._ITS_fwd.height +  self._EB.height 
        else:
            return self._tank_fwd.cylinder.height + self._tank_aft.cylinder.height + self._ITS_fwd.height +  self._ITS_aft.height + self._EB.height 



if __name__ in "__main__":
    test = Structure('CBT',2.7,7E5,'2219',328, 440E3, 7E5, 273, 126E3, 20E6,'2195')
    print('DONE')
    print('Mass: ', test.mass_total)
    #Output for dual mass 
    # print('#####################OUTPUT##############')
    # print('Mass:', test.mass_total)
    # print('Height: ', test.height_total)
    # print('#############TANK FWD####################')
    # print('Tank mass:', test._tank_fwd.mass,'height: ',test._tank_fwd.height)
    # print('Cylinder mass: ',test._tank_fwd.cylinder.mass,' heigh:',test._tank_fwd.cylinder.height,' thickenss:',test._tank_fwd.cylinder.thickness)
    # print('Dome mass aft: ',test._tank_fwd.dome_aft.mass,'heigh: ',test._tank_fwd.dome_aft.height,'thickness: ',test._tank_fwd.dome_aft.thickness)
    # print('ITS 1 height:',test._ITS_fwd.height,'mass: ',test._ITS_fwd.mass )
    # print('#############TANK AFT####################')
    # print('Tank mass:', test._tank_aft.mass,'height: ',test._tank_aft.height)
    # print('Cylinder mass: ',test._tank_aft.cylinder.mass,' heigh:',test._tank_aft.cylinder.height,' thickenss:',test._tank_aft.cylinder.thickness)
    # print('Dome mass aft: ',test._tank_aft.dome_aft.mass,'heigh: ',test._tank_aft.dome_aft.height,'thickness: ',test._tank_aft.dome_aft.thickness)
    # print('ITS 2 height:',test._ITS_aft.height,'mass: ',test._ITS_aft.mass )
    # print('#############Engine Bay####################')
    # print('EB height:',test._EB.height,'mass: ',test._EB.mass )