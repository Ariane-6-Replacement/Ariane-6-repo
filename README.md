# Ariane-6-repo

There are two ways to run the code. The simplest way is by clicking on the `run_idm.exe` file located in the same directory as this README file (or download it directly from [this link](https://github.com/Ariane-6-Replacement/Ariane-6-repo/raw/main/run_idm.exe)).

Alternatively, you can run the IDM from the console. Make sure you are running it from wherever you cloned this repository ~filepath/Ariane-6-repo/python. Otherwise you will get errors such as 'cannot import python' or 'no module named python'

To fix try in terminal, run the following command (replace the path to project root with where you cloned this repository):
`export PYTHONPATH=/path/to/project_root:$PYTHONPATH`

Then to open the IDM simply, run the following command:
`python main.py`

- main.py calls rocket.py which in turn calls all the necessary scripts
- The ui is setup in setup.py

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Contact persons:

Trajectory: Josh Shoemaker, Martin Starkov, Timo Esser  
Structure: Marcel Kwapien, Thomas, McGearty
Propulsion: Timo Esser, Dries Borstlap
Cost & Operations: Mike Noeri Tümah, Kristian Haralambiev
IDM: Arnout Dourleijn, Martin Starkov

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Assumptions Trajectory:

- Gravity turn
- Flat earth approximation
- 10% margins
- CDs (drag coefficients) fixed
- Constant thrust
- Barges operate out to 400km
- Control systems function properly(big)
- Upper stage burn assumed impulsive shot
- No inclination change
- Upper stage scaled from Ariane 6 with propellent mass
- 1.5 km/s delta V landing

Improvements to be made:

- Better integrator
- Re-entry heating
- Cd changing with Mach number
- Better Cd estimation/ aero modelling
- Modeling forces required for control systems
- Adding support for solid and liquid boosters

File to run only trajectory code: trajectory/trajectory.py

-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Other:
Control and aerodynamics systems have not been worked out.

Other limitations include: uncertainty of the cost model, constant Cd assumption (ascend/descend differ), lack of heating estimations/calculations, second stage modelled as impulsive shot.
