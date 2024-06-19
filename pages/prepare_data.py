import dash
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc
from pathlib import Path
from natsort import natsorted
dash.register_page(__name__)

from psf_analyzer.util import find_files_in_result_dir

layout = dbc.Container([
        html.Br(),
        dbc.Form(
            id='folder_picker',
            # name='select_folder',
            action='/analyze-psf',
            method='GET',
            prevent_default_on_submit=False,
            children=[
                html.Div([
                    dbc.Label('Folder of results to analyse:'),
                    dbc.Input(id='folder_name', name='folder_name', placeholder='Folder to search for tif files', type='text', value='/home/miguel/Projects/PSF_analyzer/different_objectives/olympus_100x_motic_x.35_up_1'),
                ], className="mb-3"),
                html.Div([
                    dbc.Button('Submit')
                ], className="mb-3")
            ]
        ),
        html.Div(id='selected_files')
    ])


@callback(
    Output('selected_files', 'children'),
    Input("folder_name", "value"),
    # Input("folder_picker", "n_submit"),
)
def find_tif_files(folder_name):
    files = find_files_in_result_dir(folder_name)
    tiff_files = [html.P(f'{key}: {fpath}') for key, fpath in files.items()]

    resp = html.Div(children=[
        html.H2('Found files:'),
        *tiff_files
    ])
    return resp
