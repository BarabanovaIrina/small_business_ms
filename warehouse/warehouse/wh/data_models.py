from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class ProductData:
    id: int
    name: str
    description: str
    country_of_origin: str
    price: float = 0.0
    quantity: int = 0

    def dict(self) -> Dict:
        return {k: v for k, v in asdict(self).items()}
