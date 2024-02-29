"""
Contains formulas related to critical stress due to internal pressure.

Source(s): NASA SP-8007
"""

from formulas.nasa_sp_8007.buckling_coeff import gamma_d
from databases.fos import Coeff_A_Pressure, Coeff_B

def hoop_stress(p, r, t):
    """
    Hoop stress formula 
    :param p: pressure
    :param r: radius
    :param t: thickness
    """
    p  = Coeff_A_Pressure * Coeff_B * p
    sigma_1 = p * r / t 
    # sigma_2 = p * r/ (2 * t)
    #Changed on 13.06 18:18
    # sigma_eq = (sigma_1**2 - sigma_1 * sigma_2 + sigma_2**2)**1/2
    return sigma_1