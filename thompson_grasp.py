# thompson_grasp.py
import math
from typing import List, Tuple
from abstract_grasp import AbstractGRASP
from solution import Solution
from thompson_instance import ThompsonInstance
from thompson_evaluator import ThompsonEvaluator, ELEM

class ThompsonGrasp(AbstractGRASP[ELEM]):
    """
    Concreto do AbstractGRASP para Thompson.
    Elemento = (empregado, (day, sid))
    """
    def __init__(self, instance: ThompsonInstance, alpha: float, iterations: int, construction='traditional'):
        super().__init__(ThompsonEvaluator(instance), alpha, iterations)
        self.I = instance
        self.construction = construction

        # candidatos base (ES)
        self.all_candidates: List[ELEM] = sorted(list(self.I.ES), key=lambda t: (t[1][0], t[1][1], self.I.pos[t[0]]))
        # ordem dos turnos por dificuldade (para ajudar no construtivo)
        self.cand_by_shift = {}
        for s in self.I.S:
            self.cand_by_shift[s] = [e for e in self.I.E if (e, s) in self.I.ES]
        self.build_order = sorted(self.I.S, key=lambda s: (len(self.cand_by_shift[s]), self.I.TT_s[s], self.I.ST_s[s]))

    # ====== ganchos obrigatórios ======
    def makeCL(self) -> List[ELEM]:
        # começa pelos pares elegíveis que envolvem os turnos mais “difíceis”
        ordered = []
        for s in self.build_order:
            ordered.extend([(e, s) for e in self.cand_by_shift[s]])
        return ordered

    def makeRCL(self) -> List[ELEM]:
        return []

    def updateCL(self) -> None:
        # mantém apenas os candidatos ainda “inseríveis” (delta finito)
        feasible = []
        for elem in self.CL:
            d = self.ObjFunction.evaluate_insertion_cost(elem, self.sol)
            if d != float('inf'):
                feasible.append(elem)
        self.CL = feasible

    def createEmptySol(self) -> Solution[ELEM]:
        return Solution()

    def copy_solution(self, sol: Solution[ELEM]) -> Solution[ELEM]:
        return sol.copy()

    # ====== busca local simples (best-improve) ======
    def localSearch(self) -> Solution[ELEM]:
        improved = True
        while improved:
            improved = False
            best_delta = 0.0
            best_move = None
            # INSERÇÕES
            for elem in self.all_candidates:
                d = self.ObjFunction.evaluate_insertion_cost(elem, self.sol)
                if d < best_delta:
                    best_delta, best_move = d, ("ins", elem)
            # REMOÇÕES
            for elem in list(self.sol):
                d = self.ObjFunction.evaluate_removal_cost(elem, self.sol)
                if d < best_delta:
                    # só remove se continuar viável (o avaliador já calcula custo; viabilidade é tratada via custo muito grande)
                    best_delta, best_move = d, ("rem", elem)
            # TROCAS
            for elem_in in self.all_candidates:
                for elem_out in list(self.sol):
                    d = self.ObjFunction.evaluate_exchange_cost(elem_in, elem_out, self.sol)
                    if d < best_delta:
                        best_delta, best_move = d, ("ex", (elem_in, elem_out))

            if best_move is not None and best_delta < 0:
                typ = best_move[0]
                if typ == "ins":
                    self.sol.append(best_move[1])
                elif typ == "rem":
                    self.sol.remove(best_move[1])
                else:
                    ei, eo = best_move[1]
                    if eo in self.sol:
                        self.sol.remove(eo)
                        self.sol.append(ei)
                self.ObjFunction.evaluate(self.sol)
                improved = True

        return self.sol
