
from dataclasses import dataclass
from datetime import date
import os
import shutil
import tempfile
from typing import List, Optional, Tuple
from urllib.parse import urljoin
import zipfile

import requests

from utils.create_vtp import create_vtp
from utils.get_property import get_property


@dataclass
class AvailableDatesDTO():
    Date: date
    OrderNUmber: int
    X: List[int]
    Y: List[int]


@dataclass
class AvailablePropertyDTO():
    HDMName: str
    PropertyDescription: str
    IsDynamic: bool
    AvailableDates: List[AvailableDatesDTO]

@dataclass
class FieldPropertyDTO():
    FieldPropertyId: int
    FieldPropertyName: str
    IsDynamic: bool
    HDMName: str


@dataclass
class HDMInfo():
    UnrstLink: str
    HDMProjectArchiveLink: str
    VTPFileLink: Optional[str]
    VTUFileLink: Optional[str]

    ModelXSize: int
    ModelYSize: int
    ModelZSize: int

    MapXSize: int
    MapYSize: int


class OilCaseXApi:
    def __init__(self, base_url):
       self.BaseUrl = base_url

    def headers(self, token: str):
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get(self, token: str, sub_url: str):
        full_url = urljoin(self.BaseUrl, sub_url)
        response = requests.get(full_url, headers=self.headers(token))
        return response

    def post(self, token: str, sub_url: str, data: dict):
        full_url = urljoin(self.BaseUrl, sub_url)
        response = requests.post(
            full_url, headers=self.headers(token), json=data)

        return response

    def upload_files(self, token: str, sub_url: str, file_info: List[Tuple[str, str]]):
        """
            files: List[(str file_key, str file_path)]
        """

        files = {file_key: (os.path.basename(file_path), open(
            file_path, 'rb'), 'multipart/form-data') for (file_key, file_path) in file_info}

        full_url = urljoin(self.BaseUrl, sub_url)
        response = requests.post(
            full_url, headers=self.headers(token), files=files)
        return response
    
    def get_all_properties(self, token) -> List[AvailablePropertyDTO]:
        data = self.get(token, 'Api/V1/Purchased/ModelProperty')

        data_content = [
            AvailablePropertyDTO(
                f['fieldPropertyId'],
                f['fieldPropertyName'],
                f['isDynamic'],
                f['HDMName'],
            )
            for f in data.json()]
        
        return data_content
   

    def get_available_properties(self, token) -> List[AvailablePropertyDTO]:
        data = self.get(token, 'Api/V1/Purchased/ModelProperty/Available')
        json_data = data.json()
        data_content = [
            AvailablePropertyDTO(
                f['hdmName'],
                f['propertyDescription'],
                f['isDynamic'],
                [
                    AvailableDatesDTO(
                        d['date'],
                        d['orderNumber'],
                        d['x'],
                        d['y'],
                    )
                    for d in f['availableDates']
                ]
            )
            for f in json_data]
        return data_content
  

    def get_vtp_vtu_file(self, token: str, vtp_path: str, vtu_path) -> Tuple[int, int, int]:
        """
        return nx, ny, nz
        """

        info = self.get_hdm_info(token)
        if (info.VTPFileLink is not None):
            self.download_vtp_file(info.VTPFileLink, vtp_path,
                                info.VTPFileLink, vtu_path)

        if not os.path.isfile(vtp_path):
            with tempfile.TemporaryDirectory() as tmp_properties_directory:
                self.download_hdm_archive(
                    info.HDMProjectArchiveLink, tmp_properties_directory)

                props = self.get_all_properties(token)
                static_props = [p.HDMName for p in props if p.IsDynamic is False]

                create_vtp(os.path.join(f'{tmp_properties_directory}', 'INCLUDE'), vtp_path, static_props)
                self.upload_vtp_file(info.VTPFileLink, vtp_path)

        return (info.ModelXSize, info.ModelYSize, info.ModelZSize)

    def get_dynamic_props(self, token: str, property_name: str) -> List[float]:
        info = self.get_hdm_info(token)
        with tempfile.NamedTemporaryFile('w+') as temp_file:
            self.download_unrst_file(info.UnrstLink, temp_file.name)
            data = get_property(temp_file.name, property_name)

        return data

    def get_hdm_info(self, token: str) -> HDMInfo:
        hdm_info_data = self.get(token, 'Api/V1/Info/HDM').json()
        hdm_info = HDMInfo(
            hdm_info_data['unrstLink'],
            hdm_info_data['hdmProjectArchiveLink'],
            hdm_info_data['vtpFileLink'],
            hdm_info_data['vtuFileLink'],
            hdm_info_data['modelXSize'],
            hdm_info_data['modelYSize'],
            hdm_info_data['modelZSize'],
            hdm_info_data['mapXSize'],
            hdm_info_data['mapYSize'],
            )

        return hdm_info

    def download_hdm_archive(self, link: str, directory: str):
        response = requests.get(link)
        with tempfile.NamedTemporaryFile('wb') as zip_archive:
            zip_archive.write(response.content)
            with zipfile.ZipFile(zip_archive.name, 'r') as zip_ref:
                zip_ref.extractall(directory)

    def download_vtp_file(self,
                          vtp_link: str,
                          vtp_path: str,
                          vtu_link: str,
                          vtu_path: str
                          ):
      
        
        with open(vtp_path, "wb") as file:
            response = requests.get(vtp_link)
            file.write(response.content)

        with open(vtu_path, "wb") as file:
            response = requests.get(vtu_link)
            file.write(response.content)

    def upload_vtp_file(self, token: str, vtp_path: str, vtu_path: str):
        self.upload_files(token, 'Api/V1/Info/HDM/UploadVtpVtu',
                          [('vtp', vtp_path), ('vtu', vtu_path)])

    def download_unrst_file(self, unrst_link: str, unrst_path: str):
        with open(unrst_path, "wb") as file:
            response = requests.get(unrst_link)
            file.write(response.content)
