import numpy as np
import matplotlib.pyplot as plt

# Define the parameters of the rocket
mass = 497  # kg
body_length = 7.6  # m
body_diameter = 0.3  # m
equivalent_area = 0.0707  # m^2
moment_of_inertia_yy = 6.0  # kg.m^2
moment_of_inertia_xx = 2170  # kg.m^2

# Define the bounds of the variables as a dictionary
variable_bounds = {
    "V": (1400, 300),  # Lower bound, Upper bound
    "gamma": (-60 * np.pi / 180, 60 * np.pi / 180),  # Convert degrees to radians
    "x": (0, 15000),
    "z": (-3500, -200),
    "alpha": (-10 * np.pi / 180, 10 * np.pi / 180),  # Convert degrees to radians
    "theta_dot": (-10 * np.pi / 180, 10 * np.pi / 180),  # Convert degrees to radians
    "sigma": (-20 * np.pi / 180, 20 * np.pi / 180),  # Convert degrees to radians
    "sigma_dot": (-10 * np.pi / 180, 10 * np.pi / 180),  # Convert degrees to radians
}

def print_rocket_parameters():
    # Print the parameters and bounds for reference
    print("Rocket parameters:")
    print(f"Mass: {mass} kg")
    print(f"Body length: {body_length} m")
    print(f"Body diameter: {body_diameter} m")
    print(f"Equivalent area: {equivalent_area} m^2")
    print(f"Moment of inertia (Iyy): {moment_of_inertia_yy} kg.m^2")
    print(f"Moment of inertia (Ixx): {moment_of_inertia_xx} kg.m^2")

def print_variable_bounds():
    print("\nVariable bounds:")
    for key, value in variable_bounds.items():
        print(f"{key}: ({value[0]}, {value[1]})")

def calculate_P_theta_theta(theta_i, gamma_0_i, V, F_z, m, alpha, g):
    P_theta_theta = g * np.sin(theta_i + gamma_0_i) * (
        np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
        - np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
    ) * (
        V * np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
        - V * np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
    ) ** 2 + (
        F_z(theta_i, gamma_0_i, alpha) * np.cos(alpha) / m
        - g * np.cos(theta_i + gamma_0_i)
        - V * gamma_0_i
    ) * (
        np.cos(gamma_0_i) * np.sin(theta_i + gamma_0_i)
        + np.sin(gamma_0_i) * np.cos(theta_i + gamma_0_i)
    ) * (
        V * np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
        - V * np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
    ) ** 2
    return P_theta_theta

def calculate_P_theta_xi(theta_i, gamma_0_i, V, F_z, m, alpha, g):
    P_theta_xi = (
        g * np.cos(theta_i + gamma_0_i) * (
            np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
            - np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
        ) * (
            V * np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
            - V * np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
        ) ** 2 + (
            F_z(theta_i, gamma_0_i, alpha) * np.sin(alpha) / m
            - g * np.sin(theta_i + gamma_0_i)
        ) * (
            np.cos(gamma_0_i) * np.sin(theta_i + gamma_0_i)
            + np.sin(gamma_0_i) * np.cos(theta_i + gamma_0_i)
        ) * (
            V * np.cos(gamma_0_i) * np.cos(theta_i + gamma_0_i)
            - V * np.sin(gamma_0_i) * np.sin(theta_i + gamma_0_i)
        ) ** 2
    )
    return P_theta_xi

def calculate_P_xi_theta(theta_i, gamma_0_i, V, F_z, m, alpha):
    # ... Implementation of the P_xi_theta formula ...
    return P_xi_theta_value

def solve_for_delta_alpha(P_theta_theta, P_theta_xi, P_xi_theta, delta_theta_i, delta_xi_i, ...):
  """
  This function solves for the control command (delta_alpha) using the provided matrices and state information.

  Args:
      P_theta_theta: A numpy array representing the P_theta_theta matrix.
      P_theta_xi: A numpy array representing the P_theta_xi matrix.
      P_xi_theta: A numpy array representing the P_xi_theta matrix.
      delta_theta_i: The current value of delta_theta.
      delta_xi_i: The current value of delta_xi.
      ...: Additional arguments based on the article (e.g., desired position, state variables).

  Returns:
      The calculated value of delta_alpha.
  """

  # 1. Construct the right-hand side vector (b) based on the article's formula.
  #    This likely involves the desired position, state variables, and potentially alpha.

  # 2. Solve the linear system of equations: P * [delta_theta, delta_xi] + [P_theta_alpha] * alpha = b

  # 3. Extract the solution for delta_alpha from the resulting vector.

  return delta_alpha

def eta_scheme_flat_trajectory(theta_i, gamma_0_i, V, F_z, m, alpha, delta_theta_i, delta_xi_i):
    g = 9.81  # Acceleration due to gravity

    P_theta_theta = calculate_P_theta_theta(theta_i, gamma_0_i, V, F_z, m, alpha, g)
    P_theta_xi = calculate_P_theta_xi(theta_i, gamma_0_i, V, F_z, m, alpha, g)
    P_xi_theta = calculate_P_xi_theta(theta_i, gamma_0_i, V, F_z, m, alpha)

    # Placeholder for P_theta_alpha (requires further information from the article)
    P_theta_alpha = ...

    # Construct the matrices and vectors as described in the article 
    # ... (requires specific values for variables)

    delta_alpha = solve_for_delta_alpha(P_theta_theta, P_theta_xi, P_xi_theta, delta_theta_i, delta_xi_i, ...)

    return delta_theta_i, delta_xi_i, delta_alpha 

print_rocket_parameters()
print_variable_bounds()

