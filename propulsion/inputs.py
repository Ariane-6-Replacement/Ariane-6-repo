from typing import Any


class FirstStageRequirements:
    def __init__(self):

        self.Thrust = 19.97e6    # Newton ; Derived from A64 (wiki); =Fz
        self.Fx = 10000   #TBR
        self.Fy = 10000   #TBR
        self.Mx, self.My, self.Mz = 0,0,0

        self.time_burn_1st = 100 # seconds, just a guess


class Prometheus:
    def __init__(self):
        self.Isp = 360
        self.Thrust_default = 980e3
        self.cost = 1e6
        self.OF_ratio = 3.5 #chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.eucass.eu/doi/EUCASS2017-537.pdf
        # self.OF_ratio = 1.7 # wrong? https://aris-space.ch/introduction-to-prometheus/


class Vinci:
    def __init__(self):
        pass


class Fuel:
    def __init__(self):
        self.rho_LOX = 1340 #kg/m3 liquid oxygen
        self.rho_RP1 = 860  #kg/m3 RP1 (kerosen)
        self.rho_LM = 460  #kg/m3 liquid methane  # should be checked , at which temperature?


        #Raptor Mixture Ratio: 3.8 kg LOX to 1kg Methane. [Source](https://en.wikipedia.org/wiki/Raptor_(rocket_engine)).



