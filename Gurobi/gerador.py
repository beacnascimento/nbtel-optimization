# -*- coding: utf-8 -*-
import random
import argparse
import sys

def gerar_instancia(args):
    """
    Função principal que gera os dados da instância com base nos argumentos.
    """
    
    # ---------------------------------------------------
    # 1. PARÂMETROS DE GERAÇÃO (vindos dos args)
    # ---------------------------------------------------
    N_EMPLOYEES = args.n_employees
    N_SHIFTS_PER_DAY = args.n_shifts
    N_SKILLS = args.n_skills
    MAX_SKILLS_PER_EMP = args.max_skills
    MIN_SKILLS_PER_EMP = args.min_skills
    MAX_UNAVAILABLE_DAYS = args.max_unavailable
    MAX_MXWK = 5
    MIN_MXWK = 4
    N_DAYS = 7
    
    # ---------------------------------------------------
    # 2. GERAÇÃO DOS DADOS
    # ---------------------------------------------------
    
    days_list = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    day_map = {i+1: day for i, day in enumerate(days_list)}

    # --- Geração de Habilidades (Skills) ---
    skill_ids = list(range(1, N_SKILLS + 1))
    # Peso: 10 para habilidades comuns, 1 para raras
    skill_weights = [10 if s <= 5 else (5 if s <= 10 else 1) for s in skill_ids]

    # --- Geração do employee_data ---
    employee_data = {}
    for i in range(1, N_EMPLOYEES + 1):
        eid = f'E-{i:03d}' # Formato E-001, E-002, ...
        
        num_skills = random.randint(MIN_SKILLS_PER_EMP, MAX_SKILLS_PER_EMP)
        
        # Lógica de amostragem ponderada (melhorada)
        # Garante que as habilidades dos funcionários sigam a mesma
        # distribuição de peso que as habilidades dos turnos.
        skills_set = set()
        k_sample = max(num_skills, num_skills * 2) 
        weighted_sample = random.choices(skill_ids, weights=skill_weights, k=k_sample)
        skills_set.update(weighted_sample)

        if len(skills_set) >= num_skills:
            skills = sorted(random.sample(list(skills_set), num_skills))
        else:
            skills = sorted(list(skills_set))

        if not skills:
            skills = [random.choices(skill_ids, weights=skill_weights, k=1)[0]]
        
        num_unavailable = random.randint(0, MAX_UNAVAILABLE_DAYS)
        unavailable_days = sorted(random.sample(days_list, num_unavailable))
        
        employee_data[eid] = {
            'ST': random.randint(1, 40),
            'LL': random.choice([1, 2]),
            'ES': round(random.uniform(1.0, 5.0), 1),
            'LS': round(random.uniform(1.0, 5.0), 1),
            'SklTyp': skills,
            'MxWk': random.randint(MIN_MXWK, MAX_MXWK),
            'UnDay': unavailable_days
        }

    # --- Geração de shift_data e shift_requirements ---
    shift_data = {}
    shift_requirements = {day: [] for day in days_list}
    shift_counter = 1

    for day in days_list:
        for _ in range(N_SHIFTS_PER_DAY):
            shift_id = shift_counter
            shift_requirements[day].append(shift_id)
            
            shift_data[shift_id] = {
                'ST': random.randint(1, 40),
                'BL': random.choice([1, 2]),
                'TT': random.choices(skill_ids, weights=skill_weights, k=1)[0]
            }
            shift_counter += 1

    # ---------------------------------------------------
    # 3. IMPRESSÃO NO ARQUIVO TEMPORÁRIO
    # ---------------------------------------------------
    
    # O 'run_all.py' espera que este script escreva SEMPRE
    # neste arquivo 'instancia_temp.py'.
    nome_do_arquivo = 'instancia_temp.py'
    
    try:
        with open(nome_do_arquivo, 'w', encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write(f"\n# Instância Gerada (via gerador.py)\n")
            f.write(f"# Parâmetros: {vars(args)}\n")

            f.write("\nday_map = {\n")
            for k, v in day_map.items():
                f.write(f"    {k}: '{v}',\n")
            f.write("}\n")

            f.write("\nemployee_data = {\n")
            for k, v in employee_data.items():
                f.write(f"    '{k}': {v},\n")
            f.write("}\n")

            f.write("\nshift_data = {\n")
            for k, v in shift_data.items():
                f.write(f"    {k}: {v},\n")
            f.write("}\n")

            f.write("\nshift_requirements = {\n")
            for k, v in shift_requirements.items():
                f.write(f"    '{k}': {v},\n")
            f.write("}\n")
    except Exception as e:
        print(f"Erro ao escrever arquivo de instância: {e}")
        sys.exit(1) # Sinaliza um erro

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Instâncias para o Modelo de Otimização")
    
    # --- Argumentos com valores padrão (baseados na sua baseline) ---
    parser.add_argument('--n-employees', type=int, default=180, help='Número de funcionários')
    parser.add_argument('--n-shifts', type=int, default=60, help='Número de turnos POR DIA')
    parser.add_argument('--n-skills', type=int, default=8, help='Número total de habilidades')
    parser.add_argument('--max-skills', type=int, default=5, help='Max de habilidades por funcionário')
    parser.add_argument('--min-skills', type=int, default=2, help='Min de habilidades por funcionário')
    parser.add_argument('--max-unavailable', type=int, default=1, help='Max de dias indisponíveis')
    
    args = parser.parse_args()
    
    # Imprime no console (para o log do run_all) o que está fazendo
    print(f"Gerando 'instancia_temp.py' com params: {vars(args)}")
    gerar_instancia(args)
    print("Geração concluída.")