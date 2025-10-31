"""适配器包 - 各技能包的适配器实现"""

from .nano_banana_adapter import NanoBananaAdapter
from .minimax_adapter import MinimaxAdapter

__all__ = [
    "NanoBananaAdapter",
    "MinimaxAdapter",
]
