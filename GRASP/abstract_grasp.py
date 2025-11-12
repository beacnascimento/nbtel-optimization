# abstract_grasp.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
import random, math

from .solution import Solution

E = TypeVar("E")

class AbstractGRASP(ABC, Generic[E]):
    verbose: bool = True
    rng = random.Random(0)

    def __init__(self, obj_function, alpha: float, iterations: int):
        """
        obj_function deve expor:
          - evaluate(sol) -> float (atualiza sol.cost)
          - evaluate_insertion_cost(elem, sol) -> float (delta de custo)
          - evaluate_removal_cost(elem, sol) -> float
          - evaluate_exchange_cost(elem_in, elem_out, sol) -> float
        """
        self.ObjFunction = obj_function
        self.alpha = float(alpha)
        self.iterations = int(iterations)

        self.bestCost = math.inf
        self.cost = math.inf

        self.bestSol: Solution[E] = None
        self.sol: Solution[E] = None

        self.CL: List[E] = []
        self.RCL: List[E] = []

    # ganchos a implementar
    @abstractmethod
    def makeCL(self) -> List[E]: ...
    @abstractmethod
    def makeRCL(self) -> List[E]: ...
    @abstractmethod
    def updateCL(self) -> None: ...
    @abstractmethod
    def createEmptySol(self) -> Solution[E]: ...
    @abstractmethod
    def localSearch(self) -> Solution[E]: ...
    @abstractmethod
    def copy_solution(self, sol: Solution[E]) -> Solution[E]: ...

    # construtivo (minimização)
    def constructiveHeuristic(self) -> Solution[E]:
        self.CL = self.makeCL()
        self.RCL = self.makeRCL()
        self.sol = self.createEmptySol()
        self.cost = math.inf

        while not self.constructiveStopCriteria():
            maxCost = -math.inf
            minCost = math.inf

            self.cost = self.ObjFunction.evaluate(self.sol)
            self.updateCL()
            if not self.CL:
                break

            # varredura para min/max delta
            for c in self.CL:
                delta = self.ObjFunction.evaluate_insertion_cost(c, self.sol)
                if delta < minCost: minCost = delta
                if delta > maxCost: maxCost = delta

            # monta RCL: delta <= min + alpha*(max-min)
            self.RCL.clear()
            thr = minCost + self.alpha * (maxCost - minCost)
            for c in self.CL:
                if self.ObjFunction.evaluate_insertion_cost(c, self.sol) <= thr:
                    self.RCL.append(c)

            if not self.RCL: break
            inCand = self.rng.choice(self.RCL)
            self.CL.remove(inCand)
            self.sol.append(inCand)
            self.ObjFunction.evaluate(self.sol)
            self.RCL.clear()

        return self.sol

    # loop principal
    def solve(self) -> Solution[E]:
        self.bestSol = self.createEmptySol()
        self.bestCost = self.bestSol.cost
        for it in range(self.iterations):
            self.constructiveHeuristic()
            self.localSearch()
            if self.sol.cost < self.bestCost:
                self.bestSol = self.copy_solution(self.sol)
                self.bestCost = self.bestSol.cost
                if AbstractGRASP.verbose:
                    print(f"(Iter. {it}) BestSol = {self.bestSol}")
        return self.bestSol

    # mesmo critério do Java
    def constructiveStopCriteria(self) -> bool:
        return False if (self.cost > getattr(self.sol, "cost", math.inf)) else True
