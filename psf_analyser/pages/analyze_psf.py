import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
from natsort import natsorted
import traceback
from dash.exceptions import PreventUpdate

from psf_analyser.data_handler.util import find_files_in_result_dir
from psf_analyser.data_handler.bead_data_handler import BeadDataHandler
from psf_analyser.plotting_funcs.rbf_surface import gen_surface_plot
from psf_analyser.pages.components.ind_bead_view import get_ind_bead_view, get_bead_xy_scatter, gen_bead_table
from psf_analyser.pages.components.explore_bead_view import get_explore_bead_view, get_explore_bead_fig
from psf_analyser.pages.components.zern_view import get_zern_plots
dash.register_page(__name__)

data_handler = None

def fig_fwhm_xy(data_handler):
    max_mse = 0.001
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'fwhm_xy': 'Lateral FWHM (nm)'
    }
    title = 'Lateral FWHM (nm) across FOV'

    vis_locs = data_handler.locs
    all_locs = data_handler._locs
    all_locs = all_locs[all_locs['fwhm_xy_mse']<=max_mse]
    z_min = all_locs['fwhm_xy'].min()
    z_max = all_locs['fwhm_xy'].max()

    fig = gen_surface_plot(vis_locs[vis_locs['fwhm_xy_mse']<0.001], 'x', 'y', 'fwhm_xy', labels, title, z_min, z_max)
    return fig


def fig_fwhm_z(data_handler):
    max_mse = 0.2
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'fwhm_z': 'Axial FWHM (nm)'
    }
    title = 'Axial FWHM (nm) across FOV'

    vis_locs = data_handler.locs
    all_locs = data_handler._locs
    all_locs = all_locs[all_locs['fwhm_z_mse']<=max_mse]
    z_min = all_locs['fwhm_z'].min()
    z_max = all_locs['fwhm_z'].max()

    fig = gen_surface_plot(vis_locs[vis_locs['fwhm_z_mse']<0.2], 'x', 'y', 'fwhm_z', labels, title, z_min, z_max)
    return fig

def fig_offset_surface(data_handler):
    labels = {
        'x': 'X (pixels)',
        'y': 'Y (pixels)',
        'offset': 'Offset (nm)'
    }
    title = 'Offset (nm)'

    vis_locs = data_handler.locs
    all_locs = data_handler._locs
    z_min = all_locs['offset'].min()
    z_max = all_locs['offset'].max()
    fig = gen_surface_plot(vis_locs, 'x', 'y', 'offset', labels, title, z_min, z_max)
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
        scaleanchor = 'x',
        scaleratio = 1,
    )
    return fig

def gen_figs():
    figs = [
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fwhm_xy', figure=fig_fwhm_xy(data_handler))),
                    dbc.Col(dcc.Graph(id='fwhm_z', figure=fig_fwhm_z(data_handler)))
                ])
            ], title='FWHM (xy and z)', id='fwhm-plots'),
            dbc.AccordionItem([
                dbc.Col(dcc.Graph(id='offsets_surface', figure=fig_offset_surface(data_handler))),
            ], title='Offset'),
            dbc.AccordionItem([
                get_explore_bead_view(data_handler.locs)
            ], title='Explore beads'),
            dbc.AccordionItem([
                get_ind_bead_view(data_handler, 0)
            ], title='Invididual beads'),
            dbc.AccordionItem(children=get_zern_plots(data_handler.locs), title='Zernike modelling'),
        ], start_collapsed=False),
    ]
    return figs

def no_files_found_layout():
    return dbc.Container([
        html.H4('No folder name specified...'),
        html.A(href='/', children=[
            html.P('Click here to return to the home page')
        ])
    ])

def layout(folder_name=None):
    global data_handler
    if folder_name is None:
        return no_files_found_layout()

    try:
        files = find_files_in_result_dir(folder_name)
        data_handler = BeadDataHandler(**files)
        fnames = ['all'] + list(natsorted(data_handler.locs['fname'].unique()))
        return dbc.Container([
            html.H1('Loading results...'),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Select bead stacks:', html_for='file-selector'),
                    dcc.Dropdown(options=fnames, value='all', id='file-selector'),
                ])
            ], style={'margin-bottom': '1em'}),
            dbc.Row(dbc.Col(dbc.Spinner(color="primary", children=gen_figs())))
        ], className='dbc')
    except Exception as e:
        print(traceback.format_exc())
        return dbc.Container([
            dbc.Alert(f'Could not find results in path {folder_name}', color='danger'),
            html.A(href='/', children=[
                html.P('Click here to return to the home page')
            ])
        ])


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

    i = locs['point_id'].to_numpy()[0]
    img = data_handler.get_bead_profile_img(i)
    fig = get_bead_xy_scatter(data_handler, i)
    table = gen_bead_table(data_handler, i)

    fwhm_xy_fig = fig_fwhm_xy(data_handler)
    fwhm_z_fig = fig_fwhm_z(data_handler)
    offsets_surface_fig = fig_offset_surface(data_handler)

    return fwhm_xy_fig, fwhm_z_fig, offsets_surface_fig, img, fig, table

    
@callback(
    Output("bead-explore-graph", "figure"),
    [
        Input("bead-explore-x-col-sel", "value"),
        Input("bead-explore-y-col-sel", "value"),
        Input("bead-explore-graph-type-sel", "value"),
    ],
)
def generate_chart(x_axis, y_axis, graph):
    if not x_axis:
        raise PreventUpdate
    if not y_axis:
        raise PreventUpdate
    if not graph:
        raise PreventUpdate
    return get_explore_bead_fig(data_handler.locs, x_axis, y_axis, graph)
