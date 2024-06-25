from psf_analyser.plotting_funcs.rbf_surface import gen_surface_plot
from natsort import natsorted
import dash_bootstrap_components as dbc
from dash import dcc, html
from pyotf.zernike import noll2name


def get_zern_plot_pair(df, c):
    i = int(c.replace('pcoef_', ''))
    labels = {
        'x': 'x (nm)',
        'y': 'y (nm)',
        f'pcoef_{i}': f'phase coef {i}',
        f'mcoef_{i}': f'mag. coef {i}'
    }
    title = f"Zern coef {i} - {noll2name[i]}"
    pcoef_plot = dcc.Graph(id=f'pcoef_{i}', figure=gen_surface_plot(df, 'x', 'y', c, labels, title))
    mcoef_plot = dcc.Graph(id=f'mcoef_{i}', figure=gen_surface_plot(df, 'x', 'y', c.replace('pcoef', 'mcoef'), labels, ''))
    layout = dbc.Row([
        dbc.Col(html.Div(pcoef_plot), width=6),
        dbc.Col(html.Div(mcoef_plot), width=6),
    ])
    return layout

def get_zern_plots(df):
    zern_cols = natsorted([c for c in list(df) if 'pcoef' in c])
    if len(zern_cols) == 0:
        return html.H3('No zernike polynomial fitting data found, please prepare the data using `psf-prep-data --zern ...` ')
    plots = []
    for c in zern_cols:
        plots.append(get_zern_plot_pair(df, c))

    return plots

