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


"""
Contains functions for the various elastic constants for the cylindrical shell stiffening methods considered in NASA
SP-8007 (2020Rev) section 4.1.2.6.

Source(s): NASA SP-8007
"""

import numpy as np


def isotropic_cylinders_with_rings_and_stringers(E: float, E_s: float, E_r: float,
                                                 A_s: float, A_r: float,
                                                 G_s: float, G_r: float,
                                                 I_s: float, I_r: float,
                                                 J_s: float, J_r: float,
                                                 b_s: float, b_r: float,
                                                 z_s: float, z_r: float,
                                                 v: float, t: float) -> tuple:
    """
    Elastic constants for cylinders stiffened by rings and stringers. Returns:

    E_x: Extensional stiffness of wall in x-direction
    E_y: Extensional stiffness of wall in y-direction
    E_xy: Extensional stiffness of wall in xy-plane
    G_xy: Shear stiffness of orthotropic or sandwich wall in x-y plane
    C_x: Coupling Constant for Orthotropic Cylinders
    C_y: Coupling Constant for Orthotropic Cylinders
    C_xy: Coupling Constant for Orthotropic Cylinders
    K_xy: Coupling Constant for Orthotropic Cylinders
    D_x: Bending stiffness per unit width of wall in x-direction
    D_y: Bending stiffness per unit width of wall in y-direction
    D_xy: Modified twisting stiffness per unit width of wall

    :param E: Young's modulus of the shell
    :param E_s: Young's modulus of the stringers
    :param E_r: Young's modulus of the rings
    :param A_s: Cross-sectional area of the stringers
    :param A_r: Cross-sectional area of the rings
    :param G_s: Shear modulus of the stringers
    :param G_r: Shear modulus of the rings
    :param I_s: Moment of inertia of the stringers
    :param I_r: Moment of inertia of the rings
    :param J_s: Torsion constant of the stringers
    :param J_r: Torsion constant of the rings
    :param b_s: Circumferential stringer stiffener spacing
    :param b_r: Circumferential ring stiffener spacing
    :param z_s: Distance of centroid of stiffeners from reference surface (positive when stiffeners are on outside)
    :param z_r: Distance of centroid of rings from reference surface (positive when rings are on outside)
    :param v: Poisson's ratio
    :param t: Shell thickness
    :return: E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, F_x, F_y, F_xy, H_x, H_y, H_xy, M_x, M_y, M_xy
    """

    E_x = (E * t / (1 - v ** 2)) + (E_s * A_s / b_s)
    E_y = (E * t / (1 - v ** 2)) + (E_r * A_r / b_r)
    E_xy = (v * E * t) / (1 - v ** 2)
    G_xy = E * t / (2 * (1 + v))
    C_x = z_s * (E_s * A_s / b_s)
    C_y = z_r * (E_r * A_r / b_r)
    C_xy = 0
    K_xy = 0
    D_x = E * t ** 3 / (12 * (1 - v ** 2)) + E_s * I_s / b_s + (z_s ** 2) * E_s * A_s / b_s
    D_y = E * t ** 3 / (12 * (1 - v ** 2)) + E_r * I_r / b_r + (z_r ** 2) * E_r * A_r / b_r
    D_xy = v * E * t ** 3 / (6 * (1 - v ** 2)) + E * t ** 3 / (6 * (1 + v)) + G_s * J_s / b_s + G_r * J_r / b_r

    return E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy


