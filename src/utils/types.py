from dataclasses import dataclass
import datetime
from typing import List, Tuple

@dataclass
class EtfPoint:
    price: float
    date: datetime.date = datetime.date(1900, 1, 1)

@dataclass
class EtfPlotInfo:
    name: str
    prices: List[float]