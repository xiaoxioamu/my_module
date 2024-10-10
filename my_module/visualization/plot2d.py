import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
def plot2d_interactive_multi_axis(data, scale_factors=None, **kwargs):
    """
    Create an interactive 2D plot using Plotly with multiple y-axes and customizable parameters.
    
    Parameters:
    - data: list of numpy arrays or 1D arrays, each representing a dataset to plot
    - scale_factors: list of scale factors for each dataset (optional)
    - **kwargs: dictionary containing optional plot parameters
        - 'x_label': Label for the x-axis
        - 'y_labels': List of labels for each y-axis
        - 'title': Title of the plot
        - 'legend': List of legend labels
        - 'colors': List of colors for each dataset
        - 'line_styles': List of line styles for each dataset
        - 'line_widths': List of line widths for each dataset
        - 'figsize': Tuple specifying the figure size (width, height)
    """

    # Default parameters
    default_params = {
        'x_label': 'X-axis',
        'y_labels': [f'Y-axis {j+1}' for j in range(len(data))],
        'title': 'Interactive Multi-Axis 2D Plot',
        'legend': [f'Dataset {j+1}' for j in range(len(data))],
        'colors': ['blue', 'red', 'green', 'purple', 'orange'] * (len(data) // 5 + 1),
        'line_styles': ['solid'] * len(data),
        'line_widths': [2] * len(data),
        'figsize': (1000, 600)  # Plotly uses pixels
    }
    
    # Update default parameters with provided kwargs
    plot_params = {**default_params, **kwargs}
    
    fig = go.Figure()

    # If scale_factors is not provided, use 1 for all datasets
    if scale_factors is None:
        scale_factors = [1] * len(data)

    for j, (dataset, scale_factor) in enumerate(zip(data, scale_factors)):
        if isinstance(dataset, np.ndarray) and dataset.ndim == 2:
            x = dataset[:, 0]
            y = dataset[:, 1] * scale_factor
        elif isinstance(dataset, np.ndarray) and dataset.ndim == 1:
            x = np.arange(1, len(dataset) + 1)
            y = dataset * scale_factor
        else:
            raise ValueError("Each dataset should be a 1D or 2D numpy array.")
        
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name=plot_params['legend'][j],
                line=dict(
                    color=plot_params['colors'][j],
                    dash=plot_params['line_styles'][j],
                    width=plot_params['line_widths'][j]
                ),
                yaxis=f'y{j+1}' if j > 0 else 'y'
            )
        )

    # Update layout with multiple y-axes
    layout_updates = {
        'title': plot_params['title'],
        'xaxis': {'title': plot_params['x_label']},
        'yaxis': {'title': plot_params['y_labels'][0], 'side': 'left'},
        'width': plot_params['figsize'][0],
        'height': plot_params['figsize'][1],
        'legend': {'yanchor': "top", 'y': 0.99, 'xanchor': "left", 'x': 0.01}
    }

    # Add additional y-axes
    for j in range(1, len(data)):
        layout_updates[f'yaxis{j+1}'] = {
            'title': plot_params['y_labels'][j],
            'side': 'right' if j % 2 else 'left',
            'overlaying': 'y',
            'anchor': 'free',
            'position': 1 - (j * 0.05)  # Adjust position to prevent overlap
        }

    fig.update_layout(**layout_updates)
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    fig.show()

