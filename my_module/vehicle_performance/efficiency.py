import numpy as np
from scipy.interpolate import interp1d, RegularGridInterpolator
def calculate_fuel_consumption(vehicle_params, power, velocity, fuel_energy_density):
    """
    计算燃料消耗率
    :param vehicle_params: VehicleParameters对象
    :param power: 发动机功率(W)
    :param velocity: 当前速度(m/s)
    :param fuel_energy_density: 燃料能量密度(J/L)
    :return: 燃料消耗率(L/100km)
    """
    energy_consumption = power / vehicle_params.engine_efficiency
    fuel_consumption = energy_consumption / fuel_energy_density
    fuel_consumption_per_100km = fuel_consumption * 3600 / velocity * 100
    return fuel_consumption_per_100km

def calculate_range(vehicle_params, fuel_capacity, velocity, fuel_energy_density):
    """
    计算车辆续航里程
    :param vehicle_params: VehicleParameters对象
    :param fuel_capacity: 燃料容量(L)
    :param velocity: 巡航速度(m/s)
    :param fuel_energy_density: 燃料能量密度(J/L)
    :return: 续航里程(km)
    """
    from .dynamics import calculate_power_required
    power_required = calculate_power_required(vehicle_params, velocity)
    fuel_consumption = calculate_fuel_consumption(vehicle_params, power_required, velocity, fuel_energy_density)
    range_km = fuel_capacity / (fuel_consumption / 100)
    return range_km

