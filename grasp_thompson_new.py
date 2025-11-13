# grasp_thompson.py
# GRASP para Thompson (1997) — versão otimizada:
# - Construção (Fase 1): ordem de senioridade, RCL por limiar g(s)=d_ies
# - Busca local (Fase 2): Seniority-Swap e Uncovered-Shift-Relocation (first-improvement)
# - Estratégias: 'traditional' | 'random_plus_greedy' | 'reactive'
# - Otimizações: pré-cálculo de elegibilidade ordenada, estruturas incrementais e operações in-place

from __future__ import annotations
import random, math, os, time, csv, importlib.util
from dataclasses import dataclass
from typing import Dict, Tuple, List, Set, Optional, NamedTuple

EmpId = str
Day = str
ShiftId = int
Occ = Tuple[Day, ShiftId]

# =========================
# Instância
# =========================
@dataclass
class ThompsonInstance:
    employee_data: Dict[EmpId, dict]
    shift_data: Dict[ShiftId, dict]
    shift_requirements: Dict[Day, List[ShiftId]]
    LAMBDA_LUNCH: float = 0.0
    PENALTY_UNALLOC: float = 1_000_000.0  # p/ logs

    def __post_init__(self):
        self.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        self.S: List[Occ] = [(d, sid) for d, ids in self.shift_requirements.items() for sid in ids]
        self.ST_s  = {(d, sid): self.shift_data[sid]['ST'] for d, sid in self.S}
        self.BL_s  = {(d, sid): self.shift_data[sid]['BL'] for d, sid in self.S}
        self.TT_s  = {(d, sid): self.shift_data[sid]['TT'] for d, sid in self.S}
        self.d_s   = {(d, sid): d for d, sid in self.S}

        def emp_sort(e): return int(e.split('-')[1])
        # E = [E-01, E-02, ...] em ordem de senioridade (E-01 mais sênior)
        self.E: List[EmpId] = sorted(self.employee_data.keys(), key=emp_sort)

        self.ST_e = {e: v['ST'] for e, v in self.employee_data.items()}
        self.LL_e = {e: v['LL'] for e, v in self.employee_data.items()}
        self.ES_e = {e: v['ES'] for e, v in self.employee_data.items()}
        self.LS_e = {e: v['LS'] for e, v in self.employee_data.items()}
        self.Ce_e = {e: set(v['SklTyp']) for e, v in self.employee_data.items()}
        self.m_e  = {e: v['MxWk'] for e, v in self.employee_data.items()}
        self.Un_e = {e: set(v['UnDay']) for e, v in self.employee_data.items()}
        self.De_e = {e: set(self.days) - self.Un_e[e] for e in self.E}

        # elegibilidade + custo individual
        self.ES: Set[Tuple[EmpId, Occ]] = set()
        self.v_es: Dict[Tuple[EmpId, Occ], float] = {}
        for e in self.E:
            for s in self.S:
                if (self.TT_s[s] in self.Ce_e[e]) and (self.d_s[s] in self.De_e[e]):
                    self.ES.add((e, s))
                    self.v_es[(e, s)] = self._diss(e, s)

        infeas = [e for e in self.E if all((e, s) not in self.ES for s in self.S)]
        if infeas:
            raise ValueError(f"Instância inviável: sem candidatos para {infeas}")

        # >>> Otimização: listas elegíveis pré-ordenadas por g(s)=d_ies
        self.eligible_sorted: Dict[EmpId, List[Occ]] = {
            e: sorted([s for s in self.S if (e, s) in self.ES], key=lambda s: self.v_es[(e, s)])
            for e in self.E
        }

    def _diss(self, e: EmpId, s: Occ) -> float:
        ste, sts = self.ST_e[e], self.ST_s[s]
        base = self.ES_e[e]*(ste-sts) if sts < ste else self.LS_e[e]*(sts - ste)
        return float(base + self.LAMBDA_LUNCH * abs(self.BL_s[s] - self.LL_e[e]))

# =========================
# Custo lexicográfico (p/ comparar iterações)
# =========================
class LexCost(NamedTuple):
    # comp = (P0, P1, ..., Pn) em ordem lexicográfica
    # P0 -> nº de turnos não alocados
    # P1 -> insatisfação do empregado mais sênior
    # ...
    comp: Tuple[float, ...]
    # report_value é um escalar tipo "P0 >> Pe", usado como custo da FO para logs
    report_value: float

