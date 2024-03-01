import pandas as pd

class Trajectory():
    def __init__(self):
        data = [['Standard Geostationary Transfer Orbit', 'GTO', 6, 250, 35786, 178, 11500],
                ['Geostationary Transfer Orbit + (GTO+) and Medium Transfer Orbit (MTO)', 'GTO+ MTO', 6, 2200, 35486, 'none', 10700],
                ['Sub Geostationary Transfer Orbits', 'sGTO', 6, 250, 22500, 'none', 12950],
                [],
                [],
                [],
                [],
                [],
                [],
                []]
        orbits_list = pd.DataFrame(data, columns=['name', 'abbreviation', 'inclination [deg]', 'altitude of perigee [km]', ' altitude of apogee [km]', 'argument of perigee [deg]', 'payload weight [kg]'])
