import json
import numpy as np
import os

""""
This file allows you to get the density for 
methane: 95-111K with steps of 2K and 0.1-1.5MPa with steps of 0.1
lox: 80-90K with steps of 2K and 0.1-1.5MPa with steps of of 0.1
"""

def read_json_file(input_file_path):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, input_file_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_keys_from_json(data):
    if isinstance(data, dict):
        return list(data.keys())
    else:
        return None

def round_to_closest_key(number, keys):
    closest_key = min(keys, key=lambda x: abs(float(x) - number))
    return closest_key

def get_density(filename, temperature, pressure, molar_mass):
    data = read_json_file(filename)
    keys = get_keys_from_json(data)
    temperature = round_to_closest_key(temperature,keys)
    pressure = pressure/1e6
    pressure = round_to_closest_key(pressure,[round(num, 2) for num in list(float(x) / 10 for x in range(1, 16))])

    for entry in data[temperature]:
        if entry.get('Pressure (MPa)') == pressure:
            density = entry.get('Density (mol/l)') * molar_mass
            return density



if __name__ == "__main__":
    print(get_density("NIST_methane_densities.json",105.5,500e5,16.04)) # kg/m3
    print(get_density("NIST_LOX_densities.json",80.5,500e5,31.999)) # kg/m3

