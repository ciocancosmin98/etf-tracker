from abc import ABC, abstractmethod
from typing import List, Tuple
import datetime
import requests

import sys
sys.path.append('..')

from utils.types import EtfPoint

class EtfHttpSource(ABC):

    def __init__(self, urlMappings: dict[str, str]):
        self.urlMapping = urlMappings

    @abstractmethod
    def createPoint(self, item: dict[str, str]):
        pass

    def get(self, etfName: str) -> List[EtfPoint]:
        url: str = self.urlMapping[etfName]
        
        items: List[dict[str, str]] = requests.get(url).json()

        return list(map(self.createPoint, items))

class BrdHttpSource(EtfHttpSource):

    def createPoint(self, item: dict[str, str]):
        price = float(item['vuan'])
        date = item['data'].split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])

        return EtfPoint(price, datetime.date(year, month, day))

    def __init__(self):
        idMappings = {
            'GLOBAL_E': '10',
            'GLOBAL_A': '6'
        }

        urlMappings = {
            name : 'https://www.brdam.ro/fdata/graph/{0}/all'.format(idMappings[name]) for name in idMappings
        }

        super().__init__(urlMappings)

class AllianzHttpSource(EtfHttpSource):

    def createPoint(self, item: dict[str, str]):
        price = float(item['FundPrice'])
        date = (item['Date'].split('T')[0]).split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        
        return EtfPoint(price, datetime.date(year, month, day))

    def __init__(self):
        idMappings = {
            'EUROPE_EQUITY': '27',
            'WORLD_EQUITY': '26',
            'LEU_SIMPLU': '15'
        }

        urlMappings = {
            name: 'https://mobil.allianztiriac.ro/api/financial/investmentfund/{0}?since=1900-01-01&until=2100-01-01'.format(idMappings[name]) for name in idMappings
        }

        super().__init__(urlMappings)