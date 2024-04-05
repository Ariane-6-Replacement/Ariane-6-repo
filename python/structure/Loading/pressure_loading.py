"""
Contains formulas related to critical stress due to internal pressure.

Source: NASA SP-8007
"""


def t_hoop_stress(s_yield, r, FOSY, p):
    """
    :param s_yield: yield strength in Pa
    :param r: radius in m
    :param FOSY: yield factor of safety
    :param p: pressure in Pa

    :return: thickness in m
    """
    t = p * FOSY * r/ s_yield

    return t