from python.structure.Loading.buckling_coeff import gamma_d
import numpy as np



def critical_cylinder_bending(r, t ,p, E, v, Ixx):

    phi = 1 / 16 * np.sqrt(r / t)

    # Knock-down factor
    gamma = 1 - 0.901 * (1 - np.exp(-phi))

    parameter = p / E * (r / t) ** 2
    dgamma = gamma_d(parameter)

    M_press = np.pi * r * E * t**2 * (gamma / np.sqrt(3 * (1 - v ** 2)) + dgamma) + 0.8 * p * np.pi * r**2
    return M_press

# def critical_stiffened_cylinder_bending(E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, L, r, t, v):


#     """
#     Stiffened shell bending formula from NASA SP-8007 (2020Rev) section 4.1.2 on orthotropic cylinders.

#     Experimental results indicate that the critical maximum load of a stiffened cylinder in bending can exceed the
#     critical load in axial compression. However, in the absence of an extensive investigation, it is recommended that
#     the critical maximum load of a uniform cylinder with closely spaced stiffeners be taken as equal to the critical
#     load in axial compression, calculated from the critical stiffener buckling formula multiplied by a factor
#     gamma = 0.75, which is slightly greater than the factor for compression loaded cylinders due to the reduced
#     imperfection sensitivity. In addition, as with compression-loaded stiffened cylinders, local skin buckling can also
#      occur prior to global buckling, as in the case of widely spaced stiffeners, and should be checked.
#     """

#     gamma = 0.75
#     buckling_load = buckling.critical_stiffened_cylinder_buckling(E_x, E_y, E_xy, G_xy, C_x, C_y, C_xy, K_xy, D_x, D_y, D_xy, L, r, t, v)

#     return gamma * buckling_load / (Coeff_A_Loads * K_MP * FOSY_b_global)