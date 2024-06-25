from psf_analyser.plotting_funcs.rbf_surface import gen_surface_plot
from natsort import natsorted
import dash_bootstrap_components as dbc
from dash import dcc, html

def get_zern_plots(df):
    zern_cols = [c for c in list(df) if 'pcoef' in c]
    plots = []
    for c in zern_cols:
        i = c.replace('pcoef_', '')
        labels = {
            'x': 'x (nm)',
            'y': 'y (nm)',
            f'pcoef_{i}': f'phase coef {i}',
            f'mcoef_{i}': f'mag. coef {i}'
        }
        title = f"Zern coef {i}"
        pcoef_plot = dcc.Graph(id=f'pcoef_{i}', figure=gen_surface_plot(df, 'x', 'y', c, labels, title))
        mcoef_plot = dcc.Graph(id=f'mcoef_{i}', figure=gen_surface_plot(df, 'x', 'y', c.replace('pcoef', 'mcoef'), labels, ''))
        layout = dbc.Row([
            dbc.Col(html.Div(pcoef_plot), width=6),
            dbc.Col(html.Div(mcoef_plot), width=6),
        ])
        plots.append(layout)

    return plots

