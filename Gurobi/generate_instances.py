import random

# ---------------------------------------------------
# 1. PARÂMETROS DE GERAÇÃO
# ---------------------------------------------------


# --- Escala (Tamanho) ---
# Aumentamos os funcionários para ter mais recursos
N_EMPLOYEES = 250       # +30 funcionários
N_SHIFTS_PER_DAY = 90   # Demanda total: 420 turnos
N_DAYS = 7

# --- Dificuldade (Conflito) ---
N_SKILLS = 8            # Menos habilidades raras
MAX_SKILLS_PER_EMP = 5  # Funcionários mais qualificados
MIN_SKILLS_PER_EMP = 2  # Ninguém tem apenas 1 habilidade
MAX_UNAVAILABLE_DAYS = 1 # <-- ESTA É A MUDANÇA MAIS IMPORTANTE
MAX_MXWK = 5            
MIN_MXWK = 4
# ---------------------------------------------------
# 2. GERAÇÃO DOS DADOS
# ---------------------------------------------------
print("Gerando nova instância...")

days_list = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
day_map = {i+1: day for i, day in enumerate(days_list)}

# --- Geração de Habilidades (Skills) ---
# Vamos criar um "peso" para as habilidades.
# Habilidades de 1 a 5 são comuns. Habilidades > 10 são raras.
skill_ids = list(range(1, N_SKILLS + 1))
# Peso: 10 para habilidades comuns, 1 para raras
skill_weights = [10 if s <= 5 else (5 if s <= 10 else 1) for s in skill_ids]


# --- Geração do employee_data ---
employee_data = {}
for i in range(1, N_EMPLOYEES + 1):
    eid = f'E-{i:03d}' # Formato E-001, E-002, ...
    
    # Quantas habilidades este funcionário terá?
    num_skills = random.randint(MIN_SKILLS_PER_EMP, MAX_SKILLS_PER_EMP)
    # Quais habilidades?
    skills = sorted(random.sample(skill_ids, num_skills))
    
    # Quantos dias indisponíveis?
    num_unavailable = random.randint(0, MAX_UNAVAILABLE_DAYS)
    unavailable_days = sorted(random.sample(days_list, num_unavailable))
    
    employee_data[eid] = {
        'ST': random.randint(1, 40),          # Preferência de início
        'LL': random.choice([1, 2]),          # Preferência de almoço
        'ES': round(random.uniform(1.0, 5.0), 1), # Penalidade "early"
        'LS': round(random.uniform(1.0, 5.0), 1), # Penalidade "late"
        'SklTyp': skills,
        'MxWk': random.randint(MIN_MXWK, MAX_MXWK),
        'UnDay': unavailable_days
    }

# --- Geração de shift_data e shift_requirements ---
# Vamos criar IDs de turno únicos para cada ocorrência exigida
shift_data = {}
shift_requirements = {day: [] for day in days_list}
shift_counter = 1

for day in days_list:
    for _ in range(N_SHIFTS_PER_DAY):
        shift_id = shift_counter
        
        # Adiciona o ID à lista de exigências daquele dia
        shift_requirements[day].append(shift_id)
        
        # Cria os dados para esse ID de turno
        shift_data[shift_id] = {
            'ST': random.randint(1, 40), # Horário de início do turno
            'BL': random.choice([1, 2]), # Duração do almoço
            # Qual habilidade este turno exige?
            # Usamos 'choices' com 'weights' para tornar habilidades raras
            # igualmente raras nas exigências.
            'TT': random.choices(skill_ids, weights=skill_weights, k=1)[0]
        }
        shift_counter += 1


# ---------------------------------------------------
# 3. IMPRESSÃO DOS DICIONÁRIOS
# ---------------------------------------------------
# (Pronto para copiar e colar no seu script principal)

print("\n# -*- coding: utf-8 -*-")
print(f"\n# Instância Gerada: {N_EMPLOYEES} funcionários, {shift_counter - 1} ocorrências de turno total")

print("\nday_map = {")
for k, v in day_map.items():
    print(f"    {k}: '{v}',")
print("}\n")

print("employee_data = {")
for k, v in employee_data.items():
    print(f"    '{k}': {v},")
print("}\n")

print("shift_data = {")
for k, v in shift_data.items():
    print(f"    {k}: {v},")
print("}\n")

print("shift_requirements = {")
for k, v in shift_requirements.items():
    print(f"    '{k}': {v},")
print("}\n")

print("--- Geração Concluída ---")
total_shifts_required = (shift_counter - 1)
avg_shifts_per_emp = total_shifts_required / N_EMPLOYEES
print(f"Total de turnos exigidos: {total_shifts_required}")
print(f"Carga média por funcionário: {avg_shifts_per_emp:.2f} turnos/semana")