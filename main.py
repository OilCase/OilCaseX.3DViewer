import dash_bootstrap_components as dbc

from app.services.GridManager import GridManager
from app.dash.back_callbacks import *
from app.dash.clientside_callbacks import *
from app.dash.dash_layout import set_layout

# Загружаем переменные из файла .env
grid_manager = GridManager()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

set_layout(app)

set_save_token_callback(app)
set_get_token_callback(app)

add_dropdown_properties_callback(app, grid_manager)
add_checkbox_slices_mange_callback(app, grid_manager)
add_vtk_mange_callback(app, grid_manager)

app.run_server(debug=True)