def lex_cost(I: ThompsonInstance, sol: "ThompsonSolution") -> LexCost:
    n_unalloc = len(sol.unassigned)
    diss = {e: 0.0 for e in I.E}
    for e, shifts in sol.by_emp.items():
        for s in shifts:
            diss[e] += I.v_es[(e, s)]
    # comp = ( #não alocados, diss_E1, diss_E2, ... )
    comp = (float(n_unalloc),) + tuple(diss[e] for e in I.E)
    # escalar tipo "P0 >> Pe" só para debug / FO agregada
    report = n_unalloc*I.PENALTY_UNALLOC + sum(diss.values())
    return LexCost(comp, report)

def lex_better(a: LexCost, b: LexCost) -> bool:
    # comparação estritamente lexicográfica
    return a.comp < b.comp

# =========================
# Solução (mutável) + operações in-place
# =========================
@dataclass
class ThompsonSolution:
    assign: Dict[Occ, Optional[EmpId]]
    load: Dict[EmpId, int]
    used_day: Dict[Tuple[EmpId, Day], bool]
    by_emp: Dict[EmpId, List[Occ]]
    unassigned: Set[Occ]

def empty_solution(I: ThompsonInstance) -> ThompsonSolution:
    assign = {s: None for s in I.S}
    load = {e: 0 for e in I.E}
    used_day = {(e, d): False for e in I.E for d in I.days}
    by_emp = {e: [] for e in I.E}
    unassigned = set(I.S)
    return ThompsonSolution(assign, load, used_day, by_emp, unassigned)

def can_assign(I: ThompsonInstance, sol: ThompsonSolution, e: EmpId, s: Occ) -> bool:
    if sol.assign[s] is not None: return False
    if sol.load[e] >= I.m_e[e]: return False
    if sol.used_day[(e, I.d_s[s])]: return False
    return (e, s) in I.ES

def assign_inplace(I: ThompsonInstance, sol: ThompsonSolution, e: EmpId, s: Occ) -> None:
    sol.assign[s] = e
    sol.load[e] += 1
    d = I.d_s[s]
    sol.used_day[(e, d)] = True
    sol.by_emp[e].append(s)
    sol.unassigned.discard(s)

def can_swap(I: ThompsonInstance, sol: ThompsonSolution, s1: Occ, s2: Occ) -> bool:
    if s1 == s2: return False
    e1, e2 = sol.assign[s1], sol.assign[s2]
    if (e1 is None) or (e2 is None) or (e1 == e2): return False
    if (e1, s2) not in I.ES or (e2, s1) not in I.ES: return False
    d1, d2 = I.d_s[s1], I.d_s[s2]
    if d1 != d2 and (sol.used_day[(e1, d2)] or sol.used_day[(e2, d1)]): return False
    return True

def swap_inplace(I: ThompsonInstance, sol: ThompsonSolution, s1: Occ, s2: Occ) -> None:
    e1, e2 = sol.assign[s1], sol.assign[s2]
    d1, d2 = I.d_s[s1], I.d_s[s2]
    # atualizar used_day
    sol.used_day[(e1, d1)] = False; sol.used_day[(e2, d2)] = False
    sol.used_day[(e2, d1)] = True;  sol.used_day[(e1, d2)] = True
    # atualizar assign
    sol.assign[s1], sol.assign[s2] = e2, e1
    # atualizar by_emp (listas pequenas por empregado)
    sol.by_emp[e1].remove(s1); sol.by_emp[e1].append(s2)
    sol.by_emp[e2].remove(s2); sol.by_emp[e2].append(s1)

