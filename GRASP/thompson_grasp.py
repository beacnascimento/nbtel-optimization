# thompson_grasp.py  (versão com busca local 2.6.3)

import math, random, time
from typing import List, Tuple, Dict
from .abstract_grasp import AbstractGRASP
from .solution import Solution
from .thompson_evaluator import ThompsonEvaluator, ELEM
from .thompson_instance import ThompsonInstance


class ThompsonGrasp(AbstractGRASP[ELEM]):
    """
    Concreto do AbstractGRASP para Thompson.
    Elemento = (empregado, (day, sid))

    construction:
      - 'traditional'          -> usa o construtivo do AbstractGRASP (RCL por threshold de alpha)
      - 'random_plus_greedy'   -> fase aleatória inicial + fase gananciosa
      - 'reactive'             -> Reactive GRASP (alpha escolhido adaptativamente)
    """

    def __init__(
        self,
        instance: ThompsonInstance,
        alpha: float,
        iterations: int,
        construction: str = 'traditional',
        random_p: float = 0.2,
        reactive_cfg: Dict = None
    ):
        super().__init__(ThompsonEvaluator(instance), alpha, iterations)
        self.I = instance
        self.construction = construction
        self.random_p = float(random_p)
        self.reactive_cfg = reactive_cfg or {
            "alphas": [0.0, 0.15, 0.3, 0.5, 0.7, 0.9],
            "block_size": 20,
            "min_prob": 0.05,
            # 'seed' opcional
        }

        # candidatos base (ES)
        self.all_candidates: List[ELEM] = sorted(
            list(self.I.ES),
            key=lambda t: (t[1][0], t[1][1], self.I.pos[t[0]])
        )

        # ordem dos turnos por “dificuldade”
        self.cand_by_shift = {s: [e for e in self.I.E if (e, s) in self.I.ES] for s in self.I.S}
        self.build_order = sorted(
            self.I.S, key=lambda s: (len(self.cand_by_shift[s]), self.I.TT_s[s], self.I.ST_s[s])
        )

        # RNG próprio para a classe
        self._rng = random.Random(self.reactive_cfg.get("seed", 0))

    # ====== ganchos obrigatórios (do AbstractGRASP) ======
    def makeCL(self) -> List[ELEM]:
        # Para o construtivo 'traditional' do AbstractGRASP:
        ordered = []
        for s in self.build_order:
            ordered.extend([(e, s) for e in self.cand_by_shift[s]])
        return ordered

    def makeRCL(self) -> List[ELEM]:
        return []

    def updateCL(self) -> None:
        feasible = []
        for elem in self.CL:
            d = self.ObjFunction.evaluate_insertion_cost(elem, self.sol)
            if d != float('inf'):
                feasible.append(elem)
        self.CL = feasible

    def createEmptySol(self):
        # NUNCA retorne None aqui
        return Solution([])  # iterável e com cost=+inf por padrão

    def copy_solution(self, sol: Solution[ELEM]) -> Solution[ELEM]:
        return sol.copy()

    # =========================================================================
    # --------- FUNÇÕES DE SUPORTE À BUSCA LOCAL (lexicográfica) --------------
    # =========================================================================
    def _lex_tuple(self, sol: Solution[ELEM]) -> Tuple[float, ...]:
        """
        Assinatura lexicográfica:
          (#não-cobertos, diss[E_0], diss[E_1], ..., diss[E_n])
        E_0 é o mais sênior.
        """
        self.ObjFunction.evaluate(sol)  # atualiza estados: unalloc, diss[.]
        v = [self.ObjFunction.unalloc]
        for e in self.I.E:
            v.append(self.ObjFunction.diss[e])
        return tuple(v)

    # ================= Vizinhança 1: Seniority-Swap (first-improvement) =================
    def _first_improvement_seniority_swap(self, sol: Solution[ELEM]) -> bool:
        """
        Troca (e_sênior, s_sênior) <-> (e_júnior, s_júnior)
        Aceita se:
          - e_sênior é elegível a s_júnior e e_júnior é elegível a s_sênior (e respeita 1 por dia);
          - a insatisfação do e_sênior DIMINUI;
          - e a assinatura lexicográfica da solução NÃO PIORA (<=).
        Estratégia: first-improvement.
        """
        base_sig = self._lex_tuple(sol)

        # mapa empregado -> lista de turnos atribuídos
        by_emp: Dict[str, List[Tuple[str, int]]] = {e: [] for e in self.I.E}
        for (e, s) in sol:
            by_emp[e].append(s)

        # percorre pares (sênior, júnior)
        for i, e_sen in enumerate(self.I.E):
            for j in range(i + 1, len(self.I.E)):
                e_jun = self.I.E[j]
                if not by_emp[e_sen] or not by_emp[e_jun]:
                    continue

                for s_sen in by_emp[e_sen]:
                    for s_jun in by_emp[e_jun]:
                        # elegibilidade básica
                        if (e_sen, s_jun) not in self.I.ES or (e_jun, s_sen) not in self.I.ES:
                            continue

                        # respeitar "1 por dia" (permitindo trocar o mesmo s)
                        self.ObjFunction._recompute_state(sol)
                        if s_sen != s_jun:
                            if self.I.day_of[s_jun] in self.ObjFunction.used_day[e_sen]:
                                continue
                            if self.I.day_of[s_sen] in self.ObjFunction.used_day[e_jun]:
                                continue

                        # aplicar troca
                        tmp = sol.copy()
                        tmp.remove((e_sen, s_sen))
                        tmp.remove((e_jun, s_jun))
                        tmp.append((e_sen, s_jun))
                        tmp.append((e_jun, s_sen))

                        # condição: sênior melhora sua diss e solução não piora lexicograficamente
                        self.ObjFunction._recompute_state(sol)
                        diss_sen_before = self.ObjFunction.diss[e_sen]
                        self.ObjFunction._recompute_state(tmp)
                        diss_sen_after = self.ObjFunction.diss[e_sen]

                        if not (diss_sen_after < diss_sen_before):
                            continue

                        new_sig = self._lex_tuple(tmp)
                        if new_sig <= base_sig:
                            sol.clear()
                            sol.extend(tmp)
                            self.ObjFunction.evaluate(sol)
                            return True

        return False

    # ======== Vizinhança 2: Uncovered-Shift-Relocation (first-improvement) ========
    def _first_improvement_uncovered_relocation(self, sol: Solution[ELEM]) -> bool:
        """
        Para cada turno descoberto, tenta alocar ao menos sênior possível,
        aceitando somente se a assinatura lexicográfica MELHORAR (<).
        Estratégia: first-improvement.
        """
        base_sig = self._lex_tuple(sol)
        self.ObjFunction._recompute_state(sol)

        # turnos ainda não cobertos
        uncovered = [s for s in self.I.S if self.ObjFunction.assign[s] is None]
        if not uncovered:
            return False

        for s in uncovered:
            # percorre do menos sênior para o mais sênior (preservar flexibilidade dos sêniores)
            for e in reversed(self.I.E):
                # elegibilidade + restrições locais
                if (e, s) not in self.I.ES:
                    continue
                self.ObjFunction._recompute_state(sol)
                if self.ObjFunction.count[e] >= self.I.m_e[e]:
                    continue
                if self.I.day_of[s] in self.ObjFunction.used_day[e]:
                    continue

                tmp = sol.copy()
                tmp.append((e, s))
                new_sig = self._lex_tuple(tmp)

                if new_sig < base_sig:  # melhora lexicográfica estrita
                    sol.clear()
                    sol.extend(tmp)
                    self.ObjFunction.evaluate(sol)
                    return True

        return False

    # =============================== BUSCA LOCAL (2.6.3) ===============================
    def localSearch(self) -> Solution[ELEM]:
        """
        Busca local com as vizinhanças:
        - Seniority-Swap
        - Uncovered-Shift-Relocation
        Usa first-improvement até não haver mais melhora.
        """

        # 🔹 segurança: caso self.sol esteja None (erro comum no GRASP base)
        if self.sol is None:
            self.sol = self.createEmptySol()

        # 🔹 também garante que é iterável
        if not isinstance(self.sol, list):
            self.sol = Solution(list(self.sol) if self.sol else [])

        improved = True
        while improved:
            improved = False

            # Seniority-Swap (first improvement)
            try:
                if self._first_improvement_seniority_swap(self.sol):
                    improved = True
                    continue
            except Exception as e:
                print(f"[WARN] Falha em seniority-swap: {e}")

            # Uncovered-Shift-Relocation (first improvement)
            try:
                if self._first_improvement_uncovered_relocation(self.sol):
                    improved = True
                    continue
            except Exception as e:
                print(f"[WARN] Falha em uncovered-relocation: {e}")

        # 🔹 sempre retorna uma Solution válida
        if not isinstance(self.sol, Solution):
            self.sol = Solution(self.sol)

        print("DEBUG >>> tipo sol:", type(self.sol), "conteúdo:", self.sol)

        self.ObjFunction.evaluate(self.sol)
        return self.sol


    # ====== ovveride do construtivo para suportar variantes ======
    def constructiveHeuristic(self) -> Solution[ELEM]:
        if self.construction == 'traditional':
            # usa a implementação do AbstractGRASP (RCL via self.alpha)
            return super().constructiveHeuristic()

        elif self.construction == 'random_plus_greedy':
            return self._constructive_random_plus_greedy(alpha=self.alpha, p=self.random_p)

        elif self.construction == 'reactive':
            # Reactive é gerenciado no solve(); aqui voltamos ao tradicional.
            return super().constructiveHeuristic()

        else:
            # fallback
            return super().constructiveHeuristic()

    # ====== RANDOM + GREEDY ======
    def _constructive_random_plus_greedy(self, alpha: float, p: float) -> Solution[ELEM]:
        sol = self.createEmptySol()

        # Fase 1) escolhe aleatoriamente p*|S| turnos e tenta alocar algo viável (RCL simples por alpha)
        print(f"[DEBUG] Construção Random+Greedy: p={p}, alpha={alpha}")
        
        k = max(1, min(len(self.I.S), int(math.ceil(p * len(self.I.S)))))
        rnd_shifts = self._rng.sample(self.I.S, k)

        for s in rnd_shifts:
            # candidatos viáveis agora (delta finito)
            feas = []
            for e in self.cand_by_shift[s]:
                d = self.ObjFunction.evaluate_insertion_cost((e, s), sol)
                if d != float('inf'):
                    feas.append((e, d))
            if not feas:
                continue
            # RCL por threshold com alpha (lembrando: minimização)
            feas.sort(key=lambda t: t[1])  # d crescente (melhor primeiro)
            dmin, dmax = feas[0][1], feas[-1][1]
            thr = dmin + alpha * (dmax - dmin)
            rcl = [e for (e, d) in feas if d <= thr]
            e_pick = self._rng.choice(rcl)
            sol.append((e_pick, s))
            self.ObjFunction.evaluate(sol)

        # Fase 2) completa de forma gananciosa (melhor ∆)
        for s in self.build_order:
            # se já alocado via fase 1, siga
            already = any(ss == s for (_, ss) in sol)
            if already:
                continue
            best_e, best_d = None, float('inf')
            for e in self.cand_by_shift[s]:
                d = self.ObjFunction.evaluate_insertion_cost((e, s), sol)
                if d < best_d:
                    best_d, best_e = d, e
            if best_e is not None and best_d != float('inf'):
                sol.append((best_e, s))
                self.ObjFunction.evaluate(sol)

        return sol

    # ====== REACTIVE GRASP (override de solve) ======
    def solve(self) -> Solution[ELEM]:
        if self.construction != 'reactive':
            return super().solve()

        # ---- Reactive GRASP params ----
        alphas = list(self.reactive_cfg.get("alphas", [0.0, 0.15, 0.3, 0.5, 0.7, 0.9]))
        m = len(alphas)
        block_size = int(self.reactive_cfg.get("block_size", 20))
        min_prob = float(self.reactive_cfg.get("min_prob", 0.05))

        # dist. inicial uniforme
        probs = [1.0 / m] * m
        rewards = [0.0] * m
        counts = [0] * m

        self.bestSol = self.createEmptySol()
        self.bestCost = self.bestSol.cost

        for it in range(self.iterations):
            # escolhe alpha conforme probs
            idx = self._roulette_choice(probs)
            self.alpha = alphas[idx]

            # constrói + busca local (tradicional com esse alpha)
            self.constructiveHeuristic()
            self.localSearch()

            # custo (menor melhor) → recompensa ~ 1/custo
            cost = self.sol.cost
            if math.isfinite(cost) and cost > 0:
                rew = 1.0 / cost
            else:
                rew = 0.0

            # update estatísticas
            rewards[idx] += rew
            counts[idx] += 1

            # incumbente
            if cost < self.bestCost:
                self.bestSol = self.copy_solution(self.sol)
                self.bestCost = cost
                if AbstractGRASP.verbose:
                    print(f"(Iter. {it}) BestSol = {self.bestSol}")

            # a cada bloco, atualiza probabilidades
            if (it + 1) % block_size == 0:
                # média de recompensa por alpha
                avg = [(rewards[i] / counts[i]) if counts[i] > 0 else 0.0 for i in range(m)]
                # evita tudo zerado
                if sum(avg) <= 0:
                    probs = [1.0 / m] * m
                else:
                    # p_i proporcional à média, com piso min_prob
                    raw = [max(min_prob, a) for a in avg]
                    s = sum(raw)
                    probs = [r / s for r in raw]
                # reseta bloco
                rewards = [0.0] * m
                counts = [0] * m

        return self.bestSol

    # -------- utilitário: roleta discreta --------
    def _roulette_choice(self, probs: List[float]) -> int:
        r = self._rng.random()
        acc = 0.0
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                return i
        return len(probs) - 1

