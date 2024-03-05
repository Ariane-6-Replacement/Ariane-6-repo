"""
Contains formulas related to critical stresses due to buckling as a failure mode.

Source(s): NASA SP-8007
"""

from buckling_coeff import gamma_d
import numpy as np
import pandas as pd


def _check_moderately_long(gamma: float, l: float, r: float, t: float, v: float) -> bool:
    """
    Checks if a cylinder is moderately long
    :param gamma: Knock-down factor
    :param l: Length
    :param r: Radius
    :param t: Thickness
    :param v: Poisson's ratio
    :return: Boolean True if moderately long, False if not
    """
    # Curvature Parameter
    Z = l ** 2 / (r * t) * np.sqrt(1 - v ** 2)

    # Condition on moderately long tanks
    if (gamma * Z) > np.sqrt(3) * np.pi ** 2 / 6:
        return True
    else:
        return False


def critical_cylinder_buckling(p, r, t, l, E, v):
    """
    Shell buckling formula from NASA SP-8007.
    Sechler formulas from LV manual are less precise.
    :param p: pressure
    :param E: young's modulus
    :param r: radius
    :param t: thickness
    :param v: poisson's ratio
    :param L: length
    :return: Critical Buckling Load (axial force)
    """
    # Number of buckle half waves in the axial direction
    m = 1  # Critical case (I think)
    # Number of buckle waves in the circumferential direction
    n = 1  # Critical case

    # Flexural Rigidity, make this a function
    D = E * t ** 3 / (12 * (1 - v))

    phi = 1 / 16 * np.sqrt(r / t)

    # Knock-down factor
    gamma = 1 - 0.901 * (1 - np.exp(-phi))

    # Curvature Parameter
    Z = l ** 2 / (r * t) * np.sqrt(1 - v ** 2)

    # Buckle aspect ratio
    beta = n * l / (np.pi * r * m)

    # Condition on long tanks
    if _check_moderately_long(gamma, l, r, t, v):

        k_x = 4 * np.sqrt(3) / np.pi ** 2 * gamma * Z

    else:

        k_x = m ** 2 * (1 + beta ** 2) ** 2 + 12 / np.pi ** 4 * (gamma * Z) ** 2 / (m ** 2 * (1 + beta ** 2) ** 2)

    # Checks if it's pressurized
    if p == 0:
        N_cr = k_x * np.pi ** 2 / l ** 2 * D
    else:
        parameter = p / E * (r / t) ** 2
        dgamma = gamma_d(parameter)
        N_cr = 2 * np.pi * E * t ** 2 * (gamma / np.sqrt(3 * (1 - v ** 2)) + dgamma) + p * np.pi * r**2

    return N_cr/t


def critical_stiffened_cylinder_buckling(E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, L, r, t, v):
    """
    Stiffened shell buckling formula from NASA SP-8007 (2020Rev) section 4.1.2 on orthotropic cylinders.

    Pre-buckling deformations are not considered in the derivation of this equation. Cylinder edges are assumed to
    be simply supported. These conditions are assumed to be representative of rings that are rigid in their own plane
    but offer no resistance to rotation or bending out of their plane. NOT APPLICABLE TO RING-STIFFENED CORRUGATED
    CYLINDERS.

    Calculations neglecting stiffener eccentricity yield unconservative values of the buckling load of internally
    stiffened cylinders and conservative values of the buckling load for externally stiffened cylinders.
    Generous safety factors are recommended.

    It is recommended that the buckling loads for a uniform cylinder with closely spaced, moderately large stiffeners
    calculated from this formula be multiplied by a factor of 0.65.

    Elastic constants calculated in elastic_constants.py

    :param E_x: Extensional stiffness of wall in x-direction
    :param E_y: Extensional stiffness of wall in y-direction
    :param E_xy: Extensional stiffness of wall in xy-plane
    :param G_xy: Shear stiffness of orthotropic or sandwich wall in x-y plane
    :param C_x: Coupling Constant for Orthotropic Cylinders
    :param C_y: Coupling Constant for Orthotropic Cylinders
    :param C_xy: Coupling Constant for Orthotropic Cylinders
    :param K_xy: Coupling Constant for Orthotropic Cylinders
    :param D_x: Bending stiffness per unit width of wall in x-direction
    :param D_y: Bending stiffness per unit width of wall in y-direction
    :param D_xy: Modified twisting stiffness per unit width of wall
    :param L: Length of cylinder
    :param r: Radius of cylinder
    :return: Critical Buckling Load (axial force) in N
    """
    gamma = 0.65  # Recommended knock-down factor

    # Check if cylinder is moderately long
    moderately_long = _check_moderately_long(gamma, L, r, t, v)

    # m and n, the number of axial half waves and circumferential full-waves.
    # Keep min. n = 4, since this becomes inaccurate for moderately long cylinders.
    m_trials = np.arange(1, 10)
    n_trials = np.arange(4 if moderately_long else 1, 10)
    m_min = 0
    n_min = 0

    # Create dataframe to store values of N_x for each m and n, for debugging
    # df = pd.DataFrame(columns=["N_x", "m", "n"])

    # Find m and n that minimize the buckling load
    N_x = np.inf
    for m in m_trials:
        for n in n_trials:
            # Simplify the following expressions
            A = m * np.pi / L
            B = n / r

            # Formulas from NASA SP-8007
            A_11 = E_x * (A ** 2) + G_xy * (B ** 2)
            A_22 = E_y * (B ** 2) + G_xy * (A ** 2)
            A_33 = D_x * (A ** 4) + D_xy * (A ** 2) * (B ** 2) + D_y * (B ** 4) + E_y / (r ** 2) + (
                    2 * C_y * (B ** 2)) / r \
                   + 2 * C_xy * (A ** 2) / r
            A_12 = (E_xy + G_xy) * A * B
            A_21 = A_12
            A_23 = (C_xy + 2 * K_xy) * (A ** 2) * B + (E_y / r) * B + C_y * (B ** 3)
            A_32 = A_23
            A_31 = (E_xy / r) * A + C_x * (A ** 3) + (C_xy + 2 * K_xy) * A * (B ** 2)
            A_13 = A_31

            # Determinant of A_11 --- A_33 using numpy
            det_A_numerator = np.linalg.det(np.array([[A_11, A_12, A_13], [A_21, A_22, A_23], [A_31, A_32, A_33]]))
            det_A_denominator = np.linalg.det(np.array([[A_11, A_12], [A_21, A_22]]))

            # Resulting N_x buckling load
            N_x_trial = ((1 / A) ** 2) * (det_A_numerator / det_A_denominator)

            # Concatenate values to dataframe
            # df = df.append({"N_x": N_x_trial, "m": m, "n": n}, ignore_index=True)

            if N_x_trial < N_x:
                N_x = N_x_trial
                m_min = m
                n_min = n

    return N_x * gamma 
