
from dataclasses import dataclass
from datetime import date
import os
import shutil
import tempfile
from typing import List, Optional, Tuple
import zipfile

from app.create_vtp import create_vtp
from app.get_property import get_property


@dataclass
class AvailableDatesDTO:
    Date: date
    OrderNUmber: int
    X: List[int]
    Y: List[int]


@dataclass
class AvailablePropertyDTO:
    HDMName: str
    PropertyDescription: str
    AvailableDates: List[AvailableDatesDTO]
    IsDynamic: bool

@dataclass
class HDMInfo:
    UnrstLink: str
    HDMProjectArchiveLink: str
    VTPFileLink: Optional[str]

    ModelXSize: int
    ModelYSize: int
    ModelZSize: int

    MapXSize: int
    MapYSize: int


class OilCaseXApi:
    def __init__(self, base_url):
        self.BaseUrl = base_url

    def get_available_properties(self, token) -> List[AvailablePropertyDTO]:
        availableDate1 = AvailableDatesDTO(
            date(2026, 5, 13),
            0,
            [1, 2, 5, 6, 7],
            [1, 2, 5, 15, 18]
        )
        availableDate2 = AvailableDatesDTO(
            date(2027, 9, 30),
            1,
            [],
            []
        )
        availableDate3 = AvailableDatesDTO(
            date(2028, 12, 30),
            2,
            list(range(0, 23)),
            list(range(0, 17))
        )

        return [
            AvailablePropertyDTO('PRESSURE', 'Пластовое давление',
                                 [availableDate1, availableDate2, availableDate3],
                                 True),

            AvailablePropertyDTO('ROIP', 'Остаточные запасы нефти',
                                 [availableDate1, availableDate2, availableDate3],
                                 True),

            AvailablePropertyDTO('SOIL', 'Нефтенасыщенность',
                                 [availableDate1, availableDate2, availableDate3],
                                 True),

            AvailablePropertyDTO('SGAS', 'Газонасыщенность', [availableDate3], True),

            AvailablePropertyDTO('SWAT', 'Водонасыщенность', [availableDate3], True),

            AvailablePropertyDTO('PORO', 'Пористость', [availableDate3], False),

            AvailablePropertyDTO('PERMX', 'Проницаемость X', [availableDate3], False),

            AvailablePropertyDTO('PERMY', 'Проницаемость Y', [availableDate3], False),

            AvailablePropertyDTO('PERMZ', 'Проницаемость Z', [availableDate3], False),

            AvailablePropertyDTO('SEISMIC', 'Сейсмика', [availableDate1], False),
        ]


    def get_vtp_file(self, token: str, vtp_path: str) -> Tuple[int, int ,int]:
        """
        return nx, ny, nz
        """
        
        info = self.get_hdm_info(token)
        self.download_vtp_file(info.VTPFileLink, vtp_path)

        if not os.path.isfile(vtp_path):
            with tempfile.TemporaryDirectory() as tmp_properties_directory:
                self.download_hdm_archive(info.HDMProjectArchiveLink, tmp_properties_directory)
                
                props = self.get_available_properties(token)
                static_props = [p.HDMName for p in props if p.IsDynamic is False]

                create_vtp(os.path.join(f'{tmp_properties_directory}', 'INCLUDE'), vtp_path, static_props)
                self.upload_vtp_file(info.VTPFileLink, vtp_path)

        return (info.ModelXSize, info.ModelYSize, info.ModelZSize)

    def get_dynamic_props(self, token: str, property_name: str) -> List[float]:
        info = self.get_hdm_info(token)
        with tempfile.NamedTemporaryFile('w+') as temp_file:
            self.upload_unrst_file(info.UnrstLink, temp_file.name)
            data = get_property(temp_file.name, property_name)

        return data

    def get_hdm_info(self, token: str) -> HDMInfo:
        return HDMInfo(
            '',
            '',
            '',
            69,
            50,
            75,
            23,
            17
        )
    
    def download_hdm_archive(self, link: str, directory: str):
        with zipfile.ZipFile('hdm.zip', 'r') as zip_ref:
            zip_ref.extractall(directory)

    def download_vtp_file(self, link: str, file_path: str):
        try:
            shutil.copyfile(r'data/cache/file.vtp', file_path)
            shutil.copyfile(r'data/cache/file.vtu', file_path.replace('vtp', 'vtu'))
        except:
            pass

    def upload_vtp_file(self, link: str, vtp_src: str):
        dir_cache = r'data/cache'
        if not os.path.exists(dir_cache):
            os.mkdir(dir_cache)
            
        vtp_trg = rf'{dir_cache}/file.vtp'
        vtu_trg = rf'{dir_cache}/file.vtu'

        shutil.copyfile(vtp_src, vtp_trg)
        shutil.copyfile(vtp_src.replace('vtp', 'vtu'), vtu_trg)

    def upload_unrst_file(self, link: str, file_path: str):
        shutil.copyfile(r'data/DynamicModel.UNRST', file_path)
