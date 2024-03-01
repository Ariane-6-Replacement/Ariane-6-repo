import numpy as np
def t_axial(s_yield, r, FOSY, F):
    """
    Thickness from the axial force
    """
    t = F * FOSY */ (s_yield *  2 * r * np.pi)

    return t