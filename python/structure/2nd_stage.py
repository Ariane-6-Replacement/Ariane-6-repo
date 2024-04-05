'''
Code developed for trajectory purposes only;
Sources: Ariane 5 Manual, Ariane Group, Wikipedia
'''
prop_mass_extension = NEWMASS - 31000
of = 
mf = prop_mass_extension / (of+1)
mox = prop_mass_extension - mf
vf = mf/ 70.8
vox = mox / 1141
Lf = vf / (np.pi * 2.7**2)
Lox = vox / (np.pi * 2.7**2)
struc_mass_extension = (Lf + Lox) * 3000 * np.pi * 5.4 * 5E-3
mfaring = 2657 #kg for Ariane 5
msyldas = 425 # kg for Ariane 5
mcone = 200 # kg for Ariane 5
#Scailing up the stage mass according to the O/F ratio of the engine; If better source becomes available for Ariance 6 use if instead
#4540 2nd stage mass for Ariane 5, 385 kg - mass difference between Ariane 6 and Ariane 5 upper stage engine 
mstruc = 4540 * 5.8 /4.9 + struc_mass_extension + 385

total_upper_stage_mass = mfaring + msyldas + mcone + mstruc



