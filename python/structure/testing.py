"""
Testing file for structure.py."""   

from python.structure.Components.Tank_class import Tank
from python.structure.Components.ITS_class import Shell
from python.structure.Components.CBT_class import CBT
from python.structure.Components.landing_gear_class import LG

class Structure():
    def __init__(self, outer_radius,material, pressure_ox, pressure_fuel, material3, type, volume_ox, mass_ox, volume_fuel, mass_fuel, thrust, engine_mass, engine_number):
        self.outer_radius = outer_radius
        self.pressure1 = pressure_ox
        self.pressure2 = pressure_fuel

        self.material = material
        self.material3 = material3 

        # self.material3 = material3
        self.type = type
        self.thrust = thrust
        print(f'THrust {self.thrust}')
        self.volume1 = volume_ox
        self.volume2 = volume_fuel
        self.mass1 = mass_ox
        self.mass2 = mass_fuel
        self.engine_mass = engine_mass
        self.engine_number = engine_number 
        tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
        tank2 = [self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]


        if type == "separate":
            
            tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
            tank2 =[self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]
            
            if self.mass1 > self.mass2:

                self._tank_fwd = Tank(*tank2)
                self._tank_aft = Tank(*tank1)

            else:

                self._tank_fwd = Tank(*tank1)
                self._tank_aft = Tank(*tank2)
                
            self._ITS_fwd = Shell(self.outer_radius,self.material3,2.5+self._tank_fwd.dome_fwd.height,self.thrust)
            self._ITS_aft = Shell(self.outer_radius,self.material3,1+self._tank_aft.dome_fwd.height+self._tank_fwd.dome_aft.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material3,3+self._tank_aft.dome_aft.height,self.thrust)
        
        
        elif type == 'shared':
            
            #NOTE: 1 - oxidizer, 2 - fuel, possibly add moment 
            self._CBT = CBT(self.outer_radius, self.pressure1, self.material ,self.thrust, self.volume1, self.mass1, self.volume2, self.mass2)
            self._ITS = Shell(self.outer_radius,self.material,2.5+self._CBT._dome_fwd.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material,3+self._CBT._dome_aft.height,self.thrust)
          
    @property
    def mass_engine_structure(self):
        return 3500
    
    @property
    def mass_total(self)-> float:
        if self.type == 'shared':
            return self._CBT.mass + self._EB.mass + self._ITS.mass + self.engine_mass * self.engine_number + self.mass_engine_structure
        else: 
            return self._tank_fwd.mass + self._tank_aft.mass + self._EB.mass + self._ITS_fwd.mass + self._ITS_aft.mass

    @property
    def height_total(self) -> float:
        if self.type == 'shared':
            return self._CBT.height + self._ITS.height +  self._EB.height 
        else:
            return self._tank_fwd.cylinder.height + self._tank_aft.cylinder.height + self._ITS_fwd.height +  self._ITS_aft.height + self._EB.height 


    @property
    def cg(self)->float:
        hengine =(0.6 * self._EB.height - 1.2)
        hthrust = (0.6 * self._EB.height - 0.2)
        hEB = self._EB.height * 0.5 
        if self.type == 'shared':
            ht1 = ( 0.5 * self._CBT._cylinder_aft.height + self._EB.height)
            ht2 = (0.5 * self._CBT._cylinder_fwd.height + self._CBT._cylinder_aft.height + self._EB.height)
            hITS = (0.5 * self._ITS.height + self._CBT._cylinder_fwd.height + self._CBT._cylinder_aft.height + self._EB.height)
            e1 = self._CBT._dome_aft.mass * (self._EB.height - 0.67 * self._CBT._dome_aft.height) + (self._EB.height + self._CBT._cylinder_aft.height - 0.67 * self._CBT._dome_aft.height) * self._CBT._dome_mid.mass  + (self._EB.height + self._CBT._cylinder_aft.height + self._CBT._cylinder_fwd.height+ 0.23 * self._CBT._dome_aft.height) * self._CBT._dome_fwd.mass
            temp = self.engine_mass * self.engine_number * hengine  + self.mass_engine_structure * hthrust   + hEB* self._EB.mass + self._CBT._cylinder_aft.mass * ht1  + self._CBT._cylinder_fwd.mass * ht2*1.08 + self._ITS.mass * hITS + e1
            cg = temp / (self.engine_mass*self.engine_number + self.mass_engine_structure + self.mass_total)
            return cg
        elif self.type == 'separate': 
            ht1 = (0.5 * self._tank_aft._cylinder.height + self._EB.height)
            hITS1 = (0.5 * self._ITS_aft.height + self._tank_aft._cylinder.height + self._EB.height)
            ht2= (0.5 * self._tank_fwd._cylinder.height + self._ITS_aft.height + self._tank_aft._cylinder.height + self._EB.height) 
            hITS2 = ( 0.5 * self._ITS_fwd.height + self._tank_fwd._cylinder.height + self._ITS_aft.height + self._tank_aft._cylinder.height + self._EB.height)
            e1 = self._tank_aft._dome_aft.mass * (self._EB.height - 0.67 * self._tank_aft._dome_aft.height) + (self._EB.height + self._tank_aft.cylinder.height + 0.23 * self._tank_aft._dome_aft.height) * self._tank_aft._dome_fwd.mass  + (self._EB.height + self._tank_aft._cylinder.height + self._ITS_aft.height - 0.67 * self._tank_aft._dome_aft.height) * self._tank_fwd._dome_aft.mass + (self._EB.height + self._tank_aft.cylinder.height + self._ITS_aft.height + self._tank_fwd.cylinder.height + 0.23 * self._tank_aft._dome_aft.height) * self._tank_fwd._dome_fwd.mass 

            temp = self.engine_mass * self.engine_number * hengine + self.mass_engine_structure * hthrust  +  self._EB.mass * hEB  + self._tank_aft.cylinder.mass * ht1* 1.08 + self._ITS_aft.mass * hITS1 +  self._tank_fwd.cylinder.mass * 1.08 * ht2 + self._ITS_fwd.mass * hITS2 + e1

            cg  = temp / (self.engine_mass*self.engine_number + self.mass_engine_structure + self.mass_total)
            return cg
        else:
            raise ValueError
        
            
        
    @property
    def mass_landing_gear(self):
        print(f'Struts {LG(self.outer_radius, self.mass_total, self.cg).LG_geometry}')
        return LG(self.outer_radius, self.mass_total, self.cg).mass_gear
    
    @property
    def mass_total_config(self):
        return self.mass_total + self.mass_landing_gear
    
