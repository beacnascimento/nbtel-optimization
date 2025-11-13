# -*- coding: utf-8 -*-
# Thompson (1997) adaptado às instâncias fornecidas
import gurobipy as gp
from gurobipy import GRB, quicksum

import json # Importe o JSON aqui no topo
import sys  # Importe o SYS para lidar com erros

# -------------------------------------------------------------
# 0) DADOS (Importados do 'instancia_temp.py')
# -------------------------------------------------------------

# Tenta importar os dados gerados pelo 'gerador.py'
try:
    import instancia_temp as dados
except ImportError:
    print("\nERRO: Arquivo 'instancia_temp.py' não encontrado.")
    print("Por favor, execute o 'gerador.py' ou 'run_all.py' primeiro.")
    sys.exit(1) # Interrompe o script se os dados não existirem
except Exception as e:
    print(f"\nERRO ao importar 'instancia_temp.py': {e}")
    sys.exit(1)

# Atribui os dados importados às variáveis do modelo
try:
    day_map = dados.day_map
    employee_data = dados.employee_data
    shift_data = dados.shift_data
    shift_requirements = dados.shift_requirements
    
    if not all([day_map, employee_data, shift_data, shift_requirements]):
        print("\nERRO: O arquivo 'instancia_temp.py' está incompleto.")
        sys.exit(1)
        
    print("[INFO] Dados da instância 'instancia_temp.py' carregados com sucesso.")
    
except AttributeError:
    print("\nERRO: O arquivo 'instancia_temp.py' não contém os dicionários esperados.")
    print("(Faltando: day_map, employee_data, shift_data ou shift_requirements)")
    sys.exit(1)


# -------------------------------------------------------------
# 1) PRÉ-PROCESSAMENTO: construir S como ocorrências únicas
#    s = (day, id)  (ex.: ('Mon', 1))
# -------------------------------------------------------------
days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

# todas as ocorrências exigidas (cada par day-id)
S = [(day, sid) for day, ids in shift_requirements.items() for sid in ids]

# atributos por ocorrência s=(day,sid)
ST_s  = { (day, sid): shift_data[sid]['ST'] for day, sid in S }
BL_s  = { (day, sid): shift_data[sid]['BL'] for day, sid in S }
TT_s  = { (day, sid): shift_data[sid]['TT'] for day, sid in S }
d_s   = { (day, sid): day for day, sid in S }  # dia nominal (str)
c_s   = TT_s                                   # no nosso modelo, “categoria” = TT (habilidade)

# -------------------------------------------------------------
# 2) CONJUNTOS/ORDENAÇÃO DE EMPREGADOS (senioridade)
# -------------------------------------------------------------
# E-01 é mais sênior. Ordenar por número.
def emp_sort_key(eid):
    # 'E-01' -> 1
    return int(eid.split('-')[1])

E = sorted(list(employee_data.keys()), key=emp_sort_key)

# parâmetros por empregado
ST_e  = { e: employee_data[e]['ST'] for e in E }
LL_e  = { e: employee_data[e]['LL'] for e in E }
ES_e  = { e: employee_data[e]['ES'] for e in E }
LS_e  = { e: employee_data[e]['LS'] for e in E }
Ce_e  = { e: set(employee_data[e]['SklTyp']) for e in E }
m_e   = { e: employee_data[e]['MxWk'] for e in E }
Un_e  = { e: set(employee_data[e]['UnDay']) for e in E }  # indisponíveis
# Dias disponíveis = todos - indisponíveis
De_e  = { e: set(days) - Un_e[e] for e in E }

# -------------------------------------------------------------
# 3) Custo de insatisfação v_es
#    Regra do Thompson: depende da diferença de horário de início.
#    Se ST_s < ST_e -> ES * (ST_e - ST_s); caso contrário LS * (ST_s - ST_e).
#    (opcional) penalizar diferença de almoço |BL_s - LL_e| com fator LAMBDA_LUNCH.
# -------------------------------------------------------------
LAMBDA_LUNCH = 0.0  # ajuste se quiser penalizar almoço (ex.: 1.0)

def diss(e, s):
    ste = ST_e[e]
    sts = ST_s[s]
    if sts < ste:
        pen_start = ES_e[e] * (ste - sts)
    else:
        pen_start = LS_e[e] * (sts - ste)
    pen_lunch = LAMBDA_LUNCH * abs(BL_s[s] - LL_e[e])
    return pen_start + pen_lunch

# -------------------------------------------------------------
# 4) ELEGIBILIDADE: (TT_s ∈ Ce_e) e (d_s ∈ De_e)
# -------------------------------------------------------------
ES = set()
v_es = {}
for e in E:
    for s in S:
        if (TT_s[s] in Ce_e[e]) and (d_s[s] in De_e[e]):
            ES.add((e, s))
            v_es[(e, s)] = diss(e, s)

