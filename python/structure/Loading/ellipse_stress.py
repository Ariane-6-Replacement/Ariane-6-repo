"""
This function calcualtes the maximal thickness due to internal pressure in an elliptical endcap. Discontinuity effects and external loading cases are not considered.

Source: "LAUNCH VEHICLE STRUCTURAL MASS PREDICTION MODEL" by W.A.R. Wildvank
"""

from math import sin, cos
from python.structure.constants import FOSU
import numpy as np


def t_ellipsoid(r, h , p , s_yield):
    '''
    :param r: radius in m
    :param h: height in m
    :param p: pressure in m
    :param s_yield: yield strength in Pa
    :return: Maximal endcap thickness [m]
    """ 
    '''
    #a - radius & b -height
    R1 = np.sqrt( r**4 * (h)**2+ h**4* (r)**2 ) / h**2
    R2 = (r**4 * (h)**2 + h**4 * (r)**2)**(3/2) / (r**4 * h**4)
    A = R1/2
    B = R1 * (1-R1/(2*R2))
    t = p * FOSU / s_yield * np.sqrt(A**2 - A * B + B**2)
    return round(t,4)
