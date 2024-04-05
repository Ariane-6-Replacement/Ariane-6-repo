"""
Contains formulas related to axial stress.

"""

import numpy as np

def t_axial(s_yield, R, FOSY, F):
    """
    Calcualtes cylidner thickness required to avoid yielding given an axial force

    :param F: axial load in N
    :param FOSY: yield factor of safety 
    :param s_yiled: material yield strength in Pa
    :param R: radius in m
    :return: Minimal thickness of the vessel in m 
    """
    t = F * FOSY / (s_yield *  2 * R * np.pi) 

    return t
def s_axial(t,R,FOSY,F):
    """
    Calcualtes stress in the cylindrical structure given an axial load, cylinder thickness including required safety marign

    :param F: axial load in N
    :param FOSY: yield factor of safety 
    :param t: thickness in m
    :param R: radius in m
    :return: Maximal stress in Pa
    """
    s = F * FOSY / (2 * R * np.pi * t)
    return s