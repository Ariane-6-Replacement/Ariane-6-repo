"""
This function takes in the principal stresses at a position and checks whether the material will yield there, based on
the von Mises yield criterion.

Source: wikipedia
"""


def yield_check(principalstress1: float, principalstress2: float, yieldstress: float) -> tuple:
    """
    Checks whether material yields or not based on principal stresses in Von Mises yield criterion.

    :param principalstress1: first principal stress, maximum
    :param principalstress2: second principal stress, minimum
    :param yieldstress: yield stress of the material
    :return: True if it doesn't yield, False if it yields
    """

    if (principalstress1 ** 2 + principalstress2 ** 2 - principalstress1 * principalstress2) ** (1 / 2) < yieldstress:
        return True
    else:
        return False