import pandas as pd

class Trajectory():
    def __init__(self):
        data = [['Standard Geostationary Transfer Orbit', 'GTO', 6, 250, 35786, 178, 11500],
                ['Geostationary Transfer Orbit + (GTO+) and Medium Transfer Orbit (MTO)', 'GTO+ MTO', 6, 2200, 35486, 'none', 10700],
                ['Sub Geostationary Transfer Orbits', 'sGTO', 6, 250, 22500, 'none', 12950],
                ['High Earth Orbit', 'HEO', 6, 180, 1500000, 'none', 8000],
                ['ISS Servicing', 'ISS', 51.6, 250, 250, 'none', 20000],
                ['Lunar Transfer Orbit', 'LTO', 7, 230, 400000, 'none', 8600],
                ['Sun-Synchronous Orbit', 'SSO', 97.4, 500, 500, 'none', 15500],
                ['Polar Orbit', 'POL', 90, 900, 900, 'none', 15400],
                ['Low Earth Orbit', 'LEO', 6, 250, 1200, 21650]]
        orbits_list = pd.DataFrame(data, columns=['name', 'abbreviation', 'inclination [deg]', 'altitude of perigee [km]', ' altitude of apogee [km]', 'argument of perigee [deg]', 'payload weight [kg]'])
