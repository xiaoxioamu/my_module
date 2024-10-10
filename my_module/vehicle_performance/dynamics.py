import math
import numpy as np
import matplotlib.pyplot as plt
def calculate_acceleration(vehicle_params, power, velocity):
    """
    计算车辆加速度
    :param vehicle_params: VehicleParameters对象
    :param power: 发动机功率(W)
    :param velocity: 当前速度(m/s)
    :return: 加速度(m/s^2)
    """
    force = power / velocity
    drag_force = 0.5 * 1.225 * vehicle_params.drag_coefficient * vehicle_params.frontal_area * velocity**2
    acceleration = (force - drag_force) / vehicle_params.mass
    return acceleration

def calculate_power_required(vehicle_params, velocity):
    """
    计算维持给定速度所需的功率
    :param vehicle_params: VehicleParameters对象
    :param velocity: 速度(m/s)
    :return: 所需功率(W)
    """
    drag_force = 0.5 * 1.225 * vehicle_params.drag_coefficient * vehicle_params.frontal_area * velocity**2
    power_required = drag_force * velocity / vehicle_params.engine_efficiency
    return power_required

def calculate_engine_speed_and_torque(velocity, drive_force, transmission_ratio, transmission_efficiency, wheel_radius):
    """
    Calculate the engine speed in RPM (w_e) based on velocity, gear ratio, and wheel radius.
    
    Args:
    velocity (float): Velocity in meters per second (m/s).
    gear_ratio (float): Gear ratio (dimensionless).
    wheel_radius (float): Wheel radius in meters.

    Returns:
    float: Engine speed in revolutions per minute (RPM).
    """
    TWO_PI = 2 * math.pi  # Constant for one full rotation in radians
    engine_speed = (velocity * transmission_ratio * 60) / (wheel_radius * TWO_PI)
    engine_torque = drive_force * wheel_radius / (transmission_ratio * transmission_efficiency)
    return engine_speed, engine_torque

def calculate_resistance_force(speed_range, theta, m, Cd, A, rho, Cr, g):
    """
    Calculate the resistance forces in different speed ranges.
    
    Args:
    speed_range (numpy.ndarray): Array of speeds in m/s.
    Cd (float): Aerodynamic drag coefficient.
    A (float): Frontal area in m^2.
    rho (float): Air density in kg/m^3.
    Cr (float): Rolling resistance coefficient.
    g (float): Gravitational acceleration in m/s^2.
    theta (float): Slope in radians.

    Returns:
    numpy.ndarray: Array of resistance forces in N.
    """
    resistance_force = 0.5 * Cd * A * rho * speed_range**2 + m * g * Cr * np.cos(theta) + m * g * np.sin(theta)
    
    return resistance_force

def calculate_resistance_and_driver_force(speed_range, theta, acceleration):
    """
    Calculate the resistance and driver forces in different speed ranges.
    
    Args:
    speed_range (numpy.ndarray): Array of speeds in m/s.
    theta (float): Slope in radians.
    acceleration (float): Acceleration in m/s^2.

    Returns:
    numpy.ndarray: Array of resistance forces in N.
    numpy.ndarray: Array of driver forces in N.
    """
    resistance_force = calculate_resistance_force(speed_range, theta)
    driver_force = m * acceleration + resistance_force   
    return resistance_force, driver_force

def plot_theta_and_engine_data(theta_degrees, engine_torque_array, speed_array):
    # Create two separate figures
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    fig2, ax2 = plt.subplots(figsize=(12, 6))

    # Plot theta_degrees on a separate figure
    ax1.set_xlabel('Data points')
    ax1.set_ylabel('Theta (percentage)')
    ax1.plot(theta_degrees, label='Theta (percentage)', color='tab:blue')
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')
    ax1.set_title('Theta vs Data Points')

    # Plot engine_torque_array and speed_array on the second figure
    color1 = 'tab:orange'
    ax2.set_xlabel('Data points')
    ax2.set_ylabel('Engine Torque', color=color1)
    ax2.plot(engine_torque_array, label='Engine Torque', color=color1)
    ax2.tick_params(axis='y', labelcolor=color1)

    ax3 = ax2.twinx()
    color2 = 'tab:green'
    ax3.set_ylabel('Speed (m/s)', color=color2)
    ax3.plot(speed_array, label='Speed', color=color2)
    ax3.tick_params(axis='y', labelcolor=color2)

    # Add legend for the second figure
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax2.legend(lines2 + lines3, labels2 + labels3, loc='upper left')

    ax2.set_title('Engine Torque and Speed vs Data Points')

    plt.tight_layout()
    plt.show()