# =========================
# Construção – Fase 1 (com RCL de limiar)
# =========================
class Constructor:
    def __init__(self, I: ThompsonInstance):
        self.I = I

    def _meta_turnos(self, e: EmpId, rank: int) -> int:
        """
        Meta de turnos M'_e para a Fase 1.
        Aqui usamos a CAPACIDADE TOTAL m_e[e], para favorecer
        a prioridade 1 da função objetivo (minimizar turnos não alocados).
        """
        return self.I.m_e[e]

    def build(self, alpha: float, rng: random.Random,
              strategy: str = 'traditional', random_p: float = 0.25) -> ThompsonSolution:
        I = self.I
        sol = empty_solution(I)

        # ----------------------------
        # FASE 1: construção principal
        # ----------------------------
        # processa empregados do mais sênior ao menos sênior,
        # atribuindo até a meta M'_e = m_e[e]
        for rank, e in enumerate(I.E):  # mais sênior -> menos sênior
            target = self._meta_turnos(e, rank)
            while sol.load[e] < target:
                # candidatos viáveis = elegíveis e ainda não alocados + dia livre
                C = [
                    s for s in I.eligible_sorted[e]
                    if (s in sol.unassigned) and (not sol.used_day[(e, I.d_s[s])])
                ]
                if not C:
                    break

                # Random+Greedy: diversificação
                if strategy == 'random_plus_greedy' and rng.random() < random_p:
                    assign_inplace(I, sol, e, rng.choice(C))
                    continue

                # g(s) = d_ies
                gmin = I.v_es[(e, C[0])]
                gmax = I.v_es[(e, C[-1])]
                thr  = gmin + alpha * (gmax - gmin)

                # RCL de limiar (lista já ordenada → pára cedo)
                RCL: List[Occ] = []
                for s in C:
                    v = I.v_es[(e, s)]
                    if v <= thr:
                        RCL.append(s)
                    else:
                        break

                assign_inplace(I, sol, e, rng.choice(RCL))

        # ----------------------------------------
        # FASE 1B: preenchimento de turnos vazios
        # ----------------------------------------
        # Usa capacidade restante para reduzir ao máximo o nº de turnos não cobertos
        max_passes = 3
        for _ in range(max_passes):
            changed = False
            # percorre uma cópia porque vamos modificar sol.unassigned
            for s in list(sol.unassigned):
                # candidatos: menos sênior primeiro
                cand_es = [e for e in reversed(I.E) if can_assign(I, sol, e, s)]
                if not cand_es:
                    continue
                # escolhe o elegível com menor insatisfação nesse turno
                best_e = min(cand_es, key=lambda e: I.v_es[(e, s)])
                assign_inplace(I, sol, best_e, s)
                changed = True
            if not changed:
                break

        return sol

# =========================
# Busca Local – Fase 2
# =========================
class LocalSearch:
    def __init__(self, I: ThompsonInstance):
        # apenas a instância; usamos as funções globais can_assign / swap_inplace
        self.I = I

    def _diss_emp(self, sol: ThompsonSolution, e: EmpId) -> float:
        """Insatisfação total do empregado e na solução atual."""
        return sum(self.I.v_es[(e, s)] for s in self.I.S if sol.assign[s] == e)

    def _seniority_swap(
        self,
        sol: ThompsonSolution,
        rng: random.Random,
        max_pairs: int = 100000,
    ) -> Optional[ThompsonSolution]:
        """
        V1 — Seniority-Swap (first improvement, com limite de pares).

        - Para cada par (e_sênior, e_júnior), tenta trocar turnos.
        - Aceita a primeira troca que reduz a insatisfação do MAIS SÊNIOR.
        - Explora NO MÁXIMO 'max_pairs' pares (pra não explodir tempo).
        """
        I = self.I
        E = I.E

        # turnos atuais por empregado (construído uma vez por chamada)
        by_emp = {e: [s for s in I.S if sol.assign[s] == e] for e in E}

        pairs_tried = 0

        for i in range(len(E) - 1):
            e_sen = E[i]
            sen_shifts = by_emp[e_sen]
            if not sen_shifts:
                continue

            for s1 in sen_shifts:
                v_sen_s1 = I.v_es[(e_sen, s1)]
                d1 = I.d_s[s1]

                for j in range(i + 1, len(E)):
                    e_jun = E[j]
                    jun_shifts = by_emp[e_jun]
                    if not jun_shifts:
                        continue

                    for s2 in jun_shifts:
                        pairs_tried += 1
                        if pairs_tried > max_pairs:
                            # limite de exploração atingido → considera sem melhoria
                            return None

                        # sênior precisa poder fazer s2 e melhorar
                        if (e_sen, s2) not in I.ES:
                            continue
                        d2 = I.d_s[s2]
                        if d1 != d2 and sol.used_day[(e_sen, d2)]:
                            continue
                        if I.v_es[(e_sen, s2)] >= v_sen_s1:
                            continue  # não melhora o sênior

                        # checagem final de viabilidade para o par (inclui júnior)
                        if not can_swap(I, sol, s1, s2):
                            continue

                        # FIRST-IMPROVEMENT: aceita a primeira troca que melhora o sênior
                        swap_inplace(I, sol, s1, s2)
                        return sol

        return None

    def _uncovered_shift_relocation(
        self,
        sol: ThompsonSolution,
        rng: random.Random,
    ) -> Optional[ThompsonSolution]:
        """
        V2 — Uncovered-Shift-Relocation:
        tenta alocar turnos não cobertos priorizando menos sênior.
        """
        I = self.I
        uncovered = [s for s in I.S if sol.assign[s] is None]
        if not uncovered:
            return None

        for s in uncovered:
            for e in reversed(I.E):  # menos sênior primeiro
                if can_assign(I, sol, e, s):
                    assign_inplace(I, sol, e, s)
                    return sol

        return None

    def improve(
        self,
        sol: ThompsonSolution,
        rng: random.Random,
        max_ls_iters: int = 200,
    ) -> ThompsonSolution:
        """
        Parada:
        - nenhuma melhoria em V1 nem V2
        OU
        - atingiu max_ls_iters (teto de segurança).
        """
        best = sol
        it = 0

        while it < max_ls_iters:
            it += 1
            improved = False

            # V1 — Seniority-Swap
            s1 = self._seniority_swap(best, rng)
            if s1 is not None:
                best = s1
                improved = True
            else:
                # V2 — Uncovered-Shift-Relocation
                s2 = self._uncovered_shift_relocation(best, rng)
                if s2 is not None:
                    best = s2
                    improved = True

            if not improved:
                break  # nenhuma melhoria em ambas as vizinhanças

        return best

