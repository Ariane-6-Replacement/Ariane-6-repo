from python.structure.Components.Tank_class import Tank
from python.structure.Components.ITS_class import Shell
from python.structure.Components.CBT_class import CBT

class Structure():
    def __init__(self,type, outer_radius, pressure1, material, volume1, mass1, pressure2,volume2, mass2, thrust, material3):
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
            
            if mass1 > mass2:

                self._tank_fwd = Tank(*tank2)
                self._tank_aft = Tank(*tank1)

            else:

                self._tank_fwd = Tank(*tank1)
                self._tank_aft = Tank(*tank2)
                
            self._ITS_fwd = Shell(self.outer_radius,self.material3,1+self._tank_fwd.dome_fwd.height,self.thrust)
            self._ITS_aft = Shell(self.outer_radius,self.material3,0.5+self._tank_aft.dome_fwd.height+self._tank_fwd.dome_aft.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material3,2+self._tank_aft.dome_aft.height,self.thrust)
        
        
        elif type == 'CBT':
            
            #NOTE: 1 - oxidizer, 2 - fuel, possibly add moment 
            self._CBT = CBT(self.outer_radius, self.pressure1, self.material ,self.thrust, self.volume1, self.mass1, self.volume2, self.mass2)
            self._ITS = Shell(self.outer_radius,self.material,1+self._CBT._dome_fwd.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material,2+self._CBT._dome_aft.height,self.thrust)
          



          

    def mass_engine_structure(self, engine_number, thrust):
        return 0
    
    def mass_landing_gear(self, mass_e, mass_p, mass_t, mass_es):
        return 0
    
    @property
    def mass_total(self)-> float:
        if self.type == 'CBT':
            return self._CBT.mass + self._EB.mass + self._ITS.mass 
        else: 
            return self._tank_fwd.mass + self._tank_aft.mass + self._EB.mass + self._ITS_fwd.mass + self._ITS_aft.mass

    @property
    def height_total(self) -> float:
        if self.type == 'CBT':
            return self._CBT.height + self._ITS_fwd.height +  self._EB.height 
        else:
            return self._tank_fwd.cylinder.height + self._tank_aft.cylinder.height + self._ITS_fwd.height +  self._ITS_aft.height + self._EB.height 



# if __name__ == "__main__":
#     test = Structure('DUAL',2.7,7E5,'2195',328, 440E3, 7E5, 273, 126E3, 11E6,'2195')
# #     print('DONE')
#     print(f'Tank  {test.mass_total}' )
# print(f'Tank :{test._CBT._cylinder_fwd.outer_volume} {test._CBT._cylinder_fwd.inner_volume} {test._CBT._cylinder_fwd.thickness} {test._CBT._cylinder_fwd.mass} {test._CBT._cylinder_fwd.height}' )

# print(f'Tank :{test._CBT._cylinder_aft.outer_volume} {test._CBT._cylinder_aft.mass} {test._CBT._cylinder_aft.height} {test._CBT._cylinder_aft.inner_volume} {test._CBT._dome_mid.outer_volume} {test._CBT._dome_aft.inner_volume}' )
 
    
# Tank :0.0046 3518.7390620764063 15.043 343.3450386984726 29.145353011886524 29.01811619470952

    # print(f'Else :{test._EB.mass} {test._ITS_fwd.mass} {test._ITS_aft.mass}' )
    # print(f'Tank :{test._tank_fwd.mass} {test._tank_aft.mass} ' )
    # print(f'Tank1 :{test._tank_fwd.cylinder.mass}  {test._tank_fwd.dome_fwd.mass} {test._tank_fwd.dome_aft.mass} {test._tank_fwd.cylinder.height}' )
    # print(f'Tank2 :{test._tank_aft.cylinder.mass}  {test._tank_aft.dome_fwd.mass} {test._tank_aft.dome_aft.mass} {test._tank_aft.cylinder.height}' )

# Else :795.7551147303908 592.1799107777722 878.9970156266165
# Tank :3410.302048324749 4197.676317352785
# Tank1 :2334.208409257485  271.8117211038802 304.14207349534547 9.979
# Tank2 :2924.3685271606523  271.8117211038802 381.7104515310099 12.502





    # print(f'Mass fwd:{test._tank_fwd.height}, mass aft {test._tank_aft.height}')
    # print('Mass: ', test._ITS_fwd.mass)
    # print('Mass: ', test._)
    # # Output for dual mass 
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