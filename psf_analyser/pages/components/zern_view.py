from natsort import natsorted
import dash_bootstrap_components as dbc
from dash import dcc, html
from pyotf.zernike import noll2name
import plotly.express as px

from psf_analyser.plotting_funcs.rbf_surface import gen_surface_plot

def gen_zern_surface_fig(df, c):
    i = int(c.replace('pcoef_', '').replace('mcoef_', ''))
    title = f"Zern coef {i} - {noll2name[i]}"
    labels = {
        'x': 'x (nm)',
        'y': 'y (nm)',
        f'pcoef_{i}': f'phase coef {i}',
        f'mcoef_{i}': f'mag. coef {i}'
    }
    return gen_surface_plot(df, 'x', 'y', c, labels, title)

def get_zern_plot_pair(df, c):
    i = int(c.replace('pcoef_', ''))
    pcoef_plot = dcc.Graph(id=f'pcoef_{i}', figure=gen_zern_surface_fig(df, c))
    mcoef_plot = dcc.Graph(id=f'mcoef_{i}', figure=gen_zern_surface_fig(df, c.replace('pcoef', 'mcoef')))
    layout = dbc.Row([
        dbc.Col(html.Div(pcoef_plot), width=6),
        dbc.Col(html.Div(mcoef_plot), width=6),
    ])
    return layout


def get_zern_cols(df):
    zern_cols = natsorted([c for c in list(df) if 'pcoef' in c])
    return zern_cols


def get_zern_rmse_plot(df):
    labels = {
        'x': 'x (pixel)',
        'y': 'y (pixel)'
    }
    fig = px.scatter(df, x='x', y='y', color='zern_rmse', labels=labels)
    fig.update_layout(clickmode='event')
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    return dbc.Row([
        dbc.Col(dcc.Graph(id=f'zern_rmse', figure=fig))
    ])


def get_zern_plots(df):
    zern_cols = get_zern_cols(df)
    if len(zern_cols) == 0:
        return html.H3('No zernike polynomial fitting data found, please prepare the data using `psf-prep-data --zern ...` ')
    df = df[df['zern_fit_mse']<0.01]
    plots = [get_zern_rmse_plot(df)]
    for c in zern_cols:
        plots.append(get_zern_plot_pair(df, c))

    return plots

