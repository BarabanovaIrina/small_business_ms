from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict


@dataclass
class TransactionData:
    id: int
    order_id: int
    sum: float
    date: datetime

    def dict(self) -> Dict:
        result = {k: v for k, v in asdict(self).items()}
        result["date"] = result["date"].strftime("%d/%m/%Y, %H:%M:%S")
        return result
