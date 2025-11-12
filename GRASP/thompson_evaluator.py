# GRASP/thompson_evaluator.py
from __future__ import annotations
from typing import Tuple, List, Iterable

from .solution import Solution
from .thompson_instance import ThompsonInstance

ELEM = Tuple[str, Tuple[str, int]]  # (empregado, (day, sid))


class ThompsonEvaluator:
    """
    Avaliador de MINIMIZAÇÃO (custo escalarizado em camadas):
        cost = M0*(#não-alocados) + sum_i Mi * diss(e_i)
    onde Mi decresce com a senioridade (E[0] mais sênior => maior Mi).
    Obs.: Este avaliador é usado pelo GRASP; o multiobjetivo preemptivo "real"
    você já tratou no modelo do Gurobi.
    """

    def __init__(self, instance: ThompsonInstance):
        self.I = instance
        # pesos grandes para priorizar cobertura e, depois, sêniores
        self.M0 = 1e9          # prioridade 0: minimizar turnos não alocados
        self.Mstep = 1e6       # separação entre camadas de empregados

        # estados auxiliares (recomputados a cada evaluate)
        self.assign = {}       # s -> e (ou None)
        self.count = {}        # e -> nº turnos
        self.used_day = {}     # e -> {dias já usados}
        self.diss = {}         # e -> soma de v_es
        self.unalloc = 0

    # ===================== helpers robustos =====================

    @staticmethod
    def _as_list(sol: Solution[ELEM] | Iterable[ELEM] | None) -> List[ELEM]:
        """Aceita Solution, iterável comum ou None e devolve lista."""
        return [] if sol is None else list(sol)

    def _recompute_state(self, sol: Solution[ELEM] | Iterable[ELEM] | None) -> None:
        """(Re)constrói os estados auxiliares a partir de `sol`."""
        sol_list = self._as_list(sol)

        # inicializa estados
        self.assign = {s: None for s in self.I.S}
        self.count = {e: 0 for e in self.I.E}
        self.used_day = {e: set() for e in self.I.E}
        self.diss = {e: 0.0 for e in self.I.E}

        for (e, s) in sol_list:
            # ignora pares inelegíveis
            if (e, s) not in self.I.ES:
                continue
            # já coberto por alguém? mantém o primeiro
            if self.assign[s] is not None:
                continue
            # restrições locais: 1 por dia, limite m_e, regra de senioridade
            if self.I.day_of[s] in self.used_day[e]:
                continue
            if self.count[e] >= self.I.m_e[e]:
                continue
            if self.count[e] >= 1 and not self._seniority_allows_more(e):
                continue

            # aplica
            self.assign[s] = e
            self.count[e] += 1
            self.used_day[e].add(self.I.day_of[s])
            self.diss[e] += self.I.v_es(e, s)

        self.unalloc = sum(1 for s in self.I.S if self.assign[s] is None)

    def _seniority_allows_more(self, e: str) -> bool:
        """
        Implementa a regra inspirada nas restrições (6)-(7):
        um menos sênior só pode passar de 1 turno quando o imediatamente
        mais sênior já atingiu seu m_e (ou seja, recebeu tudo que queria).
        """
        i = self.I.pos[e]
        if self.count[e] == 0:
            return True
        if i == 0:  # mais sênior sempre pode
            return True
        prev = self.I.E[i - 1]
        return self.count[prev] >= self.I.m_e[prev]

    def _can_insert(self, elem: ELEM, sol: Solution[ELEM] | Iterable[ELEM] | None) -> bool:
        """Checa viabilidade local de inserir `elem` em `sol`."""
        e, s = elem
        if (e, s) not in self.I.ES:
            return False

        self._recompute_state(sol)

        # turno já ocupado por outrem? (inserção pura não permite)
        if self.assign[s] is not None and self.assign[s] != e:
            return False
        # 1 por dia
        if self.I.day_of[s] in self.used_day[e]:
            return False
        # limite semanal
        if self.count[e] >= self.I.m_e[e]:
            return False
        # regra de senioridade para passar de 1
        if self.count[e] >= 1 and not self._seniority_allows_more(e):
            return False

        return True

    # ===================== interface estilo Evaluator =====================

    def get_domain_size(self) -> int:
        return len(self.I.ES)

    def evaluate(self, sol: Solution[ELEM] | Iterable[ELEM] | None) -> float:
        """Retorna o custo escalarizado; atualiza sol.cost se for Solution."""
        self._recompute_state(sol)

        cost = self.M0 * self.unalloc
        # E[0] (mais sênior) recebe maior peso Mi
        for i, e in enumerate(self.I.E):
            Mi = self.Mstep * (len(self.I.E) - i)
            cost += Mi * self.diss[e]

        if isinstance(sol, Solution):
            sol.cost = cost
        return cost

    def evaluate_insertion_cost(self, elem: ELEM, sol: Solution[ELEM] | Iterable[ELEM] | None) -> float:
        """Delta de custo ao inserir `elem`; +inf se inviável."""
        if not self._can_insert(elem, sol):
            return float("inf")
        before = self.evaluate(sol)
        tmp = Solution(self._as_list(sol))
        tmp.append(elem)
        after = self.evaluate(tmp)
        return after - before

    def evaluate_removal_cost(self, elem: ELEM, sol: Solution[ELEM] | Iterable[ELEM] | None) -> float:
        sol_list = self._as_list(sol)
        if elem not in sol_list:
            return float("inf")
        before = self.evaluate(sol)
        tmp = Solution(x for x in sol_list if x != elem)
        after = self.evaluate(tmp)
        return after - before

    def evaluate_exchange_cost(
        self, elem_in: ELEM, elem_out: ELEM, sol: Solution[ELEM] | Iterable[ELEM] | None
    ) -> float:
        """
        Troca: remove `elem_out`, tenta inserir `elem_in`.
        Permite que a remoção libere um turno antes ocupado.
        """
        sol_list = self._as_list(sol)
        if elem_out not in sol_list:
            return float("inf")

        before = self.evaluate(sol)
        tmp = Solution(x for x in sol_list if x != elem_out)

        # checa viabilidade pós-remoção
        if not self._can_insert(elem_in, tmp):
            return float("inf")

        tmp.append(elem_in)
        after = self.evaluate(tmp)
        return after - before

    # --------- utilitário para heurísticas (cobertura) ---------
    def evaluate_insertion_delta_coverage(
        self, elem: ELEM, sol: Solution[ELEM] | Iterable[ELEM] | None
    ) -> int:
        """Retorna 1 se a inserção cobriria um turno ainda não coberto; 0 caso contrário; -inf se inviável."""
        e, s = elem
        self._recompute_state(sol)

        if (e, s) not in self.I.ES:
            return -10**9
        # se o turno está descoberto e a inserção é viável, aumenta cobertura
        if self.assign[s] is None:
            if self.I.day_of[s] in self.used_day[e]:
                return -10**9
            if self.count[e] >= self.I.m_e[e]:
                return -10**9
            if self.count[e] >= 1 and not self._seniority_allows_more(e):
                return -10**9
            return 1

        return 0
