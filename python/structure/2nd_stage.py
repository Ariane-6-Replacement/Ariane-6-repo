'''
Code developed for trajectory purpose only;
Sources: Ariane 5 Manual, Ariane Group, Wikipedia
'''
prop_mass_extension = NEWMASS - 31000
of = 5.8
mf = prop_mass_extension / (of+1)
mox = prop_mass_extension - mf
vf = mf/ 70.8
vox = mox / 1141
Lf = vf / (np.pi * 2.7**2)
Lox = vox / (np.pi * 2.7**2)
struc_mass_extension = (Lf + Lox) * 3000 * np.pi * 5.4 * 5E-3
mfaring = 2657 #kg
msyldas = 425 # kg
mcone = 200 # kg
mstruc = 4540 * 5.8 /4.9 + struc_mass_extension + 385

total_upper_stage_mass = mfaring + msyldas + mcone + mstruc



