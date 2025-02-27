import os
import shutil
import tempfile
from uuid import uuid1

import pandas as pd
from ecl.summary import EclSum
from ecl.eclfile import EclFile
from ecl.grid import EclGrid


def read_hdm_result(smsspec_path: str, unsmry_path: str) -> pd.DataFrame:
    return EclSum.load(smsspec_path, unsmry_path).pandas_frame().to_dict('dict')


def parse(smspec_file, unsmry_file) -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as temp_dir_path:
        smspec_file_path = os.path.join(temp_dir_path, f"{uuid1()}.smsspec")
        unsmry_file_path = os.path.join(temp_dir_path, f"{uuid1()}.unsmry")

        with open(smspec_file_path, "wb") as buffer:
            shutil.copyfileobj(smspec_file, buffer)

        with open(unsmry_file_path, "wb") as buffer:
            shutil.copyfileobj(unsmry_file, buffer)

        df_json = read_hdm_result(smspec_file_path, unsmry_file_path)
        for k in df_json.keys():
            df_json[k] = [round(float(i),2) for i in list(df_json[k].values())]
        return df_json


def save_prop_from_unrst(grid_file_path, property_file_path, property_name, step, result_file_path, null_value=-9999):
    grid = EclGrid(grid_file_path)
    x = EclFile(property_file_path)[property_name][step]
    z = []

    index = 0
    for i in grid.export_actnum():
        if i:
            z.append(x[index])
            index += 1
        else:
            z.append(null_value)

    os.remove(property_file_path)
    os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
    with open(result_file_path, 'w+') as file:
        file.write(property_name.lower() + '\n' + '\n'.join([str(i) for i in z]) + ' ')