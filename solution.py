# solution.py
from typing import Generic, TypeVar, List

E = TypeVar("E")

class Solution(List[E], Generic[E]):
    """
    Versão Python da Solution<E> (Java):
    - herda de list[E]
    - guarda o custo atual (minimização)
    """
    def __init__(self, sol: 'Solution[E]' = None):
        if sol is not None:
            super().__init__(sol)
            self.cost: float = sol.cost
        else:
            super().__init__()
            self.cost: float = float('inf')

    def __str__(self) -> str:
        return f"Solution: cost=[{self.cost}], size=[{len(self)}], elements={list(self)}"

    def copy(self) -> 'Solution[E]':
        return Solution(self)
