import numpy as np
import dome, cylinder, Tank
import geometry
import Tank_input
import materials
import elastic_properties



fwd_dome_object = dome.Dome(outer_radius=outer_radius,
                            pressure = pressure,
                            material=materials.materials[material])                    

# Create an aft dome object
aft_dome_object = dome.Dome(outer_radius=outer_radius,
                            pressure = pressure,
                            material=materials.materials[material])

# Create a cylinder object
cylinder_object = cylinder.Cylinder(outer_radius=outer_radius,
                                    thrust = thrust,
                                    pressure = pressure,
                                    heigh = height,
                                    material=materials.materials[material])

# Create a Tank_inputuration object
Tank_i= Tank.Tank(forward_dome=f_dome_object,
                                                    aft_dome=a_dome_object,
                                                    cylinder=cylinder_object,
                                                    fluid=fluids.fluids[Tank_input.fluid],
                                                    fluid_volume=Tank_input.fluid_volume,
                                                    internal_pressure=Tank_input.internal_pressure)

# Calculate stiffener elastic constants for
# ring-stringer method.
# stiffener_stringer_spacing = (2 * np.pi * (cylinder_outer_radius - cylinder_thickness / 2)) / Tank_input.cylinder_stringer_num
# #TODO figure out how this shit works 
# stiffener_ring_spacing = (cylinder_extension + dome_height) / Tank_input.cylinder_ring_num
# stiffener_stringer_cross_sectional_area = Tank_input.cylinder_stringer_height * Tank_input.cylinder_stringer_thickness
# stiffener_ring_cross_sectional_area = Tank_input.cylinder_ring_height * Tank_input.cylinder_ring_thickness
# stiffener_ring_I = geometry.rectangle_I(Tank_input.cylinder_ring_thickness, Tank_input.cylinder_ring_height)
# stiffener_stringer_I = geometry.rectangle_I(Tank_input.cylinder_stringer_thickness, Tank_input.cylinder_stringer_height)
# stiffener_ring_J = geometry.rectangle_J(Tank_input.cylinder_ring_thickness, Tank_input.cylinder_ring_height)
# stiffener_stringer_J = geometry.rectangle_J(Tank_input.cylinder_stringer_thickness, Tank_input.cylinder_stringer_height)
# stiffener_ring_z = -(Tank_input.cylinder_ring_height / 2) if Tank_input.cylinder_ring_inside_surface else (Tank_input.cylinder_ring_height / 2)
# stiffener_stringer_z = -(Tank_input.cylinder_stringer_height / 2) if Tank_input.cylinder_stringer_inside_surface else (Tank_input.cylinder_stringer_height / 2)
# cylinder_material_E = materials.materials[material]["youngs_modulus"]
# cylinder_material_G = materials.materials[material]["shear_modulus"]
# cylinder_material_v = materials.materials[material]["poisson_ratio"]
# ec = elastic_properties.isotropic_cylinders_with_rings_and_stringers(
#     E=cylinder_material_E,
#     E_s=cylinder_material_E,
#     E_r=cylinder_material_E,
#     G_s=cylinder_material_G,
#     G_r=cylinder_material_G,
#     A_s=stiffener_stringer_cross_sectional_area,
#     A_r=stiffener_ring_cross_sectional_area,
#     I_s=stiffener_stringer_I,
#     I_r=stiffener_ring_I,
#     J_s=stiffener_stringer_J,
#     J_r=stiffener_ring_J,
#     b_s=stiffener_stringer_spacing,
#     b_r=stiffener_ring_spacing,
#     z_s=stiffener_stringer_z,
#     z_r=stiffener_ring_z,
#     v=cylinder_material_v,
#     t=cylinder_thickness)

