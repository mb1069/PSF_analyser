from scipy.interpolate import Rbf
import numpy as np
import plotly.graph_objects as go
from config import PLOTLY_THEME

def fit_smooth_surface(points_x, points_y, points_z, smooth=0.1):
    """
    Fit a smooth surface to 3D point data using radial basis function interpolation.
    
    Args:
        points_x (np.array): X coordinates of the data points.
        points_y (np.array): Y coordinates of the data points.
        points_z (np.array): Z coordinates of the data points.
        smooth (float): Smoothing factor for the interpolation. Higher values result in smoother surfaces.
        
    Returns:
        interp_func (callable): A function that can be called with X and Y coordinates to get the corresponding Z values.
    """
    # Create a radial basis function interpolator
    rbf = Rbf(points_x, points_y, points_z, smooth=smooth)
    
    # Define a function to evaluate the interpolated surface at given X and Y coordinates
    def interp_func(x, y):
        return rbf(x, y)
    
    return interp_func

def gen_surface_plot(df, x_col, y_col, z_col, labels, title):
    points_x = df[x_col].to_numpy()
    points_y = df[y_col].to_numpy()
    points_z = df[z_col].to_numpy()

    # Fit a smooth surface to the data
    interp_func = fit_smooth_surface(points_x, points_y, points_z, smooth=0.1)

    # Evaluate the interpolated surface at some new points
    new_x = np.linspace(points_x.min(), points_x.max(), 100)
    new_y = np.linspace(points_y.min(), points_y.max(), 100)
    new_z = np.array([[interp_func(x, y) for y in new_y] for x in new_x])

    layout = go.Layout(
        title=title,
        xaxis = {'title': labels[x_col]},
        yaxis = {'title': labels[y_col]},
        template=PLOTLY_THEME
    )
    fig = go.Figure(data =
        go.Contour(
            z=new_z.reshape((new_x.shape[0], new_y.shape[0])),
            x=new_x, 
            y=new_y,
            colorbar={"title": labels[z_col]},
            name=""
        ),
        layout=layout
    )
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    fig.update_traces(hovertemplate=f'{x_col}: %{{x}} <br>{y_col}: %{{y}} <br>{z_col}: %{{z}}') #
    return fig