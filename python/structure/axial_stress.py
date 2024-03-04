import numpy as np

def t_axial(s_yield, R, FOSY, F):
    """
    Thickness from the axial force
    """
    t = F * FOSY / (s_yield *  2 * R * np.pi)

    return t
def s_axial(t,R,FOSY,F):
    """
    Stress from the axial force
    """
    s = F*FOSY / (2* R * np.pi * t)
    return s