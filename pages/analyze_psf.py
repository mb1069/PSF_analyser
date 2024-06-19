import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
from natsort import natsorted

from psf_analyzer.util import find_files_in_result_dir
from psf_analyzer.bead_data_handler import BeadDataHandler
from plotting_funcs.rbf_surface import gen_surface_plot
from pages.components.ind_bead_view import get_ind_bead_view, get_bead_xy_scatter, gen_bead_table
from pages.components.explore_bead_view import get_explore_bead_view

dash.register_page(__name__)

data_handler = None

def fig_fwhm_xy(locs):
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'fwhm_xy': 'Lateral FWHM (nm)'
    }
    title = 'Lateral FWHM (nm) across FOV'
    fig = gen_surface_plot(locs[locs['fwhm_xy_mse']<0.001], 'x', 'y', 'fwhm_xy', labels, title)
    return fig


def fig_fwhm_z(locs):
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'fwhm_z': 'Axial FWHM (nm)'
    }
    title = 'Axial FWHM (nm) across FOV'
    fig = gen_surface_plot(locs[locs['fwhm_z_mse']<0.2], 'x', 'y', 'fwhm_z', labels, title)
    return fig

def fig_offset_surface(locs):
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'offset': 'Offset (nm)'
    }
    title = 'Offset (nm)'
    fig = gen_surface_plot(locs, 'x', 'y', 'offset', labels, title)
    return fig


def fig_offset_scatter(locs):
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'offset': 'Offset (nm)'
    }
    title = 'Offset (nm)'
    fig = px.scatter(locs, x='x', y='y', labels=labels, title=title)
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
    )
    return fig

def gen_figs(locs):
    figs = [
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fwhm_xy', figure=fig_fwhm_xy(locs))),
                    dbc.Col(dcc.Graph(id='fwhm_z', figure=fig_fwhm_z(locs)))
                ]),
                
            ], title='FWHM (xy and z)'),
            dbc.AccordionItem([
                dbc.Col(dcc.Graph(id='offsets_surface', figure=fig_offset_surface(locs))),
            ], title='Offset'),
            dbc.AccordionItem([
                get_explore_bead_view(data_handler)
            ], title='Explore beads'),
            dbc.AccordionItem([
                get_ind_bead_view(data_handler, 0)
            ], title='Invididual beads'),
        ], start_collapsed=False),
    ]
    return figs


def layout(folder_name=None):
    global data_handler
    files = find_files_in_result_dir(folder_name)
    data_handler = BeadDataHandler(**files)
    fnames = ['all'] + list(natsorted(data_handler.locs['fname'].unique()))
    return dbc.Container([
        html.H1('Loading results...'),
        dbc.Row([
            dbc.Col([
                dbc.Label("Select files", html_for="file-selector"),
                dcc.Dropdown(options=fnames, value='all', id='file-selector'),
            ])
        ], style={'margin-bottom': '1em'}),
        dbc.Row(dbc.Col(*gen_figs(data_handler.locs)))
    ], className="dbc")


@callback(
    [
        Output('ind-bead-profile-img', 'src'),
        Output('ind-bead-xy-scatter', 'figure'),
        Output('bead-data-table', 'children'),
    ],
    Input('ind-bead-xy-scatter', 'clickData'),
    prevent_initial_call=True
    )
def display_click_data(clickData):
    point_id = clickData['points'][0]['customdata'][0]

    img = data_handler.get_bead_profile_img(point_id)
    fig = get_bead_xy_scatter(data_handler, point_id)
    table = gen_bead_table(data_handler, point_id)
    return img, fig, table

@callback(
    [
        Output('fwhm_xy', 'figure', allow_duplicate=True),
        Output('fwhm_z', 'figure', allow_duplicate=True),
        Output('offsets_surface', 'figure', allow_duplicate=True),
        Output('ind-bead-profile-img', 'src', allow_duplicate=True),
        Output('ind-bead-xy-scatter', 'figure', allow_duplicate=True),
        Output('bead-data-table', 'children', allow_duplicate=True),
    ],
    Input('file-selector', 'value'),
    prevent_initial_call=True
)
def filter_data_handler_by_files(value):
    locs = data_handler._locs
    if value != 'all':
        locs = locs[locs['fname']==value]
    data_handler.locs = locs
    print(list(locs))

    i = locs['point_id'].to_numpy()[0]
    img = data_handler.get_bead_profile_img(i)
    fig = get_bead_xy_scatter(data_handler, i)
    table = gen_bead_table(data_handler, i)

    fwhm_xy_fig = fig_fwhm_xy(locs)
    fwhm_z_fig = fig_fwhm_z(locs)
    offsets_surface_fig = fig_offset_surface(locs)

    return fwhm_xy_fig, fwhm_z_fig, offsets_surface_fig, img, fig, table
