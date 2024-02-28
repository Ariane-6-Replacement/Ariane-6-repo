

class FirstStageRequirements:
    def __init__(self):

        Thrust = 19.97e6    # Newton ; Derived from A64 (wiki); =Fz
        Fx = 10000   #TBR
        Fy = 10000   #TBR
        Mx,My,Mz = 0,0,0

        time_burn_1st = 100 # seconds, just a guess


class Prometheus:
    def __init__(self):
        Isp = 360
        Thrust_default = 980e3
        cost = 1e6


class Fuel_specs:
    def __init__(self):
        
        rho_LOX = 1340 #kg/m3 liquid oxygen
        # rho_RP1 = 860  #kg/m3 RP1 (kerosen)
        rho_LM = 460  #kg/m3 liquid methane  # should be checked , at which temperature?
        mix_rat = 3.8 # kg lox per kg meth


        #Raptor Mixture Ratio: 3.8 kg LOX to 1kg Methane. [Source](https://en.wikipedia.org/wiki/Raptor_(rocket_engine)).



