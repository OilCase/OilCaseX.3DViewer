
from dataclasses import dataclass
from typing import List

from app.create_vtp import create_vtp
from app.get_property import get_property


@dataclass
class AvailableLineDTO:
    PropertName: List[int]
    X: List[int]
    Y: List[int]


@dataclass
class AvailablePropertyDTO:
    PropertName: str
    PropertKey: str


class OilCaseXApi:
    def __init__(self, base_url):
        self.BaseUrl = base_url

    def GetAvailableLines(self, token: str) -> List[AvailableLineDTO]:
        return [
            AvailableLineDTO('PORO', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('PERMX', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('PERMY', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SOIL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('TNAVHEAD', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SEQNUM', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('INTEHEAD', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('LOGIHEAD', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('DOUBHEAD', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('IGRP', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('IWEL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SWEL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('XWEL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('ZWEL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('ICON', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SCON', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('XCON', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('TNACTGRD', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('STARTSOL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('PRESSURE', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('RS', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SGAS', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SOIL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('SWAT', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('RFIPOIL', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('RFIPWAT', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('RFIPGAS', list(range(1, 69)), list(range(1, 50))),
            AvailableLineDTO('ENDSOL', list(range(1, 69)), list(range(1, 50)))
        ]

    def GetAvailableProperties(self, token) -> List[AvailablePropertyDTO]:
        return [
            AvailablePropertyDTO('PORO', 'Пористость'),
            AvailablePropertyDTO('PERMX', 'Проницаемость X'),
            AvailablePropertyDTO('PERMY', 'Проницаемость Y'),
            AvailablePropertyDTO('SOIL', "Содержание нефти"),
            AvailablePropertyDTO('TNAVHEAD', 'TNAVHEAD'),
            AvailablePropertyDTO('SEQNUM', 'SEQNUM'),
            AvailablePropertyDTO('INTEHEAD', 'INTEHEAD'),
            AvailablePropertyDTO('LOGIHEAD', 'LOGIHEAD'),
            AvailablePropertyDTO('DOUBHEAD', 'DOUBHEAD'),
            AvailablePropertyDTO('IGRP', 'IGRP'),
            AvailablePropertyDTO('IWEL', 'IWEL'),
            AvailablePropertyDTO('SWEL', 'SWEL'),
            AvailablePropertyDTO('XWEL', 'XWEL'),
            AvailablePropertyDTO('ZWEL', 'ZWEL'),
            AvailablePropertyDTO('ICON', 'ICON'),
            AvailablePropertyDTO('SCON', 'SCON'),
            AvailablePropertyDTO('XCON', 'XCON'),
            AvailablePropertyDTO('TNACTGRD', 'TNACTGRD'),
            AvailablePropertyDTO('STARTSOL', 'STARTSOL'),
            AvailablePropertyDTO('PRESSURE', 'PRESSURE'),
            AvailablePropertyDTO('RS', 'RS'),
            AvailablePropertyDTO('SGAS', 'SGAS'),
            AvailablePropertyDTO('SOIL', 'SOIL'),
            AvailablePropertyDTO('SWAT', 'SWAT'),
            AvailablePropertyDTO('RFIPOIL', 'RFIPOIL'),
            AvailablePropertyDTO('RFIPWAT', 'RFIPWAT'),
            AvailablePropertyDTO('RFIPGAS', 'RFIPGAS'),
            AvailablePropertyDTO('ENDSOL', 'ENDSOL')
        ]

    def GetVtpFile(self, token) -> str:
        print('GetVtpFile')
        directory_path = 'data/INCLUDE'
        grid_name = 'DynamicModel'
        vtp_path = create_vtp(directory_path, grid_name)
        return vtp_path

    def GetProps(self, token, property_name) -> List[float]:
        print('GetProps')
        unrst_path = 'data/DynamicModel.UNRST'
        data = get_property(unrst_path, property_name)
        return data
