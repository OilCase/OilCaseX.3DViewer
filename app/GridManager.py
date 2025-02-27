import os
import time
from typing import List

from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import pyvista as pv

from app.api import *


class GridManager():
    def __init__(self):
        url = 'https://x.oil-case.online'
        self.api = OilCaseXApi(url)
        pass

    def GetNX(self, token: str, property: str) -> List[int]:
        print('GetNX', token, property)
        available_lines = [l for l in  self.api.GetAvailableLines(token) if l.PropertName == property]

        result = available_lines[0].X if available_lines else []
        return result
        

    def GetNY(self, token: str, property: str) -> List[int]:
        print('GetNY', token, property)
        available_lines = [l for l in  self.api.GetAvailableLines(token) if l.PropertName == property]

        result = available_lines[0].Y if available_lines else []
        return result
        

    def GetProperties(self, token) -> List[AvailablePropertyDTO]:
        print(token)
        available_properties = self.api.GetAvailableProperties(token)
        return available_properties

    def update_grid_geometry(self, prop, scalar=20, slice_x=None, slice_y=None, token=None):
        print(token, prop)

        vtp_path = os.path.join('data/3d_objects', f'grid.vtp')
        if (os.path.exists(vtp_path) is False):
            vtp_path = self.api.GetVtpFile(token)

        nx, ny, nz = 69, 50, 75

        mesh = pv.read(vtp_path).extract_geometry()
        mesh.points[:, 2] *= scalar

        # Обрезка по срезам
        actnum_base = mesh["ACTNUM"][::6]
        
        actnum = actnum_base.reshape((nx, ny, nz), order="F")

        result_actnum = np.zeros_like(actnum)
        result_actnum[slice_x, :, :] = actnum[slice_x, :, :]
        result_actnum[:, slice_y, :] = actnum[:, slice_y, :]
        result_actnum = np.repeat(result_actnum.reshape(-1, order="F"), 6)

        mesh["ACTNUM"] = result_actnum

        ghosts = np.argwhere(mesh["ACTNUM"] == 0)
        mesh = mesh.remove_cells(ghosts)
        points = mesh.points.ravel()
        polys = vtk_to_numpy(mesh.GetPolys().GetData())

        prop_data = self.api.GetProps(token, prop)
        prop_data.reverse()

        prop_data_normalize = [prop_data.pop() if i else None for i in actnum_base]

        result_prop_full = np.array(prop_data_normalize).reshape((nx, ny, nz), order="F")

        result_prop = result_prop_full.copy()
        
        result_prop[:, :, :] = None

        result_prop[slice_x, :, :] = result_prop_full[slice_x, :, :]
        result_prop[:, slice_y, :] = result_prop_full[:, slice_y, :]

        result_prop = [i for i in result_prop.reshape(-1, order="F") if i != None]
        elevation = np.repeat(result_prop, 8)

        min_elevation = np.amin(elevation)
        max_elevation = np.amax(elevation)

        return [points, polys, elevation, [min_elevation, max_elevation]]

