from typing import List
from ecl.eclfile import EclFile


def get_property(unrst_path, property_name, step = 0) -> List[float]:
    try:
        unrst_file = EclFile(unrst_path)
        data = unrst_file[property_name][step]
        return list(data)
    except Exception as e:
        print(e)
    return []