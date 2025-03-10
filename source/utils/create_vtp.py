from glob import glob as find_files
from os.path import join as join_path
from tempfile import NamedTemporaryFile
from typing import List, Tuple

import numpy as np
from utils.PyGRDECL.GRDECL2VTK import GeologyModel


def create_vtp(property_direcotry, vtp_path:str, prop_names: List[str]) -> Tuple[int, int, int]:
    files_are_nedded = [
        "GRID.inc",
        "ACTNUM.inc",
        '.grdecl',
        *prop_names
    ]

    with NamedTemporaryFile('w+') as outfile:
        for file_name in files_are_nedded:
            print(file_name)
            file_path = find_files(join_path(property_direcotry, f'*{file_name}*'))[0]

            with open(file_path) as infile:
                outfile.write(infile.read().replace('NOECHO', ''))
        
        model = GeologyModel(filename=outfile.name)
        
        mask = np.where(model.GRDECL_Data.SpatialDatas['PORO'] == 0)
        model.GRDECL_Data.SpatialDatas['ACTNUM'][mask] = 0

        model.GRDECL2VTK()
        model.Write2VTP(vtp_path)
        
        return model.GRDECL_Data.NX, model.GRDECL_Data.NY, model.GRDECL_Data.NZ