# =========================
# Reactive α
# =========================
class ReactiveAlpha:
    def __init__(self, alpha_list: List[float]):
        self.A = list(alpha_list)
        self.p = [1.0/len(self.A)] * len(self.A)
        self.best = [math.inf] * len(self.A)

    def sample(self, rng: random.Random) -> float:
        r = rng.random(); acc = 0.0
        for a, prob in zip(self.A, self.p):
            acc += prob
            if r <= acc: return a
        return self.A[-1]

    def update(self, alpha: float, report_value: float):
        i = self.A.index(alpha)
        self.best[i] = min(self.best[i], report_value)
        m = min(self.best)
        scores = [1.0/(1.0 + (v - m)) for v in self.best]
        s = sum(scores)
        self.p = [x/s for x in scores]

# =========================
# GRASP driver (apenas tempo máximo)
# =========================
class ThompsonGRASP:
    def __init__(
        self,
        inst: ThompsonInstance,
        max_time_sec: float = 1800.0,               # critério principal de parada
        alpha: float = 0.25,
        construction: str = 'traditional',        # 'traditional' | 'random_plus_greedy' | 'reactive'
        alpha_list: Optional[List[float]] = None,
        random_p: float = 0.25,
        random_seed: int = 123
    ):
        assert construction in ('traditional','random_plus_greedy','reactive')
        self.I = inst
        self.max_time_sec = max_time_sec          # tempo máximo principal
        self.alpha = alpha
        self.construction = construction
        self.random_p = random_p
        self.rng = random.Random(random_seed)
        self.cons = Constructor(inst)
        self.ls = LocalSearch(inst)
        self.reactive = ReactiveAlpha(alpha_list or [0.0,0.2,0.4,0.6,0.8,1.0]) if construction=='reactive' else None
        self.random_seed = random_seed

    def run(self) -> Tuple[ThompsonSolution, LexCost, List[float], int, int]:
        """
        Retorna:
          - melhor solução
          - custo lexicográfico da melhor solução
          - histórico da FO agregada (report_value) ao longo das iterações
          - iteração em que houve a última melhoria (convergência)
          - número total de iterações executadas

        Critério de parada: APENAS tempo máximo (max_time_sec).
        """
        best_sol: Optional[ThompsonSolution] = None
        best_cost: Optional[LexCost] = None

        
        last_improve_iter = 0
        total_iters = 0

        t_start = time.time()
        it = 0

        while True:
            it += 1

            a = self.alpha if self.reactive is None else self.reactive.sample(self.rng)
            s = self.cons.build(alpha=a, rng=self.rng, strategy=self.construction, random_p=self.random_p)
            s = self.ls.improve(s, rng=self.rng)
            c = lex_cost(self.I, s)

            total_iters = it
            

            if (best_cost is None) or lex_better(c, best_cost):
                best_sol, best_cost = s, c
                last_improve_iter = it

            if self.reactive:
                self.reactive.update(a, c.report_value)

            # critério de parada: tempo máximo
            elapsed = time.time() - t_start
            if elapsed >= self.max_time_sec:
                break

        assert best_sol is not None and best_cost is not None
        return best_sol, best_cost, last_improve_iter, total_iters

