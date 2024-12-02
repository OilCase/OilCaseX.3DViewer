import os
import tempfile
from uuid import uuid1

import numpy as np
import pyvista as pv
import shutil

from utils.PyGRDECL.GRDECL2VTK import GeologyModel

null_value = -9999


def update_file_property(property_name, property_path: str, temp_dir_path: str):
    property_array = []

    with open(property_path, 'r') as file:
        lines = file.read().split('\n')

        is_run = False
        for line in lines:
            if line.lower() == property_name:
                is_run = True

            elif is_run & (line != ''):
                line_value = [v for v in line.split(' ') if v != '']

                for v in line_value:
                    if '*' in v:
                        v_count, v = v.split('*')
                        property_array += [v for _ in range(int(v_count))]
                    else:
                        property_array.append(v)

            else:
                is_run = False

    update_file = f'{temp_dir_path}/{uuid1()}.txt'
    with open(update_file, 'w+') as file:
        file.write(f"{property_name}\n")
        file.write("\n".join(property_array))

    return update_file


def resize_mesh(mesh, x_size, y_size):
    mesh.points[::, 2] = -np.abs(mesh.points[::, 2])

    min_v = min(mesh.points[::, 1])
    max_v = max(mesh.points[::, 1])
    
    mesh.points[::, 1] = mesh.points[::, 1] - min_v
    mesh.points[::, 1] = mesh.points[::, 1] / ((max_v - min_v) / y_size)
    mesh.points[::, 1] = mesh.points[::, 1] * 3

    min_v = min(mesh.points[::, 0])
    max_v = max(mesh.points[::, 0])

    mesh.points[::, 0] = mesh.points[::, 0] - min_v
    mesh.points[::, 0] = mesh.points[::, 0] / ((max_v - min_v) / x_size)
    mesh.points[::, 0] = mesh.points[::, 0] * 3


def cut_cube(model, name_property, x_save_lines, y_save_lines):
    poro_cube = model.GRDECL_Data.SpatialDatas[name_property].reshape(
        (model.GRDECL_Data.NX, model.GRDECL_Data.NY, model.GRDECL_Data.NZ), order='F')
    poro_cube_copy = poro_cube.copy()
    poro_cube[:, :, :] = null_value

    if not x_save_lines and not y_save_lines:
        x = [0, model.GRDECL_Data.NX - 2]
        y = [0, model.GRDECL_Data.NY - 2]
        z = [0, model.GRDECL_Data.NZ - 1]

        poro_cube[x, :, :] = poro_cube_copy[x, :, :]
        poro_cube[:, y, :] = poro_cube_copy[:, y, :]
        poro_cube[:, :, z] = poro_cube_copy[:, :, z]
    else:
        poro_cube[0, 0, 0] = poro_cube_copy[0, 0, 0]
        poro_cube[x_save_lines, :, :] = poro_cube_copy[x_save_lines, :, :]
        poro_cube[:, y_save_lines, :] = poro_cube_copy[:, y_save_lines, :]

    model.GRDECL_Data.SpatialDatas['poro'] = poro_cube.reshape(-1, order='F')


def generate_html(grid_file_path,
                  name_property, property_path, result_html_path=f'{uuid1()}.html',
                  x_save_lines=None, y_save_lines=None):
    with tempfile.TemporaryDirectory() as temp_dir_path:
        name_property = name_property.lower()

        vtp_path = os.path.join(temp_dir_path, f'{uuid1()}.vtp')

        property_update_file_path = update_file_property(name_property, property_path, temp_dir_path)

        model = GeologyModel(filename=grid_file_path)
        model.LoadCellData(varname=name_property, filename=property_update_file_path)

        cut_cube(model, name_property, x_save_lines, y_save_lines)

        model.GRDECL2VTK()
        model.Write2VTP(vtp_path)
        mesh = pv.read(vtp_path)

        ghosts = np.argwhere(mesh[name_property] == null_value)
        mesh = mesh.remove_cells(ghosts)

        resize_mesh(mesh, model.GRDECL_Data.NX, model.GRDECL_Data.NY)
        _ = mesh.plot(off_screen=True, scalars=name_property, show_edges=True, notebook=False)

        plotter = pv.Plotter(notebook=True, off_screen=True)
        plotter.add_mesh(mesh)

        plotter.show_bounds(grid='front', location='outer', all_edges=True)
        plotter.export_html(result_html_path)

    return result_html_path