def isotropic_isogrid_stiffened_cylinders(E: float,
                                          G: float,
                                          A_s: float,
                                          I_s: float,
                                          J_s: float,
                                          z_s: float,
                                          v: float, t: float, a: float) -> tuple:
    """
    Elastic constants for cylinders stiffened by isogrids. Returns:

    E_x: Extensional stiffness of wall in x-direction
    E_y: Extensional stiffness of wall in y-direction
    E_xy: Extensional stiffness of wall in xy-plane
    G_xy: Shear stiffness of orthotropic or sandwich wall in x-y plane
    C_x: Coupling Constant for Orthotropic Cylinders
    C_y: Coupling Constant for Orthotropic Cylinders
    C_xy: Coupling Constant for Orthotropic Cylinders
    K_xy: Coupling Constant for Orthotropic Cylinders
    D_x: Bending stiffness per unit width of wall in x-direction
    D_y: Bending stiffness per unit width of wall in y-direction
    D_xy: Modified twisting stiffness per unit width of wall

    :param E: Young's modulus
    :param G: Shear modulus of the shell
    :param A_s: Cross-sectional area of the stiffener element
    :param I_s: Moment of inertia of the stiffener element
    :param J_s: Torsion constant of the stiffener element
    :param z_s: Distance of centroid of stiffeners from reference surface (positive when stiffeners are on outside)
    :param v: Poisson's ratio
    :param t: Shell thickness
    :param a: Width of isogrid triangle
    :return: E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, F_x, F_y, F_xy, H_x, H_y, H_xy, M_x, M_y, M_xy
    """

    E_x = E * t / (1 - v ** 2) + (3 * np.sqrt(3) / 4) * (E * A_s / a)
    E_y = E_x
    E_xy = v * E * t / (1 - v ** 2) + (np.sqrt(3) / 4) * (E * A_s / a)
    G_xy = E * t / (2 * (1 + v)) + (np.sqrt(3) / 4) * (E * A_s / a)
    C_x = z_s * 3 * np.sqrt(3) * E * A_s / (4 * a)
    C_y = C_x
    C_xy = z_s * np.sqrt(3) * E * A_s / (4 * a)
    K_xy = C_xy
    D_x = E * t ** 3 / (12 * (1 - v ** 2)) + (3 * np.sqrt(3) / 4) * (E * I_s / a) + (np.sqrt(3) / 4) * (G * J_s / a)
    D_y = D_x
    D_xy = v * E * t ** 3 / (6 * (1 - v ** 2)) + E * t ** 3 / (6 * (1 + v)) + (3 * np.sqrt(3) / 2 * a) * (E * I_s) + \
           (np.sqrt(3) / 2 * a) * (G * J_s)

    return E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy



"""
Contains formulas related to critical stresses due to bending loads.

Source(s): NASA SP-8007
"""

from formulas.nasa_sp_8007.buckling_coeff import gamma_d
from formulas.nasa_sp_8007 import buckling
from databases.fos import *
import numpy as np


def critical_cylinder_bending(p, r, t, E, v):
    """
    Shell bending formula from NASA SP-8007
    :param p: pressure
    :param E: young's modulus
    :param r: radius
    :param t: thickness
    :param v: poisson's ratio
    :param L: length
    :return: Critical Bending Load (collapse load) (moment)
    """

    if not r / t < 1500: raise Exception(f"Shell buckling assumption invalid")
    phi = 1 / 16 * np.sqrt(r / t)

    # Knock-down factor
    gamma = 1 - 0.731 * (1 - np.exp(-phi))

    parameter = p / E * (r / t) ** 2

    dgamma = gamma_d(parameter)

    M_cr = np.pi * r * E * t ** 2 * (gamma / np.sqrt(3 * (1 - v ** 2)) + dgamma) + 0.8 * p * np.pi * r ** 3

    return M_cr / ( Coeff_A_Loads * K_MP * FOSY_b_global )

def critical_stiffened_cylinder_bending(E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, L, r, t, v):
    """
    Stiffened shell bending formula from NASA SP-8007 (2020Rev) section 4.1.2 on orthotropic cylinders.

    Experimental results indicate that the critical maximum load of a stiffened cylinder in bending can exceed the
    critical load in axial compression. However, in the absence of an extensive investigation, it is recommended that
    the critical maximum load of a uniform cylinder with closely spaced stiffeners be taken as equal to the critical
    load in axial compression, calculated from the critical stiffener buckling formula multiplied by a factor
    gamma = 0.75, which is slightly greater than the factor for compression loaded cylinders due to the reduced
    imperfection sensitivity. In addition, as with compression-loaded stiffened cylinders, local skin buckling can also
     occur prior to global buckling, as in the case of widely spaced stiffeners, and should be checked.
    """

    gamma = 0.75
    buckling_load = buckling.critical_stiffened_cylinder_buckling(E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, L, r, t, v)

    return gamma * buckling_load / (Coeff_A_Loads * K_MP * FOSY_b_global)

