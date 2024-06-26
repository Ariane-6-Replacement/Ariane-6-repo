"""
This function finds the axial critical stress for isogrid stiffenned cylinders in bending and axial loading.

Source: "NASA ISOGRID HANDBOOK" by McDonnel Douglas
"""
import numpy as np 

def critical_stress(t,R, E):
    '''
    :param t: plate thickness in m
    :param E: young's modulus in Pa
    :param R: radius in m

    :return: Critical axial stress in Pa, Equivalent thickness in m
    '''
    #NOTE: alpha & Beta are dimensionless parameters for a weight optimized isogrid design
    alpha = 1/3 
    Beta = 16
    v = 1/3
    t_eq = t *Beta /(1+alpha)
    E_eq = E * (1+alpha)**2/Beta
    t_weight = t * (1+3*alpha)
    Ncr = 0.65/np.sqrt(3*(1-v**2)) * E_eq*t_eq**2/R*Beta
    sigma_x = Ncr/t_weight
    
    return sigma_x, t_weight