# Ariane-6-repo

Make sure you are running from ~filepath/Ariane-6-repo. Otherwise you will get errors such as 'can not import python'

to fix try in terminal: 
export PYTHONPATH=/path/to/project_root:$PYTHONPATH

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Contact persons:

Trajectory:        Josh Shoemaker, Martin Starkov, Timo Esser    
Structure:         Marcel Kwapien, Thomas, McGearty
Propulsion:        Timo Esser, Dries Borstlap
Cost & Operations: Mike Noeri Tümah, Kristian Haralambiev
IDM:               Arnout Dourleijn, Martin Starkov

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Assumptions Trajectory:
gravity turn
Flat earth approx 
10% margins
CDs fixed 
constant thrust 
barges operate out to 400km
control systems function properly(big)
upper stage burn assumed impulsive shot
no inclination change 
upper satge scaled from Ariane 6 with propellent mass 
1.5 km/s delta V landing

Improvements to be made:
Better integrator 
Reentry heating 
Cd changing with Mach number
Better Cd estimation/ aero modelling
modeling forces required for control systems 
add solid and liquid boosters


file to run just trajectory: 3D turn

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-






Other:
Control and aerodynamics systems have not been worked out
