import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_vtk.utils import presets
import dash_vtk

points, polys, elevation, color_range = [], [], [], [0, 1]


def toDropOption(name):
    return {"label": name, "value": name}


# Основная область с визуализацией
def get_dbc_visualize():
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    html.Div(
                        get_vtk_view(),
                        style={"height": "100%",
                               "width": "100%", "overflow": "hidden"},
                    ),
                    style={"height": "85vh"},
                ),
            ],
        ),
        md=8,
    )

# Параметры визуализации


def get_dbc_visualize_settings():
    return dbc.Card(
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
                        marks={
                            1: "1", 50: "50", 100: "100"},
                    ),
                    html.Label(
                        "Цвет:", className="mt-3"),
                    dcc.Dropdown(
                        id="dropdown-preset",
                        options=list(
                            map(toDropOption, presets)),
                        value="erdc_rainbow_bright",
                    ),
                    html.Label(
                        "Свойство:", className="mt-3"),
                    dcc.Dropdown(
                        id="dropdown-property",
                        options=[],
                        value="",
                        placeholder="Выберите параметр",
                    ),
                    dcc.Checklist(
                        id="toggle-cube-axes",
                        options=[
                            {"label": " Отображать оси", "value": "grid"}],
                        value=[],
                        labelStyle={
                            "display": "inline-block"},
                        className="mt-3",
                    ),
                    dcc.Checklist(
                        id="toggle-edge-visibility",
                        options=[
                            {"label": " Отображать грани", "value": "edges"}],
                        value=[],
                        labelStyle={
                            "display": "inline-block"},
                        className="mt-3",
                    ),
                ]
            ),
        ],
        style={"margin-bottom": "15px"},
    )

# Управление X-срезами


def get_dbc_x_slices():
    return dbc.Card(
        [
            dbc.CardHeader("X-срезы"),
            dbc.CardBody(
                [
                    dcc.Checklist(
                        id="x-slices",
                        options=[
                        ],
                        value=[],
                        inline=True,
                    ),
                    dbc.Button(
                        "Выбрать все",
                        id="select-all-x",
                        color="primary",
                        size="sm",
                        style={
                            "margin-right": "5px", "margin-top": "10px"},
                    ),
                    dbc.Button(
                        "Снять все",
                        id="deselect-all-x",
                        color="secondary",
                        size="sm",
                        style={
                            "margin-top": "10px"},
                    ),
                ]
            ),
        ],
        style={"margin-bottom": "15px",
               "background": "#f8f9fa"},
    )

# Управление Y-срезами


def get_dbc_y_slices():
    return dbc.Card(
        [
            dbc.CardHeader("Y-срезы"),
            dbc.CardBody(
                [
                    dcc.Checklist(
                        id="y-slices",
                        options=[],
                        value=[],
                        inline=True,
                    ),
                    dbc.Button(
                        "Выбрать все",
                        id="select-all-y",
                        color="primary",
                        size="sm",
                        style={
                            "margin-right": "5px", "margin-top": "10px"},
                    ),
                    dbc.Button(
                        "Снять все",
                        id="deselect-all-y",
                        color="secondary",
                        size="sm",
                        style={
                            "margin-top": "10px"},
                    ),
                ]
            ),
        ],
        style={"background": "#f8f9fa"},
    )

# Кнопка применения


def get_dbc_accept_button():
    button = dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Применить",
                    id="apply-filters",
                    color="success",
                    size="lg",
                    className="d-block mx-auto mt-3",
                ),
                style={"textAlign": "center"},
            ),
            dcc.Loading(
                id="loading",
                type="circle",
                children=html.Div(
                    id='apply-filters-loader',
                    style={
                        "textAlign": "right"
                    }
                )
            ),]

    )

    return button

# Блок управления


def get_dbc_control():
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        # Параметры визуализации
                        get_dbc_visualize_settings(),

                        # Управление X-срезами
                        get_dbc_x_slices(),

                        # Управление Y-срезами
                        get_dbc_y_slices(),

                        # Кнопка применения
                        get_dbc_accept_button(),
                    ]
                ),
            ],
        ),
        md=4,
    )

# Блок с информацией о положении курсора


def get_dbc_cursor_info():
    return html.Pre(
        id="tooltip",
        style={
            "position": "absolute",
            "bottom": "25px",
            "left": "25px",
                    "zIndex": 1,
                    "color": "white",
                    "background": "rgba(0, 0, 0, 0.5)",
                    "padding": "10px",
                    "border-radius": "5px",
        },
    )

# окно просмотрп vtk


def get_vtk_view():
    return dash_vtk.View(
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
            dash_vtk.GeometryRepresentation(
                id="pick-rep",
                actor={"visibility": False},
                children=[
                    dash_vtk.Algorithm(
                        id="pick-sphere",
                        vtkClass="vtkSphereSource",
                        state={"radius": 5},
                    )
                ],
            ),
        ],
    )


def set_layout(app: dash.Dash):
    app.layout = dbc.Container(
        fluid=True,
        style={"height": "100vh", "padding": "10px"},
        children=[

            # Хранилище для фильтров
            dcc.Store(id="store-filters",
                      data={
                          "scale_factor": 20,
                          "preset": "erdc_rainbow_bright",
                          "property": "",
                          "x_slices": [],
                          "y_slices": [],
                          "show_cube_axes": [],
                          "edge_visibility": []
                      }),

            # Скрытый компонент для хранения токена
            dcc.Store(id='stored-token'),

            # Отслеживаем URL
            dcc.Location(id='url', refresh=False),
            dbc.Row(
                [
                    # Основная область с визуализацией
                    get_dbc_visualize(),

                    # Блок управления
                    get_dbc_control()
                ]
            )

            # Блок с информацией о положении курсора
            # get_dbc_cursor_info()
        ],
    )
