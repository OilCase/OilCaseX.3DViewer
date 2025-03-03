import random
import time

import dash
from dash.dependencies import Input, Output, State

from app.GridManager import GridManager


# Callback для обновления опций Dropdown свойств
def add_dropdown_properties_callback(app: dash.Dash, grid_manager: GridManager):
    @app.callback(
        [
            Output('dropdown-property', 'options'),
            Output('dropdown-date', 'options'),
            Output("x-slices", "options"),
            Output("y-slices", "options"),
        ],
        [
            Input('stored-token', 'data'),
            Input('dropdown-property', 'value'),
            Input("dropdown-date", "value"),
        ]
    )
    def update_dropdown_options(token, selected_property, selected_date):
        # Здесь можно сделать запрос к бэкенду для получения данных
        values = [{'label': opt.PropertyDescription, 'value': opt.HDMName}
                  for opt in grid_manager.GetProperties(token)]

        available_dates = [{'label': str(available_date.Date), 'value': available_date.OrderNUmber}
                           for available_date in grid_manager.GetAvailableDates(token, selected_property)]
        
        x_slices = [{'label': opt + 1, 'value': opt}
                    for opt in grid_manager.GetNX(token, selected_property, selected_date)]
        y_slices = [{'label': opt + 1, 'value': opt}
                    for opt in grid_manager.GetNY(token, selected_property, selected_date)]

        return [values, available_dates, x_slices, y_slices]
    


def add_checkbox_slices_mange_callback(app: dash.Dash, grid_manager: GridManager):
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
            Input('stored-token', 'data'),
            Input("dropdown-property", "value"),
            Input("dropdown-date", "value"),
        ],
    )
    def manage_slices(select_x, deselect_x, select_y, deselect_y, token, target_property, target_order_number):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update, dash.no_update

        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_id == "select-all-x":
            return grid_manager.GetNX(token, target_property, target_order_number), dash.no_update

        elif triggered_id == "deselect-all-x":
            return [], dash.no_update

        elif triggered_id == "select-all-y":
            return dash.no_update, grid_manager.GetNY(token, target_property, target_order_number)

        elif triggered_id == "deselect-all-y":
            return dash.no_update, []

        return dash.no_update, dash.no_update


def add_vtk_mange_callback(app: dash.Dash, grid_manager: GridManager):
    # Callback для отображения выбранного значения
    @app.callback(
        [
            Output('apply-filters', 'disabled'),
            Output('apply-filters-loader', 'children'),
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
            State('stored-token', 'data'),
            State("dropdown-preset", "value"),
            State("scale-factor", "value"),
            State("dropdown-property", "value"),
            State("x-slices", "value"),
            State("y-slices", "value"),
            State("toggle-cube-axes", "value"),
            State("toggle-edge-visibility", "value")
        ],
    )
    def update_vtk(n_clicks, token, preset, scale_factor, prop, x_slices, y_slices, cube_axes, edge_visibility):
        # Обновление данных только после нажатия кнопки "Применить"
        if n_clicks is None:
            raise dash.exceptions.PreventUpdate

        points, polys, elevation, color_range = [], None, None, []
        try:
            points, polys, elevation, color_range = grid_manager.update_grid_geometry(
                property_name=prop,
                scalar=scale_factor,
                slice_x=x_slices,
                slice_y=y_slices,
                token=token
            )
        except Exception as e:
            print(e)
            print(e.with_traceback())
            pass

        return [
            False,
            False,
            "grid" in cube_axes,
            preset,
            color_range,
            {"edgeVisibility": "edges" in edge_visibility},
            points,
            polys,
            elevation,
            random.random(),
        ]

    # Callback для блокировки кнопки во время выполнения

    @app.callback(
        [
            Output('apply-filters', 'disabled', allow_duplicate=True)
        ],
        [
            Input('apply-filters', 'n_clicks')
        ],
        prevent_initial_call=True,
    )
    def disable_button(n_clicks):
        print('asdasdasd')
        return [True]
