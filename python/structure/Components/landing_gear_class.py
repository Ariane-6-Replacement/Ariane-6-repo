import  numpy  as np

def LG_stability(H0,alpha,mass,I):
    '''H0 - height of the center of gravity with respect to the ground in m
    alpha - turn over angle in deg
    Lfp - landing gear radius in m
    '''
    # print('alpha', np.radians(alpha))
    Lfp = 0.1

    while np.sqrt(2*Lfp**2+H0**2) * (1 - np.cos(np.radians(alpha))) * 1/(1+(mass + (2*Lfp**2+H0**2))/I) > np.sqrt(H0**2 + Lfp**2) - H0:
        Lfp+=0.1
    return Lfp

# test bit 
if __name__ == "__main__":
    H0 = 6.5
    alpha = 40
    mass = 6500
    I = 2500000
    Lfp = LG_stability(H0,alpha,mass,I)
    print("LFP: ", Lfp)




def LG_geometry(Lfp, D, tau_p, tau_s, drop_h):
    '''Lw - width of the lander
    tau_p - primary strut angle
    tau_s - secondary strut angle
    x - width beyonf the lander frame
    z - height of the top attachemnt point 
    Lp - length of the primary strut
    hH - height of the primary strut with respect to the lander
    Ls - length of the secondary strut
    drop_h - vertical stroke limit '''
    tau_p = 
    tau_s
    x = Lfp - D

    z = x / np.tan( np.radians( tau_p ) )

    Lp = np.sqrt(x**2 + z**2)

    hP = np.sin(np.radians( tau_s - tau_p)) * Lp / 2 * 1/ np.sin(np.radians(tau_s))

    Ls = 0.5 * Lp * np.sin(np.radians(tau_p)) / np.sin(np.radians(tau_s))
    
    S_p_max = Lp - (z - drop_h) / np.cos(np.radians(tau_p))

    #SHADY SHIT as fuck 
    S_s_max = 0.2 * Ls

    return Lp, hP, Ls, S_p_max, S_s_max