def plot2d_interactive_multi_axis_with_x(x_data, y_data, scale_factors=None, **kwargs):
    """
    Create an interactive 2D plot using Plotly with multiple y-axes and customizable parameters.
    
    Parameters:
    - x_data: numpy array or 1D array for x-axis data
    - y_data: list of numpy arrays or 1D arrays, each representing a dataset to plot on y-axis
    - scale_factors: list of scale factors for each y dataset (optional)
    - **kwargs: dictionary containing optional plot parameters

    Example usage:
    ```python
    import numpy as np

    # Sample data
    time = np.linspace(0, 10, 100)
    torque = np.sin(time)
    speed = np.cos(time)
    pitch_angle = np.tan(time)

    # Custom parameters
    custom_params = {
        'x_label': '时间 (s)',
        'y_labels': ['扭矩 (Nm)', '速度 (km/h)', '坡度 (°)'],
        'title': '多参数随时间变化',
        'legend': ['扭矩', '速度', '坡度'],
        'colors': ['red', 'blue', 'green'],
        'line_styles': ['solid', 'dash', 'dot'],
        'line_widths': [2, 2, 2],
        'figsize': (1200, 700)
    }

    # Scale factors
    scale_factors = [1, 0.1, 10]

    # Plotting
    plot2d_interactive_multi_axis_with_x(time, [torque, speed, pitch_angle], scale_factors=scale_factors, **custom_params)
    ```
    """
    # Default parameters
    default_params = {
        'x_label': 'X-axis',
        'y_labels': [f'Y-axis {j+1}' for j in range(len(y_data))],
        'title': 'Interactive Multi-Axis 2D Plot',
        'legend': [f'Dataset {j+1}' for j in range(len(y_data))],
        'colors': ['blue', 'red', 'green', 'purple', 'orange'] * (len(y_data) // 5 + 1),
        'line_styles': ['solid'] * len(y_data),
        'line_widths': [2] * len(y_data),
        'figsize': (1000, 600)  # Plotly uses pixels
    }
    
    # Update default parameters with provided kwargs
    plot_params = {**default_params, **kwargs}
    
    fig = go.Figure()

    # If scale_factors is not provided, use 1 for all datasets
    if scale_factors is None:
        scale_factors = [1] * len(y_data)

    for j, (dataset, scale_factor) in enumerate(zip(y_data, scale_factors)):
        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=dataset * scale_factor,
                mode='lines',
                name=plot_params['legend'][j],
                line=dict(
                    color=plot_params['colors'][j],
                    dash=plot_params['line_styles'][j],
                    width=plot_params['line_widths'][j]
                ),
                yaxis=f'y{j+1}' if j > 0 else 'y'
            )
        )

    # Update layout with multiple y-axes
    layout_updates = {
        'title': plot_params['title'],
        'xaxis': {'title': plot_params['x_label']},
        'yaxis': {'title': plot_params['y_labels'][0], 'side': 'left'},
        'width': plot_params['figsize'][0],
        'height': plot_params['figsize'][1],
        'legend': {'yanchor': "top", 'y': 0.99, 'xanchor': "left", 'x': 0.01}
    }

    # Add additional y-axes
    for j in range(1, len(y_data)):
        layout_updates[f'yaxis{j+1}'] = {
            'title': plot_params['y_labels'][j],
            'side': 'right' if j % 2 else 'left',
            'overlaying': 'y',
            'anchor': 'free',
            'position': 1 - (j * 0.05)  # Adjust position to prevent overlap
        }

    fig.update_layout(**layout_updates)
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    fig.show()

def plot_2d(data, **kwargs):
    """
    Create a 2D plot using matplotlib with customizable parameters.
    
    Parameters:
    - data: list of numpy arrays or 1D arrays, each representing a dataset to plot
    - **kwargs: dictionary containing optional plot parameters
    
    Example usage:
    ```python
    actual_eng_percent_torque = PCC_test_data['ActualEngPercentTorque'].astype(float)
    eng_reference_torque = 3250
    actual_eng_torque = actual_eng_percent_torque * eng_reference_torque / 100

    # Using custom parameters
    custom_params = {
        'x_label': 'Time (s)',
        'y_label': 'Amplitude',
        'title': 'Custom 2D Plot Example',
        'legend': ['Signal A', 'Signal B'],
        'colors': ['red', 'blue'],
        'line_styles': ['-', '--'],
        'markers': ['o', 's'],
        'figsize': (12, 8)
    }
    plot_2d([actual_eng_percent_torque, actual_eng_torque], **custom_params)
    plot_2d([actual_eng_torque], **custom_params)
    ```
    """
    # Default values
    default_params = {
        'x_label': 'X-axis',
        'y_label': 'Y-axis',
        'title': '2D Plot',
        'legend': [f'Dataset {j+1}' for j in range(len(data))],
        'colors': plt.cm.rainbow(np.linspace(0, 1, len(data))),
        'line_styles': ['-', '--', '-.', ':'] * (len(data) // 4 + 1),
        'markers': ['o', 's', '^', 'D', 'v', '*', 'p', 'h'] * (len(data) // 8 + 1),
        'figsize': (10, 6)
    }
    
    # Update default parameters with provided kwargs
    plot_params = {**default_params, **kwargs}
    
    # Create the plot
    plt.figure(figsize=plot_params['figsize'])
    
    for j, dataset in enumerate(data):
        if dataset.ndim == 1:
            # If dataset is 1D, use array index as x-values
            x = np.arange(1, len(dataset) + 1)
            y = dataset
        else:
            # If dataset is 2D, use first column as x and second as y
            x = dataset[:, 0]
            y = dataset[:, 1]
        
        plt.plot(x, y, 
                 color=plot_params['colors'][j],
                 linestyle=plot_params['line_styles'][j],
                 marker=plot_params['markers'][j],
                 label=plot_params['legend'][j])
    
    plt.xlabel(plot_params['x_label'])
    plt.ylabel(plot_params['y_label'])
    plt.title(plot_params['title'])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()
