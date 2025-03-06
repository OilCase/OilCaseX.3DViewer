import math
import os
from random import random
from typing import Any, List, Optional

from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pyvista as pv

from app.api import *


class GridManager():
    def __init__(self):
        url = 'https://x.oil-case.online'
        self.api = OilCaseXApi(url)

    def get_available_date_lines(self, token: str, target_property: str, order_number: int) -> Optional[AvailableDatesDTO]:
        print('GetAvailableDateLines', token, target_property, order_number)

        available_properties = [p for p in self.api.get_available_properties(
            token) if p.HDMName == target_property]

        if len(available_properties) == 0:
            return None

        available_property = available_properties[0]

        available_dates = [
            d for d in available_property.AvailableDates if d.OrderNUmber == order_number
        ]
        available_date = available_dates[0] if available_dates else None

        return available_date

    def get_NX(self, token: str, target_property: str, order_number: date) -> List[int]:
        available_date = self.get_available_date_lines(
            token, target_property, order_number)
        available_lines = available_date.X if available_date else []

        return available_lines

    def get_NY(self, token: str, target_property: str, target_date: date) -> List[int]:
        available_date = self.get_available_date_lines(
            token, target_property, target_date)
        available_lines = available_date.Y if available_date else []

        return available_lines

    def get_available_dates(self, token, target_property) -> List[AvailableDatesDTO]:
        print('GetAvailableDates', token, target_property)

        properties = self.api.get_available_properties(token)
        available_property = [
            p.AvailableDates for p in properties if p.HDMName == target_property
        ]

        available_dates = available_property[0] if available_property else []

        return available_dates

    def get_properties(self, token) -> List[AvailablePropertyDTO]:
        print(token)
        available_properties = self.api.get_available_properties(token)
        return available_properties

    def update_grid_geometry(self, property_name, scalar=20, slice_x=None, slice_y=None, token=None):
        print(token, property_name)

        mesh, nx, ny, nz = self.read_mesh(token)

        mesh.points[:, 2] *= scalar

        # Обрезка по срезам
        actnum_base = mesh["ACTNUM"][::6]

        hdm_info = self.api.get_hdm_info(token)
        size_x = hdm_info.MapXSize
        size_y = hdm_info.MapYSize

        scale_x = nx / size_x
        scale_y = ny / size_y

        scale_slice_x = self.scale_lines(slice_x, scale_x, nx)
        scale_slice_y = self.scale_lines(slice_y, scale_y, ny)

        actnum = actnum_base.reshape((nx, ny, nz), order="F")

        result_actnum = np.zeros_like(actnum)
        result_actnum[scale_slice_x, :, :] = actnum[scale_slice_x, :, :]
        result_actnum[:, scale_slice_y, :] = actnum[:, scale_slice_y, :]
        result_actnum = np.repeat(result_actnum.reshape(-1, order="F"), 6)

        mesh["ACTNUM"] = result_actnum

        ghosts = np.argwhere(mesh["ACTNUM"] == 0)
        mesh = mesh.remove_cells(ghosts)
        points = mesh.points.ravel()
        polys = vtk_to_numpy(mesh.GetPolys().GetData())

        # в mesh находятся статичсекие свойства которы никогда не меняються
        # Если их нет обращаеся в unrst файл
        try:
            result_prop = mesh[property_name][::6]
        except:
            prop_data = self.api.get_dynamic_props(token, property_name)
            prop_data.reverse()

            prop_data_normalize = [
                prop_data.pop() if i else None for i in actnum_base
            ]

            result_prop_full = np.array(
                prop_data_normalize).reshape((nx, ny, nz), order="F")

            result_prop = np.empty_like(result_prop_full)

            result_prop[scale_slice_x, :, :] = result_prop_full[scale_slice_x, :, :]
            result_prop[:, scale_slice_y, :] = result_prop_full[:, scale_slice_y, :]

            result_prop = [i for i in result_prop.reshape(-1, order="F") if i != None]

        elevation = np.repeat(result_prop, 8)

        min_elevation = np.amin(elevation)
        max_elevation = np.amax(elevation)

        return [points, polys, elevation, [min_elevation, max_elevation]]

    def read_mesh(self, token) -> Tuple[Any, int, int, int]:
        model_name = f'{int(random() * 1_000_000)}'

        vtp_path = f'{model_name}.vtp'
        vtu_path = f'{model_name}.vtu'

        nx, ny, nz = self.api.get_vtp_file(token, vtp_path)
        mesh = pv.read(vtp_path).extract_geometry()

        os.remove(vtp_path)
        os.remove(vtu_path)

        return (mesh, nx, ny, nz)

    def scale_lines(self, lines, scale, upper_limit) -> List[int]:
        scale_lines = [list(range(int(line * scale), int((line + 1) * scale))) for line in lines]
        scale_lines = sum(scale_lines, [])
        scale_lines = [l for l in set(scale_lines) if 0 <= l < upper_limit]
        return scale_lines