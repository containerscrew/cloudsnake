from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class SelectorItem:
    id: str
    label: str
    meta: Sequence[str] = ()