def generate_trajectory(desired_trajectory, initial_conditions, timesteps, dt, eta_scheme_flat_trajectory):
  """
  This function generates a trajectory using the eta scheme for flat trajectory tracking.

  Args:
      desired_trajectory: A numpy array (n x 2) containing the desired position at each timestep.
      initial_conditions: A tuple (theta_i, gamma_0_i, V, m, alpha) representing initial conditions.
      timesteps: The number of timesteps for the simulation.
      dt: The time step size.
      eta_scheme_flat_trajectory: A function implementing the eta scheme for flat trajectory tracking.

  Returns:
      A tuple containing:
          - trajectory: A numpy array (n x 2) containing the generated trajectory.
          - control_commands: A list of control commands (delta_alpha) at each timestep.
  """

  trajectory = np.zeros((timesteps, 2))
  control_commands = []

  theta_i, gamma_0_i, V, m, alpha = initial_conditions

  # Assuming delta_theta_i and delta_xi_i are initially zero
  delta_theta_i, delta_xi_i = 0, 0

  for i in range(timesteps):
    # Extract desired position for the current timestep
    desired_pos = desired_trajectory[i]

    # Update the state using the eta scheme
    delta_theta_i, delta_xi_i, delta_alpha = eta_scheme_flat_trajectory(
        theta_i, gamma_0_i, V, F_z, m, alpha, delta_theta_i, delta_xi_i
    )

    # Update state variables for the next timestep
    theta_i += delta_theta_i * dt
    # ... Update other state variables based on the specific model ...

    # Update trajectory and control command history
    trajectory[i] = [theta_i, ...]  # Replace ... with actual state variables
    control_commands.append(delta_alpha)

  return trajectory, control_commands

def calculate_open_loop_trajectory(initial_position, desired_trajectory, timesteps):
    """
    This function calculates an open-loop trajectory for a given desired trajectory.

    Args:
        initial_position: A numpy array (2,) representing the initial position (x, z).
        desired_trajectory: A numpy array (n x 2) containing the desired trajectory points (x, z).
        timesteps: Number of timesteps for discretizing the desired trajectory.

    Returns:
        A numpy array (n x 2) containing the controller output trajectory points (x, z).
    """

    # Check if initial position has the correct dimension (2)
    if initial_position.shape != (2,):
        raise ValueError("Initial position must be a 2-dimensional vector.")

    # Check if desired trajectory has the correct shape (n x 2)
    if desired_trajectory.shape[1] != 2:
        raise ValueError("Desired trajectory must have 2 columns (x, z).")

    # Ensure desired trajectory and timesteps have the same length
    if desired_trajectory.shape[0] != timesteps:
        raise ValueError(
            "Desired trajectory and timesteps must have the same number of elements."
        )

    # Reshape desired_trajectory to a column vector (n x 1)
    desired_trajectory_reshaped = desired_trajectory.reshape(-1, 1)

    # Generate interpolation indices (n x 1)
    indices = np.arange(desired_trajectory.shape[0])[:, np.newaxis]

    # Perform linear interpolation along the first dimension (rows)
    controller_trajectory = np.interp(
        np.linspace(0, 1, timesteps), indices, desired_trajectory_reshaped
    )

    # Reshape back to original (n x 2) format
    controller_trajectory = controller_trajectory.reshape(-1, 2)

    # Adjust the controller trajectory to start from the initial position
    controller_trajectory += initial_position - controller_trajectory[0, :]

    return controller_trajectory

def generate_parabolic_trajectory(initial_position, final_position, flight_time, timesteps, a=0.5):
    """
    This function generates a parabolic trajectory between two points.

    Args:
        initial_position: A numpy array (2,) representing the initial position (x, z).
        final_position: A numpy array (2,) representing the desired final position (x, z).
        flight_time: Total flight time in seconds.
        timesteps: Number of timesteps for discretizing the trajectory.
        a: Parameter for controlling the shape of the parabola (default 0.5).

    Returns:
        A numpy array (timesteps x 2) containing the desired trajectory points (x, z).
    """

    # Check if initial and final positions have the same dimension (2)
    if initial_position.shape != (2,) or final_position.shape != (2,):
        raise ValueError("Initial and final positions must be 2-dimensional vectors.")

    # Calculate time vector
    time_vector = np.linspace(0, flight_time, timesteps)

    # Calculate x positions based on the parabola equation
    x = initial_position[0] + (final_position[0] - initial_position[0]) * (
        time_vector / flight_time
    )

    # Calculate z positions with parabolic shape
    z = a * (x - (initial_position[0] + final_position[0]) / 2) ** 2 + initial_position[1]

    # Combine x and z into a single trajectory array
    trajectory = np.stack((x, z), axis=1)

    return trajectory

def plot_flat_trajectory():
    # Define initial position
    initial_position = np.array([0, 0])

    # Define desired trajectory parameters
    final_position = np.array([1000, 100])  # Adjust final position as needed
    flight_time = 10  # Adjust flight time as needed
    timesteps = 200
    a = 0.5  # Adjust parabola parameter (a) to control the shape

    # Generate parabolic desired trajectory
    desired_trajectory = generate_parabolic_trajectory(
        initial_position, final_position, flight_time, timesteps, a
    )

    # Calculate controller trajectory
    controller_trajectory = calculate_open_loop_trajectory(
        initial_position, desired_trajectory, timesteps
    )

    # Plot desired and controller trajectories
    plt.plot(desired_trajectory[:, 0], desired_trajectory[:, 1], label="Desired")
    plt.plot(controller_trajectory[:, 0], controller_trajectory[:, 1], label="Controller")
    plt.xlabel("X Position")
    plt.ylabel("Z Position")
    plt.title("Desired vs. Controller Trajectories")
    plt.legend()
    plt.grid(True)
    plt.show()