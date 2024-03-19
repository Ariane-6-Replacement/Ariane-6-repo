"""
Contains formulas related to critical stress due to internal pressure.

Source(s): NASA SP-8007
"""


def t_hoop_stress(s_yield, r, FOSY, p):
    """
    Thickness from hoop stress
    """
    t = p * FOSY * r/ s_yield

    return t