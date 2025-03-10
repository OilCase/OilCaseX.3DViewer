from typing import List
from ecl.eclfile import EclFile


def get_property_from_unrst(unrst_path, property_name, step = 0) -> List[float]:
    try:
        unrst_file = EclFile(unrst_path)
        
        print("get_property_from_unrst", unrst_file.keys(), step)
        
        data = unrst_file[property_name][step]
        result = list(data)

        print("get_property_from_unrst", len(result))

        return result
    except Exception as e:
        print(e)
    return []