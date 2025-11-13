# -*- coding: utf-8 -*-
import subprocess
import os
import shutil
import time
import json

# ==============================================================================
# 1. DEFINIÇÃO DE TODOS OS 20 EXPERIMENTOS
# ==============================================================================
#
# AGORA SUPORTA INSTÂNCIAS ESTÁTICAS!
#
# Para instâncias geradas: use os parâmetros normais (n_employees, n_shifts, ...)
# Para instâncias estáticas: adicione a chave 'static_file': 'nome_do_arquivo.py'
#
# ==============================================================================

EXPERIMENTOS = [
    
    # --- INSTÂNCIA #1: A BASELINE DO ARTIGO (ESTÁTICA) ---
    {
        'id': 'Grupo0_Artigo_Thompson_Baseline',
        'static_file': 'instances.py'  
    },

    # --- GRUPO 1: ESCALABILIDADE (4 instâncias) ---
    {
        'id': 'Grupo1_Escala_Pequena_282',
        'n_employees': 120, 'n_shifts': 40,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo1_Escala_Media_315',
        'n_employees': 135, 'n_shifts': 45,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo1_Escala_Grande_420',
        'n_employees': 180, 'n_shifts': 60,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo1_Escala_Extrema_630',
        'n_employees': 250, 'n_shifts': 90,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    
    # --- GRUPO 2: SENSIBILIDADE À DISPONIBILIDADE (4 instâncias) ---
    {
        'id': 'Grupo2_Disponib_FlexTotal_U0',
        'n_employees': 180, 'n_shifts': 60, 'max_unavailable': 0
    },
    {
        'id': 'Grupo2_Disponib_Base_U1',
        'n_employees': 180, 'n_shifts': 60, 'max_unavailable': 1
    },
    {
        'id': 'Grupo2_Disponib_Restrita_U2',
        'n_employees': 180, 'n_shifts': 60, 'max_unavailable': 2
    },
    {
        'id': 'Grupo2_Disponib_Gargalo_U3',
        'n_employees': 180, 'n_shifts': 60, 'max_unavailable': 3
    },

    # --- GRUPO 3: SENSIBILIDADE ÀS HABILIDADES (4 instâncias) ---
    {
        'id': 'Grupo3_Skills_Facil_S5_Max7',
        'n_employees': 180, 'n_shifts': 60,
        'n_skills': 5, 'max_skills': 7, 'min_skills': 3
    },
    {
        'id': 'Grupo3_Skills_Base_S8_Max5',
        'n_employees': 180, 'n_shifts': 60,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2
    },
    {
        'id': 'Grupo3_Skills_Dificil_S15_Max4',
        'n_employees': 180, 'n_shifts': 60,
        'n_skills': 15, 'max_skills': 4, 'min_skills': 2
    },
    {
        'id': 'Grupo3_Skills_Extrema_S20_Max3',
        'n_employees': 180, 'n_shifts': 60,
        'n_skills': 20, 'max_skills': 3, 'min_skills': 1
    },

    # --- GRUPO 4: REPETIBILIDADE (4 instâncias) ---
    {
        'id': 'Grupo4_Repet_Baseline_Run1',
        'n_employees': 180, 'n_shifts': 60, 'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo4_Repet_Baseline_Run2',
        'n_employees': 180, 'n_shifts': 60, 'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo4_Repet_Baseline_Run3',
        'n_employees': 180, 'n_shifts': 60, 'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    
    # --- GRUPO 5: INTERAÇÃO E OUTROS (4 instâncias) ---
    {
        'id': 'Grupo5_Repet_Baseline_Run4', # Movido para cá para completar 20
        'n_employees': 180, 'n_shifts': 60, 'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
    {
        'id': 'Grupo5_Pequena_Dificil_S20_U2',
        'n_employees': 100, 'n_shifts': 35,
        'n_skills': 20, 'max_skills': 2, 'min_skills': 1, 'max_unavailable': 2
    },
    {
        'id': 'Grupo5_Grande_Facil_S5_U0',
        'n_employees': 250, 'n_shifts': 90,
        'n_skills': 5, 'max_skills': 7, 'min_skills': 3, 'max_unavailable': 0
    },
    {
        'id': 'Grupo5_Excesso_MaoDeObra_420_250F',
        'n_employees': 250, 'n_shifts': 60,
        'n_skills': 8, 'max_skills': 5, 'min_skills': 2, 'max_unavailable': 1
    },
]

# ==============================================================================
# 2. SCRIPT DE AUTOMAÇÃO (ORQUESTRADOR)
# ==============================================================================
# (Modificado para suportar 'static_file')

def run_experiment(exp, log_file):
    """
    Executa um único experimento (Gerar/Copiar, Resolver, Salvar).
    """
    instance_name = exp['id']
    print("\n" + "="*80)
    print(f"--- INICIANDO EXPERIMENTO: {instance_name} ---")
    print(f"Parâmetros: {exp}")
    log_file.write(f"\n{time.ctime()} - INICIANDO: {instance_name}\n")
    log_file.flush()

    # --- Passo A: Gerar ou Copiar Instância ---
    
    if 'static_file' in exp:
        # --- Este é um experimento ESTÁTICO ---
        static_filename = exp['static_file']
        print(f"Usando arquivo estático: {static_filename}")
        
        if not os.path.exists(static_filename):
            print(f"ERRO FATAL: Arquivo estático '{static_filename}' não encontrado.")
            log_file.write(f"{time.ctime()} - ERRO (Estático): {instance_name} - Arquivo {static_filename} não existe\n")
            log_file.flush()
            return # Pula este experimento
        
        try:
            # Copia o arquivo estático (ex: instances.py) para 'instancia_temp.py'
            shutil.copyfile(static_filename, 'instancia_temp.py')
            print(f"Arquivo '{static_filename}' copiado para 'instancia_temp.py'")
        except Exception as e:
            print(f"ERRO FATAL ao copiar {static_filename}: {e}")
            log_file.write(f"{time.ctime()} - ERRO (Cópia): {instance_name} - {e}\n")
            log_file.flush()
            return
            
    else:
        # --- Este é um experimento GERADO ---
        print("Executando gerador.py...")
        cmd_generate = ["python", "gerador.py"]
        for param, value in exp.items():
            if param != 'id':
                cmd_generate.append(f"--{param.replace('_', '-')}")
                cmd_generate.append(str(value))
        
        try:
            subprocess.run(cmd_generate, check=True, capture_output=True, text=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            print(f"ERRO FATAL ao gerar instância para {instance_name}.")
            print(e.stderr)
            log_file.write(f"{time.ctime()} - ERRO (Geração): {instance_name}\n")
            log_file.flush()
            return

    # --- Passo B: Resolver o Modelo ---
    # print("Executando new_model_big.py (solver)...")
    # start_time = time.time()
    
    # # Lembre-se de colocar um TimeLimit DENTRO do new_model_big.py
    # # ex: m.Params.TimeLimit = 7200 # 2 horas
    
    # try:
    #     timeout_segundos = 6 * 3600 # Timeout de 6 horas
    #     #outfile = open(f"{instance_name}.out", "w")#, encoding="utf-8")
    #     #errfile = open(f"{instance_name}.err", "w")#, encoding="utf-8")
    #     result = subprocess.run(
    #         ["python", "new_model_big.py"], 
    #         check=True, 
    #         capture_output=True, 
    #         text=True, 
    #         encoding='utf-8',
    #         timeout=timeout_segundos,
    #         #stdout= outfile,
    #         #stderr= errfile
    #     )
        
    #     #outfile.close()
    #     #errfile.close()



        # end_time = time.time()
        # tempo_total = end_time - start_time
    #     print(f"Modelo concluído. Tempo total: {tempo_total:.2f} segundos.")
    #     log_file.write(f"{time.ctime()} - SUCESSO: {instance_name} - Tempo: {tempo_total:.2f}s\n")
    #     log_file.flush()
        
    # except subprocess.TimeoutExpired:
    #     print(f"ERRO: TIMEOUT DO PROCESSO para {instance_name} (excedeu {timeout_segundos}s).")
    #     log_file.write(f"{time.ctime()} - ERRO (Timeout): {instance_name}\n")
    #     log_file.flush()
    #     return
        
    # except subprocess.CalledProcessError as e:
    #     print(f"ERRO FATAL ao resolver o modelo para {instance_name}.")
    #     print("--- STDOUT (Saída do Solver): ---")
    #     print(e.stdout)
    #     print("--- STDERR (Erro do Solver): ---")
    #     print(e.stderr)
    #     log_file.write(f"{time.ctime()} - ERRO (Solver): {instance_name}\n")
    #     log_file.flush()
    #     pass

    # --- Passo B: Resolver o Modelo ---
    print("Executando new_model_big.py (solver)...")
    
    # Nomes dos arquivos de log temporários
    STDOUT_LOG_TEMP = "log_console_temp.txt"
    STDERR_LOG_TEMP = "log_stderr_temp.txt"

    try:
        timeout_segundos = 6 * 3600
        start_time = time.time()
        
        # Abre os arquivos de log (stdout e stderr)
        with open(STDOUT_LOG_TEMP, "w", encoding="utf-8") as f_out, \
             open(STDERR_LOG_TEMP, "w", encoding="utf-8") as f_err:
            
            # Executa o subprocesso, redirecionando o output
            result = subprocess.run(
                ["python", "new_model_big.py"],
                check=True,       # Levanta um erro se o script falhar (exit code != 0)
                text=True,        # Garante que o output é texto
                timeout=timeout_segundos,
                stdout=f_out,     # REDIRECIONA stdout PARA o arquivo f_out
                stderr=f_err      # REDIRECIONA stderr PARA o arquivo f_err
            )
        
        end_time = time.time()
        tempo_total = end_time - start_time
        print(f"Modelo concluído. Tempo total: {tempo_total:.2f} segundos.")
        log_file.write(f"{time.ctime()} - SUCESSO: {instance_name} - Tempo: {tempo_total:.2f}s\n")
        log_file.flush()

    except subprocess.TimeoutExpired:
        # O timeout aconteceu. Os logs (stdout/stderr) JÁ FORAM escritos
        # até o momento do timeout, o que é ótimo para a análise.
        print(f"ERRO: TIMEOUT DO PROCESSO para {instance_name} (excedeu {timeout_segundos}s).")
        log_file.write(f"{time.ctime()} - ERRO (Timeout): {instance_name}\n")
        log_file.flush()
        pass # Continua para a seção C (Arquivamento)

    except subprocess.CalledProcessError as e:
        # O script new_model_big.py falhou (ex: Infeasible, que retorna sys.exit(1))
        # Os logs (stdout/stderr) JÁ FORAM escritos, capturando o erro.
        print(f"ERRO: O Solver falhou (provavelmente Infeasible ou erro) para {instance_name}.")
        print(f"Veja '{STDERR_LOG_TEMP}' para detalhes (se houver).")
        log_file.write(f"{time.ctime()} - ERRO (Solver Falhou): {instance_name}\n")
        log_file.flush()
        pass # Continua para a seção C (Arquivamento)

    # --- Passo C: Salvar e Arquivar Resultados ---
    # print("Arquivando arquivos de resultado...")
    # output_dir = os.path.join("resultados", instance_name)
    # os.makedirs(output_dir, exist_ok=True)
    
    # files_to_move = {
    #     "instancia_temp.py": f"instancia_{instance_name}.py",
    #     "resultado_temp.json": f"resultado_{instance_name}.json",
    #     "resultado_temp.txt": f"log_solver_{instance_name}.txt",
    #     "model.lp": f"modelo_{instance_name}.lp",
    #     "modelo_inviavel.ilp": f"modelo_inviavel_{instance_name}.ilp"
    # }


    # --- Passo C: Salvar e Arquivar Resultados ---
    print("Arquivando arquivos de resultado...")
    output_dir = os.path.join("resultados2", instance_name)
    os.makedirs(output_dir, exist_ok=True)
    
    files_to_move = {
        # Arquivos padrão
        "instancia_temp.py": f"instancia_{instance_name}.py",
        "resultado_temp.json": f"resultado_{instance_name}.json",
        #"log_iteracoes.csv": f"log_iteracoes_{instance_name}.csv",
        
        # --- NOSSAS MUDANÇAS AQUI ---
        "report_temp.txt": f"report_final_{instance_name}.txt",  # O relatório limpo
        "log_console_temp.txt": f"log_console_completo_{instance_name}.txt", # O log do Gurobi
        "log_stderr_temp.txt": f"log_erros_{instance_name}.txt", # O log de erros
        # --- FIM DAS MUDANÇAS ---
        
        "model.lp": f"modelo_{instance_name}.lp",
        "modelo_inviavel.ilp": f"modelo_inviavel_{instance_name}.ilp"
    }

    # O resto do script de arquivamento continua...
    for temp_name, final_name in files_to_move.items():
        try:
            if os.path.exists(temp_name):
                shutil.move(temp_name, os.path.join(output_dir, final_name))
                print(f"  - Arquivado: {final_name}")
            else:
                if temp_name not in ["model.lp", "modelo_inviavel.ilp"]:
                    print(f"  - Aviso: Arquivo esperado '{temp_name}' não foi encontrado.")
        except Exception as e:
            print(f"ERRO ao mover {temp_name}: {e}")
            log_file.write(f"{time.ctime()} - ERRO (Arquivamento): {instance_name} - {e}\n")
            log_file.flush()
            
    print(f"--- EXPERIMENTO {instance_name} CONCLUÍDO ---")

# --- 3. EXECUÇÃO ---
if __name__ == "__main__":
    os.makedirs("resultados2", exist_ok=True)
    
    with open("log_geral_execucao.txt", "a", encoding="utf-8") as log_file:
        print(f"Iniciando processo de {len(EXPERIMENTOS)} experimentos...")
        print("Os resultados serão salvos na pasta 'resultados2/'.")
        print("Um log geral está sendo escrito em 'log_geral_execucao.txt'.")
        log_file.write(f"\n\n{time.ctime()} === INICIANDO LOTE DE {len(EXPERIMENTOS)} EXPERIMENTOS ===\n")
        
        for exp in EXPERIMENTOS:
            run_experiment(exp, log_file)
            
        print("\n" + "="*80)
        print("TODOS OS EXPERIMENTOS FORAM CONCLUÍDOS.")
        log_file.write(f"{time.ctime()} === LOTE CONCLUÍDO ===\n")