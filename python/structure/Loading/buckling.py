"""
Contains formulas related to critical stresses due to buckling as a failure mode.

Source(s): NASA SP-8007
"""

from python.structure.Loading.buckling_coeff import gamma_d
import numpy as np



def _check_moderately_long(gamma: float, l: float, r: float, t: float, v: float) -> bool:
    """
    Checks if a cylinder is moderately long
    :param gamma: Knock-down factor
    :param l: Length
    :param r: Radius
    :param t: Thickness
    :param v: Poisson's ratio
    :return: Boolean True if moderately long, False if not
    """
    # Curvature Parameter
    Z = l ** 2 / (r * t) * np.sqrt(1 - v ** 2)

    # Condition on moderately long tanks
    if (gamma * Z) > np.sqrt(3) * np.pi ** 2 / 6:
        return True
    else:
        return False


def critical_cylinder_buckling(p, r, t, l, E, v):
    """
    Shell buckling formula from NASA SP-8007.
    Sechler formulas from LV manual are less precise.
    :param p: pressure
    :param E: young's modulus
    :param r: radius
    :param t: thickness
    :param v: poisson's ratio
    :param l: length
    :return: Critical Buckling Load (axial force)
    """
    # Number of buckle half waves in the axial direction
    m = 1  # Critical case
    # Number of buckle waves in the circumferential direction
    n = 1  # Critical case

    # Flexural Rigidity
    D = E * t ** 3 / (12 * (1 - v))

    phi = 1 / 16 * np.sqrt(r / t)

    # Knock-down factor
    gamma = 1 - 0.901 * (1 - np.exp(-phi))

    # Curvature Parameter
    Z = l ** 2 / (r * t) * np.sqrt(1 - v ** 2)

    # Buckle aspect ratio
    beta = n * l / (np.pi * r * m)

    # Condition on long tanks
    if _check_moderately_long(gamma, l, r, t, v):

        k_x = 4 * np.sqrt(3) / np.pi ** 2 * gamma * Z

    else:

        k_x = m ** 2 * (1 + beta ** 2) ** 2 + 12 / np.pi ** 4 * (gamma * Z) ** 2 / (m ** 2 * (1 + beta ** 2) ** 2)

    # Checks if it's pressurized
    if p == 0:
        N_cr = k_x * np.pi ** 2 / l ** 2 * D
    else:
        parameter = p / E * (r / t) ** 2
        dgamma = gamma_d(parameter)
        N_cr= 2 * np.pi * E * t ** 2 * (gamma / np.sqrt(3 * (1 - v ** 2)) + dgamma) + p * np.pi * r**2

    return N_cr