# =========================
# Relatório textual (para debug / visualização)
# =========================
def summarize_solution(I: ThompsonInstance, sol: ThompsonSolution, cost: LexCost) -> str:
    lines: List[str] = []

    # -------------------------------------------------
    # "Cabeçalho" dos níveis lexicográficos
    # -------------------------------------------------
    n_unalloc = int(cost.comp[0])

    lines.append("\nOtimização (GRASP) concluída!")
    lines.append("")
    lines.append(f"Nível 0 (turnos não alocados) -> valor: {n_unalloc}")

    # cost.comp = ( #não alocados, diss_E1, diss_E2, ... )
    for idx, e in enumerate(I.E, start=1):
        diss_e = cost.comp[idx]
        lines.append(f"  Nível {idx} (insatisfação de {e}) -> valor: {diss_e:.2f}")

    # -------------------------------------------------
    # 1) Atribuições por empregado
    # -------------------------------------------------
    alocacoes_por_empregado: Dict[EmpId, List[Occ]] = {
        e: list(sol.by_emp[e]) for e in I.E
    }

    turnos_alocados_count = sum(len(v) for v in alocacoes_por_empregado.values())

    lines.append("\n--- Alocações por Empregado ---")
    for e in I.E:
        alocados = sorted(
            alocacoes_por_empregado[e],
            key=lambda s: (I.d_s[s], I.ST_s[s], s[1])
        )
        lines.append(f"  {e} ({len(alocados)} / {I.m_e[e]} turnos): {alocados}")

    # -------------------------------------------------
    # 2) Turnos NÃO alocados
    # -------------------------------------------------
    turnos_nao_alocados = sorted(list(sol.unassigned))

    lines.append("\n--- Turnos NÃO Alocados ---")
    if turnos_nao_alocados:
        for s in turnos_nao_alocados:
            lines.append(f"  Turno (Dia: {s[0]}, ID: {s[1]}) "
                         f"(TT={I.TT_s[s]}, ST={I.ST_s[s]})")
    else:
        lines.append("  Todos os turnos foram alocados!")

    # -------------------------------------------------
    # 3) Atribuições por Turno (lista completa)
    # -------------------------------------------------
    lines.append("\n--- Atribuições por Turno (todos os turnos) ---")
    for s in sorted(I.S, key=lambda x: (I.d_s[x], I.ST_s[x], x[1])):
        e = sol.assign[s]
        if e is None:
            lines.append(
                f"  Turno (Dia: {s[0]}, ID: {s[1]}) -> NÃO ALOCADO "
                f"(TT={I.TT_s[s]}, ST={I.ST_s[s]})"
            )
        else:
            lines.append(
                f"  Turno (Dia: {s[0]}, ID: {s[1]}) -> Empregado {e} "
                f"(TT={I.TT_s[s]}, ST={I.ST_s[s]})"
            )

    # -------------------------------------------------
    # 4) Verificação final
    # -------------------------------------------------
    total = turnos_alocados_count + len(turnos_nao_alocados)
    lines.append(
        f"\nVerificação: {turnos_alocados_count} turnos alocados, "
        f"{len(turnos_nao_alocados)} não alocados. "
        f"Total: {total} (de {len(I.S)})"
    )

    lines.append(f"\n(report_value GRASP = {cost.report_value:.2f})")

    return "\n".join(lines)

# =========================
# Funções auxiliares para rodar TODAS as instâncias e salvar em CSV
# =========================