if __name__ == "__main__":


    #Ariane 5
    #test =Structure(2.7,'2219',3E5,3E5,'2219', 'separate', 120,130E3,390, 25E3,14.1E6,1500,1)

    test =Structure(2.7,'2195',7E5,7E5,'7075', 'shared', 229,262E3,176, 75E3,9E6,1100,9)
    print('DONE')
    print('#####################OUTPUT##############')
    print(f'CG: {test.cg}')
    print('Mass:',test.mass_total)
    print('Height: ', test.height_total)

    # print('#############Engine Bay####################')
    print('EB height:',test._EB.height,'mass: ',test._EB.mass )
    # print(f'ITS {test._ITS.mass}, {test._ITS.height} m')
    # print(f'CBT {test._CBT.mass} aft vol {test._CBT._cylinder_aft.inner_volume} fwd vol {test._CBT._cylinder_fwd.inner_volume}, {test._CBT._dome_mid.inner_volume}')

    
    print(f'cylinder fwd {test._CBT._cylinder_fwd.mass} kg, {test._CBT._cylinder_fwd.height} m')
    print(f'cylinder aft {test._CBT._cylinder_aft.mass} kg, {test._CBT._cylinder_aft.height} m')
    print(f'dome fwd {test._CBT._dome_fwd.mass} kg {test._CBT._dome_fwd.height} m')
    print(f'dome mid {test._CBT._dome_mid.mass}')
    print(f'dome aft {test._CBT._dome_aft.mass}')
    print(f'mass_landing_gear {test.mass_landing_gear}')

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
    print(f'ITS {test._ITS.mass}')
    print(f'CBT {test._CBT.mass} aft vol {test._CBT._cylinder_aft.inner_volume} fwd vol {test._CBT._cylinder_fwd.inner_volume}, {test._CBT._dome_mid.inner_volume}')
    print(f'cylinder fwd {test._CBT._cylinder_fwd.mass} kg, {test._CBT._cylinder_fwd.height} m')
    print(f'cylinder aft {test._CBT._cylinder_aft.mass} kg, {test._CBT._cylinder_aft.height} m')
    print(f'dome fwd {test._CBT._dome_fwd.mass} kg {test._CBT._dome_fwd.height} m')
    print(f'dome mid {test._CBT._dome_mid.mass}')
    print(f'dome aft {test._CBT._dome_aft.mass}')
    print(f'TOTAL MASS: {test.mass_total_config}')