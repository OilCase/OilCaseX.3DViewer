import os
import shutil
import time
from typing import Optional, Callable


class CacheHtml:
    def __init__(self, cache_dir: str, object_limit: int = 100, life_time_object_sec: int = 60 * 60 * 5):
        if os.path.isdir(cache_dir):
            shutil.rmtree(cache_dir)

        self.cache_dir = cache_dir
        self.life_time_object_seconds = life_time_object_sec
        self.object_limit = object_limit

        self.data_dict: dict = {"example": {
            "time": 0,  # время добавления в секундах
            "data_path": {"data data"}
        }}

    def get_or_set(self, name: str, f: Callable[[], str]) -> Optional[str]:
        cache_path = self.get(name)

        if cache_path is None:
            cache_path = f()
            self.set(name, cache_path)

        return cache_path

    def get(self, name: str) -> Optional[str]:
        if len(self.data_dict) > self.object_limit:
            remove_save_count = 2

            func_sort = lambda cache_item_name: self.data_dict[cache_item_name]['time']
            for c_item_name in sorted(self.data_dict.keys(), key=func_sort)[remove_save_count:]:
                self.remove(c_item_name)

        html_data = self.data_dict.get(name)
        if html_data is None:
            return None

        print(time.time() - html_data['time'] <= self.life_time_object_seconds, time.time(), html_data['time'],
              self.life_time_object_seconds)
        if time.time() - html_data['time'] <= self.life_time_object_seconds:
            if os.path.isfile(html_data['data_path']):
                html_data['time'] = time.time()
                return html_data['data_path']

        self.remove(name)
        return None

    def remove(self, name: str):
        os.remove(self.data_dict[name]['data_path'])
        self.data_dict.pop(name)

    def set(self, name: str, path: str):
        self.data_dict[name] = {
            "time": time.time(),
            "data_path": path
        }