# -------------------------------------------------------------
# 5) MODELO E VARIÁVEIS
# -------------------------------------------------------------
m = gp.Model("Thompson_1997_instances")

# x[e,s] binária
x = m.addVars(list(ES), vtype=GRB.BINARY, name="x")

# u[s] binária: 1 se a ocorrência s ficou sem cobertura
u = m.addVars(S, vtype=GRB.BINARY, name="u")

# y[e] binária: 1 se atingiu o máximo m_e[e]
y = m.addVars(E, vtype=GRB.BINARY, name="y")

# -------------------------------------------------------------
# 6) RESTRIÇÕES
# -------------------------------------------------------------

# (2) Cobertura de cada ocorrência: sum_e x[e,s] + u[s] = 1
for s in S:
    m.addConstr(quicksum(x[e, s] for e in E if (e, s) in ES) + u[s] == 1, name=f"cover_{s}")

# (3) Pelo menos um turno por empregado
# for e in E:
#     m.addConstr(quicksum(x[e, s] for s in S if (e, s) in ES) >= 1, name=f"atleast1_{e}")

# (4) No máximo m_e por empregado
for e in E:
    m.addConstr(quicksum(x[e, s] for s in S if (e, s) in ES) <= m_e[e], name=f"max_{e}")

# (5) No máximo 1 turno por dia e por empregado
for e in E:
    for day in De_e[e]:  # só faz sentido nos dias em que ele pode trabalhar
        m.addConstr(
            quicksum(x[e, s] for s in S if ((e, s) in ES and d_s[s] == day)) <= 1,
            name=f"oneday_{e}_{day}"
        )

# (6) Senioridade (parte 1)
# Para e menos sênior (i>0): sum_s x[e,s] <= 1 + (m_e[e]-1)*y[e_prev]
for i in range(1, len(E)):
    e = E[i]
    e_prev = E[i - 1]
    m.addConstr(
        quicksum(x[e, s] for s in S if (e, s) in ES) <= 1 + (m_e[e] - 1) * y[e_prev],
        name=f"seniority_up_{e}"
    )

# (7) Senioridade (parte 2):
# m_e[e] * y[e] <= sum_s x[e,s], para todos exceto possivelmente o último
for i in range(0, len(E) - 1):
    e = E[i]
    m.addConstr(
        m_e[e] * y[e] <= quicksum(x[e, s] for s in S if (e, s) in ES),
        name=f"seniority_flag_{e}"
    )

# -------------------------------------------------------------
# 7) MULTIOBJETIVO LEXICOGRÁFICO (PREEMPTIVO)
#     Nível 1: minimizar não-alocados
#     Níveis seguintes: minimizar insatisfação por empregado (ordem de senioridade)
# -------------------------------------------------------------
P0 = 1.0                       # peso do nível 1 (dentro do nível)
P_e = {e: 1.0 for e in E}      # pesos por empregado (dentro do nível)

prio_unalloc = len(E) + 1      # prioridade máxima
obj_unalloc = P0 * quicksum(u[s] for s in S)
m.setObjectiveN(obj_unalloc, index=0, priority=prio_unalloc, weight=1.0, name="unallocated")

# Empregados: E[0] é mais sênior -> maior prioridade
for i, e in enumerate(E):
    prio_e = len(E) - i
    obj_e = P_e[e] * quicksum(v_es[e, s] * x[e, s] for s in S if (e, s) in ES)
    m.setObjectiveN(obj_e, index=i + 1, priority=prio_e, weight=1.0, name=f"diss_{e}")

m.ModelSense = GRB.MINIMIZE


# -------------------------------------------------------------
# 8) OTIMIZAÇÃO
# -------------------------------------------------------------

m.Params.TimeLimit = 1800 

# (Opcional, mas recomendado) Adicione um print para saber que o limite está ativo
print(f"\n[INFO] Iniciando otimização com limite de tempo de {m.Params.TimeLimit} segundos...\n")

m.optimize()

# -------------------------------------------------------------
# 9) RELATÓRIO DE SAÍDA
# -------------------------------------------------------------
# if m.status in (GRB.OPTIMAL, GRB.INTERRUPTED):
#     print(f"Nível 0 (turnos não alocados) -> valor: {m.ObjNVal}")
#     for k in range(1, m.NumObj):
#         m.params.ObjNumber = k
#         print(f"  Nível {k} -> valor: {m.ObjNVal}")

#     print("\nAtribuições (x[e,(day,id)]=1):")
#     for (e, s), var in x.items():
#         if var.X > 0.5:
#             print(f"  {e} -> {s}  (TT={TT_s[s]}, ST_turno={ST_s[s]}, v_es={v_es[(e,s)]:.2f})")

#     print("\nTurnos não alocados (u[s]=1):")
#     for s, var in u.items():
#         if var.X > 0.5:
#             print(f"  {s} (TT={TT_s[s]}, ST={ST_s[s]})")
# -------------------------------------------------------------
# 9) RELATÓRIO DE SAÍDA (Versão Corrigida para run_all.py)
# -------------------------------------------------------------

