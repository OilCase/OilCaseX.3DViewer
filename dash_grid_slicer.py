import dash
import dash_vtk
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import random
import os
import numpy as np
import pyvista as pv

from vtk.util.numpy_support import vtk_to_numpy
# import webbrowser
from dash_vtk.utils import presets

from utils.PyGRDECL.GRDECL2VTK import GeologyModel




def toDropOption(name):
    return {"label": name, "value": name}


class GridManager():
    def __init__(self, directory_path, grid_name, vtp_path):
        file_name = ["_GRID", "_ACTNUM", "_PORO", "_PERMX"]
        grid_file_path = directory_path + "/" + "temporary.GRDECL"

        with open(grid_file_path, 'w') as outfile:
            for fname in file_name:
                with open(directory_path + "/" + grid_name + fname + ".inc") as infile:
                    outfile.write(infile.read().replace('NOECHO', ''))
                    infile.close()

            with open(directory_path + "/" + grid_name + ".GRDECL") as infile:
                outfile.write(infile.read().replace('NOECHO', ''))
                infile.close()
                
            outfile.close()



        vtp_path = os.path.join('data/3d_objects', f'grid.vtp')

        model = GeologyModel(filename=grid_file_path)

        mask = np.where(model.GRDECL_Data.SpatialDatas['PORO'] == 0)
        model.GRDECL_Data.SpatialDatas['ACTNUM'][mask] = 0

        model.GRDECL2VTK()
        model.Write2VTP(vtp_path)

        os.remove(grid_file_path)

        self.NX, self.NY, self.NZ = model.GRDECL_Data.NX, model.GRDECL_Data.NY, model.GRDECL_Data.NZ
        self.properties = list(model.GRDECL_Data.SpatialDatas.keys())

    def create_mesh(self, vtp_path):
        self.mesh = pv.read(vtp_path).extract_geometry()

    def update_grid_geometry(self, prop="PORO", scalar=20, slice_x=None, slice_y=None):
        mesh = self.mesh.copy()
        mesh.points[:, 2] *= scalar 

        # Обрезка по срезам
        actnum = mesh["ACTNUM"][::6]
        actnum = actnum.reshape((self.NX, self.NY, self.NZ), order="F")
        result_actnum = np.zeros_like(actnum)
      
        result_actnum[slice_x, :, :] = actnum[slice_x, :, :]
       
        result_actnum[:, slice_y, :] = actnum[:, slice_y, :]
        result_actnum = np.repeat(result_actnum.reshape(-1, order="F"), 6)
        mesh["ACTNUM"] = result_actnum

        ghosts = np.argwhere(mesh["ACTNUM"] == 0)
        mesh = mesh.remove_cells(ghosts)
        points = mesh.points.ravel()
        polys = vtk_to_numpy(mesh.GetPolys().GetData())

        elevation = np.repeat(mesh[prop][::6], 8)
        min_elevation = np.amin(elevation)
        max_elevation = np.amax(elevation)

        return [points, polys, elevation, [min_elevation, max_elevation]]
    


vtp_path = 'data/3d_objects/grid.vtp'
directory_path = 'data/INCLUDE'
grid_name = 'DynamicModel'


Grid_Manager = GridManager(directory_path, grid_name, vtp_path)
Grid_Manager.create_mesh(vtp_path)

points, polys, elevation, color_range = [], [], [], [0, 1]



# Setup VTK rendering of PointCloud
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

vtk_view = dash_vtk.View(
    id="vtk-view",
    pickingModes=["hover"],
    children=[
        dash_vtk.GeometryRepresentation(
            id="vtk-representation",
            children=[
                dash_vtk.PolyData(
                    id="vtk-polydata",
                    points=points,
                    polys=polys,
                    children=[
                        dash_vtk.PointData(
                            [
                                dash_vtk.DataArray(
                                    id="vtk-array",
                                    registration="setScalars",
                                    name="elevation",
                                    values=elevation,
                                )
                            ]
                        )
                    ],
                )
            ],
            colorMapPreset="erdc_blue2green_muted",
            colorDataRange=color_range,
            property={"edgeVisibility": False},
            showCubeAxes=False,
            cubeAxesStyle={"axisLabels": ["", "", ""]},
        ),
        # dash_vtk.GeometryRepresentation(
        #     id="pick-rep",
        #     actor={"visibility": False},
        #     children=[
        #         dash_vtk.Algorithm(
        #             id="pick-sphere",
        #             vtkClass="vtkSphereSource",
        #             state={"radius": 5},
        #         )
        #     ],
        # ),
    ],
)


