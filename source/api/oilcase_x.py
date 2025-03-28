from dataclasses import dataclass
from datetime import date
import os
import tempfile
from typing import List, Optional, Tuple
from urllib.parse import urljoin
import zipfile

import requests

from utils.create_vtp import create_vtp
from utils.get_property import get_property_from_unrst
from utils.retry import retry_with_timeout


@dataclass
class AvailableDatesDTO():
    Date: date
    OrderNumber: int
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

    @retry_with_timeout(max_retries=3, timeout=10)
    def get(self, token: str, sub_url: str) -> requests.Response:
        full_url = urljoin(self.BaseUrl, sub_url)
        response = requests.get(full_url, headers=self.headers(token))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response

    @retry_with_timeout(max_retries=3, timeout=10)
    def post(self, token: str, sub_url: str, data: dict) -> requests.Response:
        full_url = urljoin(self.BaseUrl, sub_url)
        response = requests.post(full_url, headers=self.headers(token), json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response

    @retry_with_timeout(max_retries=3, timeout=20)
    def upload_files(self, token: str, sub_url: str, file_info: List[Tuple[str, str]]):
        """
            files: List[(str file_key, str file_path)]
        """

        files = {}
        try:
            for file_key, file_path in file_info:
                with open(file_path, 'rb') as f:
                    files[file_key] = (
                        os.path.basename(file_path),
                        f,
                        'multipart/form-data'
                    )

            full_url = urljoin(self.BaseUrl, sub_url)

            response = requests.post(full_url, headers=self.headers(token), files=files)
            response.raise_for_status()
            
            return response
        finally:
            # Ensure files are properly closed
            for file_data in files.values():
                if hasattr(file_data[1], 'close'):
                    file_data[1].close()

    def get_all_properties(self, token) -> List[FieldPropertyDTO]:
        data = self.get(token, 'Api/V1/Purchased/ModelProperty')

        data_content = [
            FieldPropertyDTO(
                f['fieldPropertyId'],
                f['fieldPropertyName'],
                f['isDynamic'],
                f['hdmName'],
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
        if info.VTPFileLink is not None:
            self.download_vtp_vtu_file(
                info.VTPFileLink, vtp_path,
                info.VTPFileLink, vtu_path
            )

        if not os.path.isfile(vtp_path):
            with tempfile.TemporaryDirectory() as tmp_properties_directory:
                self.download_hdm_archive(
                    info.HDMProjectArchiveLink, tmp_properties_directory)

                props = self.get_all_properties(token)
                static_props = [
                    p.HDMName for p in props if p.IsDynamic is False]

                create_vtp(os.path.join(
                    f'{tmp_properties_directory}', 'INCLUDE'), vtp_path, static_props)
                self.upload_vtp_vtu_file(token, vtp_path, vtu_path)

        return (info.ModelXSize, info.ModelYSize, info.ModelZSize)

    def get_dynamic_props(self, token: str, property_name: str, step=0) -> List[float]:
        info = self.get_hdm_info(token)
        with tempfile.NamedTemporaryFile('w+') as temp_file:
            self.download_unrst_file(info.UnrstLink, temp_file.name)
            data = get_property_from_unrst(temp_file.name, property_name, step)

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

    @retry_with_timeout(max_retries=3, timeout=120)
    def download_hdm_archive(self, link: str, directory: str):
        response = requests.get(link)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile('wb') as zip_archive:
            zip_archive.write(response.content)
            with zipfile.ZipFile(zip_archive.name, 'r') as zip_ref:
                zip_ref.extractall(directory)

    @retry_with_timeout(max_retries=3, timeout=60)
    def download_vtp_vtu_file(self,
                              vtp_link: str,
                              vtp_path: str,
                              vtu_link: str,
                              vtu_path: str
                              ):
        self.save_file(vtp_link, vtp_path)
        self.save_file(vtu_link, vtu_path)

    def upload_vtp_vtu_file(self, token: str, vtp_path: str, vtu_path: str):
        self.upload_files(token, 'Api/V1/Info/HDM/UploadVtpVtu',
                          [('vtp', vtp_path), ('vtu', vtu_path)])

    @retry_with_timeout(max_retries=3, timeout=60)
    def download_unrst_file(self, unrst_link: str, unrst_path: str):
        self.save_file(unrst_link, unrst_path)

    @retry_with_timeout(max_retries=3, timeout=30)
    def save_file(self, link: str, path: str):
        with open(path, "wb") as file:
            response = requests.get(link)
            response.raise_for_status()
            file.write(response.content)

