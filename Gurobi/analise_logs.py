# -*- coding: utf-8 -*-
import os
import re # Para usar Expressões Regulares (RegEx)
import csv
import time

# --- Configurações ---
PASTA_RESULTADOS = "resultados2"
ARQUIVO_SAIDA_CSV = "tabela_resultados_finais.csv"

# Pegue os IDs dos experimentos do seu run_all.py
# (Vou usar apenas alguns como exemplo, cole a sua lista completa)
EXPERIMENTOS_IDS = [
    'Grupo0_Artigo_Thompson_Baseline',
    'Grupo1_Escala_Pequena_282',
    'Grupo1_Escala_Media_315',
    'Grupo1_Escala_Grande_420',
    'Grupo1_Escala_Extrema_630',
    'Grupo2_Disponib_FlexTotal_U0',
    'Grupo2_Disponib_Base_U1',
    'Grupo2_Disponib_Restrita_U2',
    'Grupo2_Disponib_Gargalo_U3',
    'Grupo3_Skills_Facil_S5_Max7',
    'Grupo3_Skills_Base_S8_Max5',
    'Grupo3_Skills_Dificil_S15_Max4',
    'Grupo3_Skills_Extrema_S20_Max3',
    'Grupo4_Repet_Baseline_Run1',
    'Grupo4_Repet_Baseline_Run2',
    'Grupo4_Repet_Baseline_Run3',
    'Grupo5_Repet_Baseline_Run4',
    'Grupo5_Pequena_Dificil_S20_U2',
    'Grupo5_Grande_Facil_S5_U0',
    'Grupo5_Excesso_MaoDeObra_420_250F',
]

def analisar_log(log_path):
    """
    Lê um arquivo de log e extrai o tempo e a soma da insatisfação.
    """
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"  [AVISO] Log não encontrado: {log_path}")
        return None, None, None, None, None

    # 1. Encontrar o TEMPO total de execução do Gurobi
    # (Ex: "Multi-objectives: stopped in 1800.02 seconds")
    match_time = re.search(r"Multi-objectives: (?:stopped|solved) in ([\d\.]+) seconds", content)
    tempo_gurobi = float(match_time.group(1)) if match_time else None

    # 2. Encontrar os turnos NÃO ALOCADOS (Resultado do Nível 0)
    # (Ex: "Best objective 0.000000000000e+00, best bound 0.000000000000e+00")
    # Nota: re.findall encontra TODOS os matches. O primeiro é sempre o Nível 0.
    matches_obj = re.findall(r"Optimal solution found.*?\nBest objective ([\d\.e\+\-]+)", content, re.DOTALL)
    
    if not matches_obj:
        # Pode ter falhado (ex: Infeasible)
        status_match = re.search(r"O modelo é inviável \(INFEASIBLE\)", content)
        if status_match:
            return "Infeasible", None, None, tempo_gurobi, None
        return "Erro", None, None, tempo_gurobi, None

    # 3. Pegar o resultado do Nível 0 (Turnos Não Alocados)
    turnos_nao_alocados = float(matches_obj[0])

    # 4. Pegar todos os outros níveis (Insatisfação)
    # [1:] significa "ignorar o primeiro item"
    valores_insatisfacao = [float(v) for v in matches_obj[1:]]
    
    if not valores_insatisfacao:
        # Acontece se o modelo parou antes de otimizar o Nível 1
        return "TimeLimit (Nivel 0)", turnos_nao_alocados, 0, tempo_gurobi, 0

    # 5. Calcular as métricas
    insatisfacao_total = sum(valores_insatisfacao)
    insatisfacao_media = insatisfacao_total / len(valores_insatisfacao)

    return "Sucesso", turnos_nao_alocados, insatisfacao_total, tempo_gurobi, insatisfacao_media


def main():
    print(f"Iniciando análise da pasta: {PASTA_RESULTADOS}/")
    
    # Abre o arquivo CSV para escrever os resultados
    with open(ARQUIVO_SAIDA_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Escreve o cabeçalho
        writer.writerow([
            "Instancia (Tamanho)",
            "Status",
            "Turnos_Nao_Alocados (Nivel 0)",
            "Insatisfacao_Total (Melhor Ganho)",
            "Insatisfacao_Media_por_Nivel (Ganho Medio)",
            "Tempo_Gurobi (s)"
        ])

        # Itera sobre todos os experimentos definidos
        for exp_id in EXPERIMENTOS_IDS:
            print(f"Analisando: {exp_id}...")
            
            # Monta o caminho para o arquivo de log principal
            log_path = os.path.join(PASTA_RESULTADOS, exp_id, f"log_console_completo_{exp_id}.txt")
            
            status, nao_alocados, insat_total, tempo, insat_media = analisar_log(log_path)
            
            # Escreve a linha no CSV
            writer.writerow([
                exp_id,
                status,
                nao_alocados,
                insat_total,
                insat_media,
                tempo
            ])

    print(f"\nAnálise concluída. Resultados salvos em: {ARQUIVO_SAIDA_CSV}")

if __name__ == "__main__":
    main()