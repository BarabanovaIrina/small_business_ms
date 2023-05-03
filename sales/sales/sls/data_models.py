from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List


@dataclass
class OrderedItemData:
    id: int
    price: float
    quantity: int = 1

    def dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items()}


@dataclass
class OrderData:
    id: int
    customer_id: int
    date: datetime
    items: List[OrderedItemData]

    def dict(self) -> Dict:
        result = {k: v for k, v in asdict(self).items()}
        result["date"] = result["date"].strftime("%d/%m/%Y, %H:%M:%S")
        return result
