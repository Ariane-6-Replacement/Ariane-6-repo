"""
This function finds the meridional/longitudinal and circumferential/hoop stress due to internal pressure in an elliptical endcap. Discontinuity effects and external loading cases are not considered.

Source: "Stresses in Shells" by Flugge
"""

from math import sin, cos
from constants import FOSY
import numpy as np


# def stress_position(effective_internal_pressure: float, phi: float, major_axis: float, minor_axis: float,
#                     thickness: float) -> tuple:
#     """
#     Finds stress state in a two-dimensional model; it is recommended for a/b to stay under 1.42 to avoid compressive stresses

#     :param effective_internal_pressure: effective internal pressure in the dome (basic pressure + hydrostatic pressure) in Pa
#     :param phi: angle with respect to vertical axis (in this case, parallel to the length of the cylinder), runs from 0 at vertex to pi/2 at joint with cylinder in m
#     :param major_axis: major axis of the ellipse, in this case equal to the radius (probably internal, but no practical difference from median) in m
#     :param minor_axis: minor axis of the ellipse, in this case equal to the height of the semi-ellipse (again, probably internal, but no practical difference from median) in m
#     :param thickness: cylinder thickness in m
#     :return: stress state as a function of position in the cylinder (meridional, circumferential)
#     """
#     effective_internal_pressure = Coeff_A_Pressure * effective_internal_pressure * Coeff_B

#     meridional_stress = effective_internal_pressure * major_axis ** 2 / (2 * thickness) * 1 / (
#             (major_axis ** 2) * (sin(phi)) ** 2 + (minor_axis ** 2) * (cos(phi)) ** 2) ** (1 / 2)

#     circumferential_stress = effective_internal_pressure * major_axis ** 2 / (2 * thickness * minor_axis ** 2) * (
#             minor_axis ** 2 - (major_axis ** 2 - minor_axis ** 2) * (sin(phi)) ** 2) / (
#                                      (major_axis ** 2) * (sin(phi)) ** 2 + (minor_axis ** 2) * (cos(phi)) ** 2) ** (
#                                      1 / 2)

#     return meridional_stress, circumferential_stress

def t_ellipsoid(r, h , p , s_yield):
    '''
    Assumes constant thickness for the top of the endcap 
    '''
    #a - radius & b -height
    R1 = np.sqrt( r**4 * (h)**2+ h**4* (r)**2 ) / h**2
    R2 = (r**4 * (h)**2 + h**4 * (r)**2)**(3/2) / (r**4 * h**4)
    A = R1/2
    B = R1 * (1-R1/(2*R2))
    t = p * FOSY/ s_yield * np.sqrt(A**2 - A * B + B**2)
    return round(t,4)