app.layout = dbc.Container(
    fluid=True,
    style={"height": "100vh", "padding": "10px"},
    children=[
        # Хранилище для фильтров
        dcc.Store(id="store-filters", data={
            "scale_factor": 20,
            "preset": "erdc_rainbow_bright",
            "property": "PORO",
            "x_slices": [i for i in range(Grid_Manager.NX)],
            "y_slices": [i for i in range(Grid_Manager.NY)],
            "show_cube_axes": [],
            "edge_visibility": []
        }),
        dbc.Row(
            [
                # Основная область с визуализацией
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                html.Div(
                                    vtk_view,
                                    style={"height": "100%", "width": "100%", "overflow": "hidden"},
                                ),
                                style={"height": "85vh"},
                            ),
                        ],
                    ),
                    md=8,
                ),
                # Блок управления
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    # Параметры визуализации
                                    dbc.Card(
                                        [
                                            dbc.CardBody(
                                                [
                                                    html.Label("Масштаб:"),
                                                    dcc.Slider(
                                                        id="scale-factor",
                                                        min=1,
                                                        max=100,
                                                        step=1,
                                                        value=20,
                                                        marks={1: "1", 50: "50", 100: "100"},
                                                    ),
                                                    html.Label("Цвет:", className="mt-3"),
                                                    dcc.Dropdown(
                                                        id="dropdown-preset",
                                                        options=list(map(toDropOption, presets)),
                                                        value="erdc_rainbow_bright",
                                                    ),
                                                    html.Label("Свойство:", className="mt-3"),
                                                    dcc.Dropdown(
                                                        id="dropdown-property",
                                                        options=[
                                                            {"label": key, "value": key}
                                                            for key in Grid_Manager.properties
                                                            if key != "ACTNUM"
                                                        ],
                                                        value="PORO",
                                                        placeholder="Выберите параметр",
                                                    ),
                                                    dcc.Checklist(
                                                        id="toggle-cube-axes",
                                                        options=[{"label": " Отображать оси", "value": "grid"}],
                                                        value=[],
                                                        labelStyle={"display": "inline-block"},
                                                        className="mt-3",
                                                    ),
                                                    dcc.Checklist(
                                                        id="toggle-edge-visibility",
                                                        options=[{"label": " Отображать грани", "value": "edges"}],
                                                        value=[],
                                                        labelStyle={"display": "inline-block"},
                                                        className="mt-3",
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={"margin-bottom": "15px"},
                                    ),
                                    # Управление X-срезами
                                    dbc.Card(
                                        [
                                            dbc.CardHeader("X-срезы"),
                                            dbc.CardBody(
                                                [
                                                    dcc.Checklist(
                                                        id="x-slices",
                                                        options=[
                                                            {"label": str(i), "value": i}
                                                            for i in range(Grid_Manager.NX)
                                                        ],
                                                        value=[i for i in range(Grid_Manager.NX)],
                                                        inline=True,
                                                    ),
                                                    dbc.Button(
                                                        "Выбрать все",
                                                        id="select-all-x",
                                                        color="primary",
                                                        size="sm",
                                                        style={"margin-right": "5px", "margin-top": "10px"},
                                                    ),
                                                    dbc.Button(
                                                        "Снять все",
                                                        id="deselect-all-x",
                                                        color="secondary",
                                                        size="sm",
                                                        style={"margin-top": "10px"},
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={"margin-bottom": "15px", "background": "#f8f9fa"},
                                    ),
                                    # Управление Y-срезами
                                    dbc.Card(
                                        [
                                            dbc.CardHeader("Y-срезы"),
                                            dbc.CardBody(
                                                [
                                                    dcc.Checklist(
                                                        id="y-slices",
                                                        options=[
                                                            {"label": str(i), "value": i}
                                                            for i in range(Grid_Manager.NY-1)
                                                        ],
                                                        value=[i for i in range(Grid_Manager.NY-1)],
                                                        inline=True,
                                                    ),
                                                    dbc.Button(
                                                        "Выбрать все",
                                                        id="select-all-y",
                                                        color="primary",
                                                        size="sm",
                                                        style={"margin-right": "5px", "margin-top": "10px"},
                                                    ),
                                                    dbc.Button(
                                                        "Снять все",
                                                        id="deselect-all-y",
                                                        color="secondary",
                                                        size="sm",
                                                        style={"margin-top": "10px"},
                                                    ),
                                                ]
                                            ),
                                        ],
                                        style={"background": "#f8f9fa"},
                                    ),
                                    # Кнопка применения
                                    dbc.Row(
                                        dbc.Col(
                                            dbc.Button(
                                                "Применить",
                                                id="apply-filters",
                                                color="success",
                                                size="lg",
                                                className="d-block mx-auto mt-3",
                                            ),
                                            style={"textAlign": "center"},
                                        )
                                    ),
                                ]
                            ),
                        ],
                    ),
                    md=4,
                ),
            ]
        ),
        # Блок с информацией о положении курсора
        # html.Pre(
        #     id="tooltip",
        #     style={
        #         "position": "absolute",
        #         "bottom": "25px",
        #         "left": "25px",
        #         "zIndex": 1,
        #         "color": "white",
        #         "background": "rgba(0, 0, 0, 0.5)",
        #         "padding": "10px",
        #         "border-radius": "5px",
        #     },
        # ),
    ],
)