def load_instance_module(path: str):
    """Importa dinamicamente um arquivo .py de instância."""
    module_name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def run_all_instances_and_save_csv(inst_dir: str,
                                   seed: int = 123,
                                   max_time_sec: float = 1800.0,
                                   out_csv: str = "resultados_grasp_thompson.csv"):
    """
    Varre todos os arquivos .py de instância em inst_dir,
    roda GRASP (3 estratégias) e salva resumo em CSV.

    Campos principais no CSV:
      - obj_cost: custo da função objetivo (report_value da melhor solução)
      - avg_diss_per_emp: média de insatisfação por empregado
      - n_covered / n_uncovered
      - time_sec
      - conv_iter: iteração em que houve a última melhoria (convergência)
      - iterations_run: número de iterações que couberam no tempo
    """
    if not os.path.isdir(inst_dir):
        raise SystemExit(f"Pasta de instâncias não encontrada: {inst_dir}")

    print(f"Lendo instâncias em: {inst_dir}")

    STRATEGIES = ["traditional", "random_plus_greedy", "reactive"]
    ALPHA_TRAD = 0.25
    ALPHA_LIST_REACT = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    RANDOM_P_RPG = 0.30

    rows: List[Dict[str, object]] = []

    for fname in sorted(os.listdir(inst_dir)):
        if not fname.endswith(".py"):
            continue

        instance_path = os.path.join(inst_dir, fname)
        instance_name = os.path.splitext(fname)[0]

        print(f"\n=== Instância: {instance_name} ===")
        mod = load_instance_module(instance_path)

        try:
            employee_data = mod.employee_data
            shift_data = mod.shift_data
            shift_requirements = mod.shift_requirements
        except AttributeError as exc:
            print(f"  [ERRO] Arquivo {fname} não possui "
                  f"employee_data / shift_data / shift_requirements: {exc}")
            continue

        I = ThompsonInstance(employee_data, shift_data, shift_requirements)
        total_shifts = len(I.S)

        for strategy in STRATEGIES:
            print(f"  -> Estratégia: {strategy}")

            if strategy == "reactive":
                grasp = ThompsonGRASP(
                    I,
                    max_time_sec=max_time_sec,
                    construction="reactive",
                    alpha_list=ALPHA_LIST_REACT,
                    random_seed=seed,
                )
            elif strategy == "random_plus_greedy":
                grasp = ThompsonGRASP(
                    I,
                    max_time_sec=max_time_sec,
                    alpha=ALPHA_TRAD,
                    construction="random_plus_greedy",
                    random_p=RANDOM_P_RPG,
                    random_seed=seed,
                )
            else:  # traditional
                grasp = ThompsonGRASP(
                    I,
                    max_time_sec=max_time_sec,
                    alpha=ALPHA_TRAD,
                    construction="traditional",
                    random_seed=seed,
                )

            t0 = time.time()
            sol, cost, conv_iter, total_iters = grasp.run()
            t1 = time.time()
            elapsed = t1 - t0

            n_unalloc = int(cost.comp[0])
            n_covered = total_shifts - n_unalloc
            obj_cost = cost.report_value

            # média da insatisfação por empregado
            if len(I.E) > 0:
                mean_diss = sum(cost.comp[1:]) / len(I.E)
            else:
                mean_diss = 0.0

            row: Dict[str, object] = {
                "instance": instance_name,
                "strategy": strategy,
                "alpha": grasp.alpha if strategy != "reactive" else "",
                "random_p": grasp.random_p if strategy == "random_plus_greedy" else "",
                "seed": seed,
                # métricas pedidas
                "obj_cost": obj_cost,
                "avg_diss_per_emp": round(mean_diss, 4),
                "n_covered": n_covered,
                "n_uncovered": n_unalloc,
                "time_sec": round(elapsed, 4),
                "conv_iter": conv_iter,        # iteração da última melhoria
                "iterations_run": total_iters,  # quantas iterações couberam no tempo
            }

            rows.append(row)

    if not rows:
        print("\nNenhuma instância/resultado gerado. Verifique a pasta.")
        return

    fieldnames = sorted({k for row in rows for k in row.keys()})

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResultados salvos em: {out_csv}")

# =========================
# Execução como script
# =========================
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # >>> AJUSTE AQUI se o caminho for diferente:
    # Ex.: nbtel-optimization/instancias novas/instancias novas/*.py
    INST_DIR = os.path.join(BASE_DIR, "instancias novas")
    # Se for só "instancias novas", use:
    # INST_DIR = os.path.join(BASE_DIR, "instancias novas")

    OUT_CSV = os.path.join(BASE_DIR, "resultados_grasp_thompson.csv")

    run_all_instances_and_save_csv(
        inst_dir=INST_DIR,
        seed=123,
        max_time_sec=1800.0,     # tempo máximo por execução de GRASP (ajuste aqui)
        out_csv=OUT_CSV,
    )
