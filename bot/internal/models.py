"""Models"""

from typing import List, Optional

from dataclasses import dataclass


@dataclass
class Question():
    """Question model."""

    _id: "str"
    id: int
    title: str
    slug: str
    description: str
    level: str
    topic: List[str]
    success: float
    hint: Optional[str]
    similar: Optional[List[int]]
    date: Optional[str]
