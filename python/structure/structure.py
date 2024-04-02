from python.structure.Components.Tank_class import Tank
from python.structure.Components.ITS_class import Shell
from python.structure.Components.CBT_class import CBT
from python.structure.Components.landing_gear_class import LG

class Structure():
    def __init__(self, outer_radius,material, pressure_ox, pressure_fuel, material3):
        self.outer_radius = outer_radius
        self.pressure1 = pressure_ox
        self.pressure2 = pressure_fuel

        self.material = material
        self.material3 = material3 

        # self.material3 = material3
    def calc(self, type, volume_ox, mass_ox, volume_fuel, mass_fuel, thrust, engine_mass, engine_number):
        self.type = type
        self.thrust = thrust
        self.volume1 = volume_ox
        self.volume2 = volume_fuel
        self.mass1 = mass_ox
        self.mass2 = mass_fuel
        self.engine_mass = engine_mass
        self.engine_number = engine_number 
        tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
        tank2 = [self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]

        # self.input = "struc in"
        # self.output = 4

        if type == "separate":
            
            tank1 = [self.outer_radius,self.pressure1,self.material,self.thrust,self.volume1,self.mass1]
            tank2 =[self.outer_radius,self.pressure2,self.material,self.thrust,self.volume2,self.mass2]
            
            if self.mass1 > self.mass2:

                self._tank_fwd = Tank(*tank2)
                self._tank_aft = Tank(*tank1)

            else:

                self._tank_fwd = Tank(*tank1)
                self._tank_aft = Tank(*tank2)
                
            self._ITS_fwd = Shell(self.outer_radius,self.material3,2+self._tank_fwd.dome_fwd.height,self.thrust)
            self._ITS_aft = Shell(self.outer_radius,self.material3,1+self._tank_aft.dome_fwd.height+self._tank_fwd.dome_aft.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material3,3.0+self._tank_aft.dome_aft.height,self.thrust)
        
        
        elif type == 'shared':
            
            #NOTE: 1 - oxidizer, 2 - fuel, possibly add moment 
            self._CBT = CBT(self.outer_radius, self.pressure1, self.material ,self.thrust, self.volume1, self.mass1, self.volume2, self.mass2)
            self._ITS = Shell(self.outer_radius,self.material,1+self._CBT._dome_fwd.height,self.thrust)
            self._EB = Shell(self.outer_radius,self.material,3.0+self._CBT._dome_aft.height,self.thrust)
          
    @property
    def mass_engine_structure(self):
        return 4000
    
    @property
    def mass_total(self)-> float:
        if self.type == 'shared':
            print(f'CBT {self._CBT._cylinder_aft.height} {self._CBT._cylinder_fwd.height}; Radius: {self.outer_radius}; Mass: {self._CBT.mass_f}  {self._CBT.mass_ox}; Volume {self._CBT.volume_f}, {self._CBT.volume_ox}')
            return self._CBT.mass + self._EB.mass + self._ITS.mass
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
        print(f'height_total {self.height_total}')
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

            temp = self.engine_mass * self.engine_number * hengine + self.mass_engine_structure * hthrust + self._EB.mass * hEB  + self._tank_aft.cylinder.mass * ht1* 1.08 + self._ITS_aft.mass * hITS1 +  self._tank_fwd.cylinder.mass * 1.08 * ht2 + self._ITS_fwd.mass * hITS2 + e1

            cg = temp / (self.engine_mass*self.engine_number + self.mass_engine_structure + self.mass_total)
            return cg
        else:
            raise ValueError
        
    @property
    def mass_landing_gear(self):
        lgmass = LG(self.outer_radius, self.mass_total, self.cg).mass_gear
        print(f"landing gear mass: {lgmass} kg")

        return lgmass
    
# if __name__ == "__main__":
#     print("CALCULATING STRUCTURE")
#     # test = Structure(2.7,7E5,'2219',328, 440E3, 7E5, 273, 126E3, 20E6,'2195')
#     #Ariane 5
#     # test = Structure(2.7,3E5,'2219',120, 130E3, 3E5, 390, 25E3, 20E6,'2219')
#     t = Structure(2.7,'2219',3E5,3E5,'2219')
#     test =Structure.calc(t, 'shared', 120,130E3,390, 25E3,14.1E6,1500,1)
#     print('DONE')
#     print('#####################OUTPUT##############')
#     print('Mass:',test)
#     print('Height: ', test.height_total)
#     print('#############TANK FWD####################')
#     print('Tank mass:', test._tank_fwd.mass,'height: ',test._tank_fwd.height)
#     print('Cylinder mass: ',test._tank_fwd.cylinder.mass,' heigh:',test._tank_fwd.cylinder.height,' thickenss:',test._tank_fwd.cylinder.thickness)
#     print('Dome mass aft: ',test._tank_fwd.dome_aft.mass,'heigh: ',test._tank_fwd.dome_aft.height,'thickness: ',test._tank_fwd.dome_aft.thickness)
#     print('ITS 1 height:',test._ITS_fwd.height,'mass: ',test._ITS_fwd.mass )
#     print('#############TANK AFT####################')
#     print('Tank mass:', test._tank_aft.mass,'height: ',test._tank_aft.height)
#     print('Cylinder mass: ',test._tank_aft.cylinder.mass,' heigh:',test._tank_aft.cylinder.height,' thickenss:',test._tank_aft.cylinder.thickness)
#     print('Dome mass aft: ',test._tank_aft.dome_aft.mass,'heigh: ',test._tank_aft.dome_aft.height,'thickness: ',test._tank_aft.dome_aft.thickness)
#     print('ITS 2 height:',test._ITS_aft.height,'mass: ',test._ITS_aft.mass )
#     print('#############Engine Bay####################')
#     print('EB height:',test._EB.height,'mass: ',test._EB.mass )