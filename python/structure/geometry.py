"""
Contains formulas for general geometric calculations.

Source(s): my mind, my brain, my heart, my soul, my body, my blood, my sweat, my tears, my life, my death, my everything
"""

import numpy as np
from numpy.polynomial.polynomial import Polynomial
from scipy.integrate import trapz


# CUBOID #############################################################

def rectangle_I(width: float, height: float) -> float:
    """
    Calculates the area moment of inertia of a rectangular section.
    :param width: width of the rectangle
    :param height: height of the rectangle
    :return: moment of inertia of the rectangular section
    """
    return (width * (height ** 3)) / 12


def rectangle_J(width: float, height: float) -> float:
    """
    Calculates the torsional constant of a rectangle.
    :param width: width of the rectangle
    :param height: height of the rectangle
    :return: torsion constant of the rectangular section
    """
    a = max(width, height)  # Long side
    b = min(width, height)  # Short side

    A = a * (b ** 3)
    B = 1 - (b ** 4) / (12 * (a ** 4))
    C = 0.21 * (b / a)

    J = A * ((1 / 3) - C * B)
    return J


# CYLINDER ###########################################################

def cylindrical_shell_I(radius: float, thickness: float) -> float:
    """
    Calculates the moment of inertia of a cylindrical shell.
    :param radius: outer radius of the cylindrical shell
    :param thickness: thickness of the cylindrical shell
    :return: moment of inertia of the cylindrical shell
    """
    return (1 / 4) * np.pi * (radius ** 4) - (1 / 4) * np.pi * ((radius - thickness) ** 4)


def cylindrical_shell_A(radius: float, thickness: float) -> float:
    """
    Calculates the sectional area of a cylindrical shell.
    :param radius:outer radius of the cylindrical shell
    :param thickness: thickness of the cylindrical shell
    :return: sectional area of the cylindrical shell
    """
    return np.pi * (radius ** 2) - np.pi * ((radius - thickness) ** 2)


def cylinder_V(radius: float, height: float) -> float:
    """
    Calculates the volume of a cylinder.
    :param radius: outer radius of the cylinder
    :param height: height of the cylinder
    :return: cylinder volume
    """
    return np.pi * (radius ** 2) * height


def cylinder_h(volume: float, radius: float) -> float:
    """
    Calculates the height of a cylinder.
    :param volume: volume of the cylinder
    :param radius: outer radius of the cylinder
    :return: height of the cylinder
    """
    return volume / (np.pi * (radius ** 2))


def cylinder_r(volume: float, height: float) -> float:
    """
    Calculates the radius of a cylinder.
    :param volume: volume of the cylinder
    :param height: height of the cylinder
    :return: radius of the cylinder
    """
    return np.sqrt(volume / (np.pi * height))



# SEMI-ELLIPSOID ####################################################

def semi_ellipsoid_V(radius: float, height: float) -> float:
    """
    Calculates the volume of an elliptical dome. Assumes semimajor axis = semiminor axis = radius.
    :param radius: radius of the elliptical dome
    :param height: height of the elliptical dome
    :return: volume of the elliptical dome
    """

    return ((4 / 3) * np.pi * radius ** 2 * height) / 2


def semi_ellipsoid_h(volume: float, radius: float) -> float:
    """
    Calculates the height of an elliptical dome. Assumes semimajor axis = semiminor axis = radius.
    :param volume: volume of the elliptical dome
    :param radius: radius of the elliptical dome
    :return: height of the elliptical dome
    """

    return (2 * volume) / ((4 / 3) * np.pi * radius ** 2)
