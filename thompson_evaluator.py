# thompson_evaluator.py
from typing import Tuple, List
from solution import Solution
from thompson_instance import ThompsonInstance

ELEM = Tuple[str, Tuple[str,int]]  # (empregado, (day, sid))

class ThompsonEvaluator:
    """
    Avaliador de MINIMIZAÇÃO (custo lexicográfico escalarizado):
      cost = M0*(#não-alocados) + sum_i Mi * diss(e_i)
    onde Mi decresce com a senioridade (e1 mais sênior recebe maior Mi).
    """
    def __init__(self, instance: ThompsonInstance):
        self.I = instance
        self.M0 = 1e9
        self.Mstep = 1e6  # separação entre camadas de empregados

    # ======= infra de estado incremental =======
    def _recompute_state(self, sol: Solution[ELEM]):
        # mapeia atribuição s->e (no máximo 1 por turno)
        self.assign = {s: None for s in self.I.S}
        self.count = {e: 0 for e in self.I.E}
        self.used_day = {e: set() for e in self.I.E}
        self.diss = {e: 0.0 for e in self.I.E}

        for (e, s) in sol:
            if (e, s) not in self.I.ES:  # ignora pares inelegíveis
                continue
            if self.assign[s] is not None:  # já tem alguém: mantém o primeiro e ignora conflito
                continue
            # checa um por dia e limite semanal / senioridade
            if self.I.day_of[s] in self.used_day[e]: 
                continue
            if self.count[e] >= self.I.m_e[e]:
                continue
            if self.count[e] >= 1 and not self._seniority_allows_more(e):
                continue

            self.assign[s] = e
            self.count[e] += 1
            self.used_day[e].add(self.I.day_of[s])
            self.diss[e] += self.I.v_es(e, s)

        self.unalloc = sum(1 for s in self.I.S if self.assign[s] is None)

    def _seniority_allows_more(self, e) -> bool:
        i = self.I.pos[e]
        if self.count[e] == 0: return True
        if i == 0: return True
        prev = self.I.E[i-1]
        return self.count[prev] >= self.I.m_e[prev]

    def _can_insert(self, elem: ELEM, sol: Solution[ELEM]) -> bool:
        e, s = elem
        if (e, s) not in self.I.ES: return False
        self._recompute_state(sol)
        if self.assign[s] is not None and self.assign[s] != e:
            # permitir troca no evaluate_exchange_cost; aqui apenas “inserção pura”
            return False
        if self.I.day_of[s] in self.used_day[e]: return False
        if self.count[e] >= self.I.m_e[e]: return False
        if self.count[e] >= 1 and not self._seniority_allows_more(e): return False
        return True

    # ======= Interface estilo Evaluator (minimização) =======
    def get_domain_size(self) -> int:
        return len(self.I.ES)

    def evaluate(self, sol: Solution[ELEM]) -> float:
        self._recompute_state(sol)
        cost = self.M0 * self.unalloc
        for i, e in enumerate(self.I.E):
            Mi = self.Mstep * (len(self.I.E) - i)  # mais sênior, maior peso
            cost += Mi * self.diss[e]
        sol.cost = cost
        return cost

    def evaluate_insertion_cost(self, elem: ELEM, sol: Solution[ELEM]) -> float:
        if not self._can_insert(elem, sol):
            return float('inf')  # inviável aumentar custo (min)
        before = self.evaluate(sol)
        tmp = sol.copy(); tmp.append(elem)
        after = self.evaluate(tmp)
        return after - before

    def evaluate_removal_cost(self, elem: ELEM, sol: Solution[ELEM]) -> float:
        if elem not in sol:
            return float('inf')
        before = self.evaluate(sol)
        tmp = sol.copy(); tmp.remove(elem)
        after = self.evaluate(tmp)
        return after - before

    def evaluate_exchange_cost(self, elem_in: ELEM, elem_out: ELEM, sol: Solution[ELEM]) -> float:
        # troca (remove out, insere in)
        if elem_out not in sol:
            return float('inf')
        e_in, s_in = elem_in
        # permitir troca de ocupantes do mesmo turno
        before = self.evaluate(sol)
        tmp = sol.copy()
        tmp.remove(elem_out)
        # checa viabilidade pós-remoção pra inserir
        self._recompute_state(tmp)
        # caso s_in esteja ocupado por outro, a remoção acima pode liberar
        if (e_in, s_in) not in self.I.ES: 
            return float('inf')
        if self.I.day_of[s_in] in self.used_day[e_in]: 
            return float('inf')
        if self.count[e_in] >= self.I.m_e[e_in]: 
            return float('inf')
        if self.count[e_in] >= 1:
            i = self.I.pos[e_in]
            if i > 0:
                prev = self.I.E[i-1]
                if self.count[prev] < self.I.m_e[prev]:
                    # ainda não pode passar de 1
                    if self.count[e_in] >= 1:
                        return float('inf')
        tmp.append(elem_in)
        after = self.evaluate(tmp)
        return after - before

    # auxiliar de cobertura (para heurísticas opcionais)
    def evaluate_insertion_delta_coverage(self, elem: ELEM, sol: Solution[ELEM]) -> int:
        e, s = elem
        self._recompute_state(sol)
        if (e, s) not in self.I.ES: return -10**9
        if self.assign[s] is None:
            # cobriria 1 turno a mais?
            if (self.I.day_of[s] in self.used_day[e]): return -10**9
            if self.count[e] >= self.I.m_e[e]: return -10**9
            if self.count[e] >= 1 and not self._seniority_allows_more(e): return -10**9
            return 1
        return 0
