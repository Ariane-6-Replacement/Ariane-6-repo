import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

# Rocket parameters (replace with actual values)
mass = 10  # kg
moment_of_inertia = 0.5  # kg*m^2
center_of_gravity = 0.2  # m from bottom

# PID controller parameters
Kp = np.array([3, 3, 0.1])  # proportional gain for x, y, and z
Ki = np.array([5000, 5000, 5000])  # integral gain for x, y, and z
Kd = np.array([0, 0, 5])  # derivative gain for x, y, and z

# Controller parameters
max_correction_angle = np.radians(10)  # in radians

# Simulation time and step size
t_max = 300  # seconds
dt = 0.01  # seconds

# Initialize integral_terms within the function on each call
integral_terms = np.zeros(3)  # initialize for x, y, and z
# Initialize PID terms outside the function
previous_error = np.zeros(3)
g = 9.81  # m/s^2

def calculate_pid_output(error, integral_terms, derivative_terms):
  """Calculates the PID controller output."""
  return Kp * error + Ki * integral_terms + Kd * derivative_terms

def update_animation(i):
  """Updates the animation for each frame."""
  global previous_error, integral_terms, desired_position, position

  # Calculate error in all three directions
  error = desired_position[i] - position[i]

  # Update integral terms with anti-windup protection
  integral_terms += error * dt
  #integral_terms = np.clip(integral_terms, -10, 10)  # limit integral terms

  # Calculate derivative term (avoid division by zero)
  derivative_terms = (error - previous_error) / dt if dt > 0 else np.zeros(3)
  previous_error = error

  # Calculate PID output (consider all three directions)
  control_force = calculate_pid_output(error, integral_terms, derivative_terms) * mass * g

  # Update acceleration with control force
  acceleration = control_force / mass

  if i + 1 < len(position):
    # Update position and velocity (assuming constant acceleration)
    position[i + 1] = position[i] + dt * (position[i] - center_of_gravity) + 0.5 * dt**2 * acceleration

    # Update line data for animation
    line.set_data_3d(position[:i + 1, 0], position[:i + 1, 1], position[:i + 1, 2])

  return line,

# Define a function for a parabola with peak at the center
def parabola(x, peak_z):
  # Calculate the center of the x-axis
  center_x = 500
  # Adjust the parabola based on the center
  return -peak_z * ((x - center_x) / 500)**2 + peak_z

# Set the desired peak height
peak_height = 100_000

landing_x = 1000
landing_y = 1000

# Create lists of x and y values
x = list(range(landing_x))
y = list(range(landing_y))  # Set all y values to 0

# Calculate the corresponding z-values
z = [parabola(i, peak_height) for c, i in enumerate(x)]

# Calculate time of flight
time_to_peak = np.sqrt(2 * peak_height / g)
total_time = 2 * time_to_peak  # assuming symmetrical trajectory

# Generate time points
time = np.arange(0, total_time, dt)
position = np.zeros((len(time), 3))  # store positions in x, y, z

# Combine points into a single array
desired_position = np.vstack((x, y, z)).T

# Create animation figure and line
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
desired_line, = ax.plot(desired_position[:, 0], desired_position[:, 1], desired_position[:, 2], label='Desired Trajectory')  # 3D line plot
line, = ax.plot(position[:, 0], position[:, 1], position[:, 2], label='Rocket Trajectory')  # 3D line plot


# Set plot limits and labels
ax.set_xlim(0, landing_x)
ax.set_ylim(0, landing_y)
ax.set_zlim(0, peak_height + 100)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")

# Animate
animation = animation.FuncAnimation(fig, update_animation, frames=len(time), interval=10)

plt.show()