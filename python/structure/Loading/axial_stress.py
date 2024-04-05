import numpy as np

def t_axial(s_yield, R, FOSY, F):
    """
    Calcualtes cylidner thickness required to avoid yielding given an axial force

    F - Axial load in N
    FOSY - yield factor of safety 
    s_yiled - material yield strength in Pa
    R - radius in m
    """
    t = F * FOSY / (s_yield *  2 * R * np.pi) 

    return t
def s_axial(t,R,FOSY,F):
    """
    Calcualtes stress in the cylindrical structure given an axial load, cylinder thickness including required safety marign

    F - Axial load in N
    FOSY - yield factor of safety 
    t - cylinder thickness
    R - radius in m
    """
    s = F * FOSY / (2 * R * np.pi * t)
    return s