def plot_engine_characteristics_interactive(engine_map, actual_engine_rpm, actual_engine_torque, **kwargs):
    """
    Create an interactive plot of engine universal characteristic curves using Plotly.
    
    Parameters:
    - engine_map: Dictionary containing engine map data
    - actual_engine_rpm: Array of actual engine RPM values
    - actual_engine_torque: Array of actual engine torque values
    - **kwargs: Dictionary containing optional plot parameters
        - 'title': Title of the plot (default: 'Engine Universal Characteristic Curves')
        - 'width': Width of the figure in pixels (default: 1200)
        - 'height': Height of the figure in pixels (default: 800)
    
    Returns:
    None: Displays the plot using Plotly
    """
    import plotly.graph_objects as go

    # Default parameters
    default_params = {
        'title': 'Engine Universal Characteristic Curves',
        'width': 1200,
        'height': 800,
    }
    
    # Update default parameters with provided kwargs
    plot_params = {**default_params, **kwargs}

    fc_map_gpkwh = engine_map['fc_map_gpkwh']
    fc_map_nm = engine_map['fc_map_nm']
    fc_map_rpm = engine_map['fc_map_rpm']
    fc_map_maxNm = engine_map['fc_map_maxNm']
    fc_map_frNm = engine_map['fc_map_frNm']

    # Create figure with single plot
    fig = go.Figure()

    # 2D Contour Plot with different density for different ranges and labeled contours
    fig.add_trace(
        go.Contour(
            z=fc_map_gpkwh, 
            x=fc_map_rpm, 
            y=fc_map_nm, 
            contours=dict(
                start=fc_map_gpkwh.min(),
                end=300,
                size=(300 - fc_map_gpkwh.min()) / 80,
                showlabels=True,
                labelfont=dict(size=10, color='black')
            ),
            line=dict(color='black'),
            contours_coloring='lines',
            hoverinfo='x+y+z',
            hoverlabel=dict(bgcolor="purple", font_size=12, font_family="Arial"),
            texttemplate='%{z:.0f}',
            textfont=dict(size=8),
            showscale=False  # This line removes the colorbar
        )
    )

    fig.add_trace(
        go.Contour(
            z=fc_map_gpkwh, 
            x=fc_map_rpm, 
            y=fc_map_nm, 
            contours=dict(
                start=300,
                end=fc_map_gpkwh.max(),
                size=(fc_map_gpkwh.max() - 300) / 10,
                showlabels=True,
                labelfont=dict(size=10, color='black')
            ),
            line=dict(color='black'),
            showscale=False,
            contours_coloring='lines',
            hoverinfo='x+y+z',
            hoverlabel=dict(bgcolor="purple", font_size=12, font_family="Arial"),
            texttemplate='%{z:.0f}',
            textfont=dict(size=8)
        )
    )

    # Add fc_map_frNm curve
    fig.add_trace(
        go.Scatter(
            x=fc_map_rpm,
            y=fc_map_frNm,
            mode='lines',
            name='Engine Friction Torque',
            line=dict(color='green', width=2),
            hovertemplate='RPM: %{x}<br>Friction Nm: %{y}<extra></extra>'
        )
    )

    # Add fc_map_maxNm curve
    fig.add_trace(
        go.Scatter(
            x=fc_map_rpm,
            y=fc_map_maxNm,
            mode='lines',
            name='Engine Max Torque',
            line=dict(color='red', width=2),
            hovertemplate='RPM: %{x}<br>Max Nm: %{y}<extra></extra>'
        )
    )

    # Add actual engine data points
    fig.add_trace(
        go.Scatter(
            x=actual_engine_rpm,
            y=actual_engine_torque,
            mode='markers',
            name='Actual Engine Data',
            marker=dict(
                color='yellow',
                size=5,
                line=dict(
                    color='black',
                    width=1
                )
            ),
            hovertemplate='RPM: %{x}<br>Torque: %{y}<extra></extra>'
        )
    )

    fig.update_layout(
        title=plot_params['title'],
        xaxis_title='Engine Speed (RPM)',
        yaxis_title='Engine Torque (Nm)',
        width=plot_params['width'],
        height=plot_params['height'],
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    fig.show()

# Usage example:
# plot_engine_characteristics_interactive(engine_map, actual_engine_rpm, actual_engine_torque, title="Custom Title", width=1000, height=800)


def f_fuel_gps_map(fc_map_rpm, fc_map_nm, fc_map_maxNm, fc_map_gpkwh,
                  fc_radps, fc_Nm_all, fc_Nm_fr, fc_radps_idle, fc_idle_gps):
    """
    功能：查表计算发动机瞬时能耗 (Lookup table to calculate instantaneous engine fuel consumption)

    参数:
        fc_map_rpm (np.ndarray): RPM map
        fc_map_nm (np.ndarray): Torque (Nm) map
        fc_map_maxNm (np.ndarray): Maximum Torque map
        fc_map_gpkwh (np.ndarray): Fuel consumption map (g/kWh)
        fc_radps (np.ndarray): Engine speed in rad/s
        fc_Nm_all (np.ndarray): Total torque (Nm)
        fc_Nm_fr (np.ndarray): Friction torque (Nm)
        fc_radps_idle (np.ndarray): Idle engine speed in rad/s
        fc_idle_gps (np.ndarray): Idle fuel consumption (g/s)

    返回:
        np.ndarray: Fuel consumption map (fuel_gps_map)
    """
    # Ensure inputs are numpy arrays
    fc_map_rpm = np.asarray(fc_map_rpm)
    fc_map_nm = np.asarray(fc_map_nm)
    fc_map_maxNm = np.asarray(fc_map_maxNm)
    fc_map_gpkwh = np.asarray(fc_map_gpkwh).T
    fc_radps = np.asarray(fc_radps)
    fc_Nm_all = np.asarray(fc_Nm_all)
    fc_Nm_fr = np.asarray(fc_Nm_fr)
    fc_radps_idle = np.asarray(fc_radps_idle)
    fc_idle_gps = np.asarray(fc_idle_gps)

    # Convert rad/s to RPM
    temp_rpm = fc_radps * 30 / np.pi

    # Clamp temp_rpm within fc_map_rpm range
    temp_rpm = np.clip(temp_rpm, np.min(fc_map_rpm), np.max(fc_map_rpm))

    # Calculate net torque
    temp_nm = fc_Nm_all - fc_Nm_fr

    # Clamp temp_nm within fc_map_nm range
    temp_nm = np.clip(temp_nm, np.min(fc_map_nm), np.max(fc_map_nm))

    # Interpolate max torque for temp_rpm using interp1d
    interp_maxNm_func = interp1d(fc_map_rpm, fc_map_maxNm, kind='linear', fill_value="extrapolate")
    temp_nm_max = interp_maxNm_func(temp_rpm) * 0.95  # Scale down by 0.95

    # Ensure temp_nm does not exceed temp_nm_max
    temp_nm = np.minimum(temp_nm, temp_nm_max)

    # Create 2D interpolation function for fc_map_gpkwh using RegularGridInterpolator
    interp_gpkwh_func = RegularGridInterpolator(
        (fc_map_rpm, fc_map_nm),
        fc_map_gpkwh,
        bounds_error=False,
        fill_value=0
    )

    # Prepare points for interpolation
    points = np.array([temp_rpm, temp_nm]).T  # Shape (N, 2)

    # Interpolate gpkwh for temp_rpm and temp_nm
    temp_gpkwh = interp_gpkwh_func(points)
    temp_gpkwh = np.nan_to_num(temp_gpkwh, nan=0.0)

    # Recalculate temp_rpm and temp_nm after initial adjustments
    temp_rpm = fc_radps * 30 / np.pi
    temp_nm = fc_Nm_all - fc_Nm_fr
    temp_nm = np.maximum(temp_nm, 0)  # Net torque cannot be negative

    # Calculate fuel_gps_map
    fuel_gps_map = (temp_nm * temp_rpm * np.pi / 30) / (1000 * 3600) * temp_gpkwh

    # Idle fuel consumption special handling
    fc_rpm_idle_max = fc_radps_idle * 30 / np.pi + 10  # RPM
    fc_rpm_idle_min = fc_radps_idle * 30 / np.pi - 50  # RPM
    fc_nm_idle_max = np.max(fc_map_maxNm) * 0.1  # 10% of max torque

    # Create boolean mask for idle conditions
    idle_mask = (
        (temp_rpm > fc_rpm_idle_min) &
        (temp_rpm < fc_rpm_idle_max) &
        (temp_nm < fc_nm_idle_max)
    )

    # Apply idle fuel consumption
    fuel_gps_map[idle_mask] = fc_idle_gps

    # Set fuel consumption to 0 where total torque or engine speed is 0 or negative
    fuel_gps_map = np.where((fc_Nm_all <= 0) | (fc_radps <= 0), 0, fuel_gps_map)

    return fuel_gps_map

# Example input data
# fc_map_rpm = np.array([1000, 2000, 3000, 4000, 5000])
# fc_map_nm = np.array([50, 100, 150, 200, 250])
# fc_map_maxNm = np.array([200, 250, 300, 280, 260])
# fc_map_gpkwh = np.array([
#     [250, 240, 230, 220, 210],
#     [240, 230, 220, 210, 200],
#     [230, 220, 210, 200, 190],
#     [220, 210, 200, 190, 180],
#     [210, 200, 190, 180, 170]
# ])
# fc_radps = np.array([100, 150, 200])
# fc_Nm_all = np.array([120, 180, 240])
# fc_Nm_fr = np.array([20, 30, 40])
# fc_radps_idle = np.array([50])
# fc_idle_gps = np.array([0.5])

# # Calculate fuel consumption
# fuel_gps_map = f_fuel_gps_map(
#     fc_map_rpm, fc_map_nm, fc_map_maxNm, fc_map_gpkwh,
#     fc_radps, fc_Nm_all, fc_Nm_fr, fc_radps_idle, fc_idle_gps
# )

# print(fuel_gps_map)