# Nomes dos arquivos temporários que o run_all.py espera
NOME_JSON_SAIDA = 'resultado_temp.json'
NOME_LOG_SAIDA = 'report_temp.txt'
NOME_LP_MODELO = 'model.lp'
NOME_ILP_INVIAVEL = 'modelo_inviavel.ilp'

if m.status in (GRB.OPTIMAL, GRB.INTERRUPTED):
    print("Otimização concluída com sucesso!")

    # --- 1. Processar resultados nas estruturas de dados ---
    alocacoes_por_empregado = {e: [] for e in E}
    turnos_alocados_count = 0
    turnos_nao_alocados = []

    for (e, s), var in x.items():
        if var.X > 0.5:
            alocacoes_por_empregado[e].append(s)
            turnos_alocados_count += 1

    for s, var in u.items():
        if var.X > 0.5:
            turnos_nao_alocados.append(s)
            
    # Pega o valor do objetivo Nível 0 (não alocados)
    m.params.ObjNumber = 0
    obj_nao_alocados = m.ObjNVal

    # --- 2. Imprimir o relatório (para o log do subprocesso) ---
    print("\n--- Alocações por Empregado ---")
    for e, alocados in alocacoes_por_empregado.items():
        print(f"  {e} ({len(alocados)} / {m_e[e]} turnos): {alocados}")

    print("\n--- Turnos NÃO Alocados ---")
    if turnos_nao_alocados:
        for s in turnos_nao_alocados:
            print(f"  Turno (Dia: {s[0]}, ID: {s[1]})")
    else:
        print("  Todos os turnos foram alocados!")
    print(f"\nVerificação: {turnos_alocados_count} turnos alocados, {len(turnos_nao_alocados)} não alocados. Total: {turnos_alocados_count + len(turnos_nao_alocados)} (de {len(S)})")

    # --- 3. Salvar o relatório em JSON ---
    print(f"Salvando relatório em '{NOME_JSON_SAIDA}'...")
    dados_de_saida = {
        "status": "Solucao Encontrada",
        "tempo_execucao_seg": m.Runtime,
        "objetivo_nivel_0_nao_alocados": obj_nao_alocados,
        "alocacoes": alocacoes_por_empregado,
        "turnos_nao_alocados": turnos_nao_alocados
    }
    try:
        with open(NOME_JSON_SAIDA, "w", encoding="utf-8") as f:
            json.dump(dados_de_saida, f, ensure_ascii=False, indent=4)
        print(f"Relatório '{NOME_JSON_SAIDA}' salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")

    # --- 4. Salvar o log de texto (Duplicado para segurança) ---
    print(f"Salvando log de texto em '{NOME_LOG_SAIDA}'...")
    try:
        with open(NOME_LOG_SAIDA, "w", encoding="utf-8") as f:
            f.write(f"Tempo de Execução (Gurobi): {m.Runtime:.2f} segundos\n")
            f.write(f"Turnos não alocados (Nível 0): {obj_nao_alocados}\n\n")
            f.write("--- Alocações por Empregado ---\n")
            for e, alocados in alocacoes_por_empregado.items():
                f.write(f"  {e} ({len(alocados)} / {m_e[e]} turnos): {alocados}\n")
            
            f.write("\n--- Turnos NÃO Alocados ---\n")
            if turnos_nao_alocados:
                for s in turnos_nao_alocados:
                    f.write(f"  Turno (Dia: {s[0]}, ID: {s[1]})\n")
            else:
                f.write("  Todos os turnos foram alocados!\n")
            
            f.write(f"\nVerificação: {turnos_alocados_count} turnos alocados, {len(turnos_nao_alocados)} não alocados. Total: {turnos_alocados_count + len(turnos_nao_alocados)} (de {len(S)})\n")
        print(f"Log '{NOME_LOG_SAIDA}' salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar Log TXT: {e}")

    # --- 5. Salvar o modelo .lp ---
    m.write(NOME_LP_MODELO)
    print(f"\nModelo salvo em '{NOME_LP_MODELO}'")


elif m.status == GRB.INFEASIBLE:
    print("\nO modelo é inviável (INFEASIBLE).")
    print("Computando IIS (Irreducible Inconsistent Subsystem) para depuração...")
    m.computeIIS()
    m.write(NOME_ILP_INVIAVEL)
    print(f"Arquivo '{NOME_ILP_INVIAVEL}' escrito. Verifique este arquivo para ver as restrições conflitantes.")
    # Importante: Sai com um código de erro para o 'run_all.py' saber que falhou
    sys.exit(1) 

elif m.status == GRB.INF_OR_UNBD:
    print("\nO modelo é inviável ou ilimitado (INF_OR_UNBD).")
    sys.exit(1)

else:
    print(f"\nOtimização terminada com status: {m.status}")
    sys.exit(1)