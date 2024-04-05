"""
Contains formulas related to critical stresses due to bending loads.

Source: NASA SP-8007
"""

from python.structure.Loading.buckling_coeff import gamma_d
import numpy as np


def critical_cylinder_bending(r, t ,p, E, v):
    """
    Shell bending formula from NASA SP-8007
    :param p: pressure in Pa
    :param E: young's modulus in Pa
    :param r: radius in m
    :param t: thickness in m
    :param v: poisson's ratio
    :return: Critical Bending Load (collapse load) (moment)
    """
    phi = 1 / 16 * np.sqrt(r / t)

    # Knock-down factor
    gamma = 1 - 0.901 * (1 - np.exp(-phi))

    parameter = p / E * (r / t) ** 2
    dgamma = gamma_d(parameter)

    M_press = np.pi * r * E * t**2 * (gamma / np.sqrt(3 * (1 - v ** 2)) + dgamma) + 0.8 * p * np.pi * r**2
    return M_press