@app.callback(
    [
        Output("x-slices", "value"),
        Output("y-slices", "value"),
    ],
    [
        Input("select-all-x", "n_clicks"),
        Input("deselect-all-x", "n_clicks"),
        Input("select-all-y", "n_clicks"),
        Input("deselect-all-y", "n_clicks"),
    ],
)
def manage_slices(select_x, deselect_x, select_y, deselect_y):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "select-all-x":
        return [i for i in range(Grid_Manager.NX)], dash.no_update
    elif triggered_id == "deselect-all-x":
        return [], dash.no_update
    elif triggered_id == "select-all-y":
        return dash.no_update, [i for i in range(Grid_Manager.NY)]
    elif triggered_id == "deselect-all-y":
        return dash.no_update, []

    return dash.no_update, dash.no_update



@app.callback(
    [
        Output("vtk-representation", "showCubeAxes"),
        Output("vtk-representation", "colorMapPreset"),
        Output("vtk-representation", "colorDataRange"),
        Output("vtk-representation", "property"),
        Output("vtk-polydata", "points"),
        Output("vtk-polydata", "polys"),
        Output("vtk-array", "values"),
        Output("vtk-view", "triggerResetCamera"),
    ],
    [
        Input("apply-filters", "n_clicks"),
    ],
    [
        State("dropdown-preset", "value"),
        State("scale-factor", "value"),
        State("dropdown-property", "value"),
        State("x-slices", "value"),
        State("y-slices", "value"),
        State("toggle-cube-axes", "value"),
        State("toggle-edge-visibility", "value"),
    ],
)
def update_vtk(n_clicks, preset, scale_factor, prop, x_slices, y_slices, cube_axes, edge_visibility):
    # Обновление данных только после нажатия кнопки "Применить"
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate

    points, polys, elevation, color_range = Grid_Manager.update_grid_geometry(
        prop=prop, scalar=scale_factor, slice_x=x_slices, slice_y=y_slices
    )

    return [
        "grid" in cube_axes,
        preset,
        color_range,
        {"edgeVisibility": "edges" in edge_visibility},
        points,
        polys,
        elevation,
        random.random(),
    ]




if __name__ == "__main__":
    # url =  'http://127.0.0.1:8050/'
    # webbrowser.open(url, new=2, autoraise=True)  
    app.run_server(debug=False)
