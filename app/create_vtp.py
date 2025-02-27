import os
import numpy as np
from utils.PyGRDECL.GRDECL2VTK import GeologyModel


def create_vtp(directory_path, grid_name) -> str:
    print('create_vtp', directory_path, grid_name)

    file_name = ["_GRID", "_ACTNUM", "_PORO", "_PERMX"]
    grid_file_path = directory_path + "/" + "temporary.GRDECL"
    print('grid_file_path')

    with open(grid_file_path, 'w') as outfile:
        for fname in file_name:
            with open(directory_path + "/" + grid_name + fname + ".inc") as infile:
                outfile.write(infile.read().replace('NOECHO', ''))
                infile.close()

        with open(directory_path + "/" + grid_name + ".GRDECL") as infile:
            outfile.write(infile.read().replace('NOECHO', ''))
            infile.close()

        outfile.close()

    print('GeologyModel', directory_path, grid_name)

    model = GeologyModel(filename=grid_file_path)

    mask = np.where(model.GRDECL_Data.SpatialDatas['PORO'] == 0)
    model.GRDECL_Data.SpatialDatas['ACTNUM'][mask] = 0

    model.GRDECL2VTK()

    vtp_path = os.path.join('data/3d_objects', f'grid.vtp')
    model.Write2VTP(vtp_path)
    return vtp_path

    # os.remove(grid_file_path)

    # NX, NY, NZ = model.GRDECL_Data.NX, model.GRDECL_Data.NY, model.GRDECL_Data.NZ
    # properties = list(model.GRDECL_Data.SpatialDatas.keys())

    # return vtp_path
