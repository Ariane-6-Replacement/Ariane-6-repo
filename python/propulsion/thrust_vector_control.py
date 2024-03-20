from python.propulsion.inputs import Prometheus, FirstStageRequirements

class TVC:
    def __init__(self):
        engine = Prometheus()
        req = FirstStageRequirements()
        self.possible_engines = req.booster_area/engine.area_truss_structure * 0.66

TVC1 = TVC()
print(TVC1.possible_engines)