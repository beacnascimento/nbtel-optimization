# GRASP/solution.py
from typing import Generic, TypeVar, Iterable, List

E = TypeVar("E")

class Solution(List[E], Generic[E]):
    """
    Lista de elementos + custo (minimização).
    Aceita: None, outra Solution, ou qualquer iterável de elementos.
    """
    def __init__(self, iterable: Iterable[E] | "Solution[E]" | None = None,
                 cost: float = float("inf")):
        if isinstance(iterable, Solution):
            # copia elementos e custo de outra Solution
            super().__init__(iterable)
            self.cost: float = iterable.cost
        elif iterable is None:
            super().__init__()
            self.cost: float = cost
        else:
            # iterável comum (ex.: list, tuple, set)
            super().__init__(iterable)
            self.cost: float = cost

    def copy(self) -> "Solution[E]":
        return Solution(self, self.cost)

    def __repr__(self) -> str:
        return f"Solution(cost={self.cost}, size={len(self)}, elements={list(self)})"

    __str__ = __repr__
