import gurobipy as gp
from gurobipy import GRB
import time

# Dados completos extraídos do artigo de Thompson (1997)
# "Assigning Telephone Operators to Shifts at New Brunswick Telephone Company"

# --- Mapeamento para facilitar a leitura ---
# Mapeia o número do dia da semana (usado na Tabela 1) para uma string
day_map = {
    1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'
}

# --- Dados da Tabela 1: Funcionários ---
# Chave: ID do Funcionário (E-01 é o mais sênior)
# ST: Horário de início desejado (1=6:00, 2=6:30, ...)
# LL: Duração do almoço desejada (em meias horas, 1=30min, 2=60min)
# ES: Penalidade por início antecipado (por meia hora)
# LS: Penalidade por início tardio (por meia hora)
# SklTyp: Lista de habilidades que o funcionário possui
# MxWk: Máximo de turnos na semana
# UnDay: Lista de dias de folga (indisponível)
"""
    'E-11': {'ST': 1, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-12': {'ST': 4, 'LL': 2, 'ES': 1, 'LS': 1, 'SklTyp': [1,3,10], 'MxWk': 5, 'UnDay': []},
    'E-13': {'ST': 1, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-14': {'ST': 5, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-15': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 2, 'SklTyp': [1,3], 'MxWk': 5, 'UnDay': []},
    'E-16': {'ST': 20, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-17': {'ST': 19, 'LL': 1, 'ES': 12, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-18': {'ST': 4, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[5], day_map[7]]},
    'E-19': {'ST': 19, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[6], day_map[7]]},
    'E-20': {'ST': 6, 'LL': 1, 'ES': 1, 'LS': 6, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-21': {'ST': 19, 'LL': 1, 'ES': 12, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-22': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-23': {'ST': 28, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[1], day_map[1]]}, # E-23 tem UnDay [1,1] no paper, mantido aqui
    'E-24': {'ST': 20, 'LL': 1, 'ES': 1, 'LS': 1.5, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-25': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2,3,4,10], 'MxWk': 5, 'UnDay': [day_map[1], day_map[5]]},
    'E-26': {'ST': 6, 'LL': 2, 'ES': 1, 'LS': 2, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-27': {'ST': 4, 'LL': 1, 'ES': 1.5, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[5]]},
    'E-28': {'ST': 21, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-29': {'ST': 23, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,9], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-30': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-31': {'ST': 24, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-32': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[4], day_map[7]]},
    'E-33': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-34': {'ST': 37, 'LL': 1, 'ES': 1, 'LS': 8, 'SklTyp': [6,7], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-35': {'ST': 20, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,5,9], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-36': {'ST': 19, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[2], day_map[5]]},
    'E-37': {'ST': 11, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-38': {'ST': 22, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,4,5,10,11], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-39': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [4,5,10,11], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-40': {'ST': 37, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [6,7], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-41': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[7]]},
    'E-42': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-43': {'ST': 26, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-44': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-45': {'ST': 7, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-46': {'ST': 37, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [6], 'MxWk': 3, 'UnDay': []},
    'E-47': {'ST': 16, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2,6], 'MxWk': 2, 'UnDay': []},
    'E-48': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2,6], 'MxWk': 2, 'UnDay': []},
    'E-49': {'ST': 19, 'LL': 1, 'ES': 4, 'LS': 2, 'SklTyp': [1,2,6], 'MxWk': 3, 'UnDay': []},
    'E-50': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-51': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-52': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 4, 'UnDay': []},
    'E-53': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[4]]},
    'E-54': {'ST': 19, 'LL': 1, 'ES': 8, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-55': {'ST': 22, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-56': {'ST': 18, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-57': {'ST': 25, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-58': {'ST': 18, 'LL': 1, 'ES': 6, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-59': {'ST': 18, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-60': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-61': {'ST': 3, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2,4], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-62': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-63': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-64': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[7]]},
    'E-65': {'ST': 15, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-66': {'ST': 4, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-67': {'ST': 15, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-68': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-69': {'ST': 17, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-70': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-71': {'ST': 13, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-72': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-73': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 2, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[5]]},
"""

employee_data = {
    'E-01': {'ST': 25, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [9], 'MxWk': 5, 'UnDay': []},
    'E-02': {'ST': 24, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [5], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-03': {'ST': 4, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [2], 'MxWk': 5, 'UnDay': []},
    'E-04': {'ST': 3, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-05': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1, 8], 'MxWk': 5, 'UnDay': [day_map[6], day_map[7]]},
    'E-06': {'ST': 5, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[1], day_map[2]]},
    'E-07': {'ST': 3, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-08': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 2, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[6], day_map[7]]},
    'E-09': {'ST': 37, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,7], 'MxWk': 5, 'UnDay': [day_map[4], day_map[5]]},
    'E-10': {'ST': 3, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []}, 
    'E-11': {'ST': 1, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-12': {'ST': 4, 'LL': 2, 'ES': 1, 'LS': 1, 'SklTyp': [1,3,10], 'MxWk': 5, 'UnDay': []},
    'E-13': {'ST': 1, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-14': {'ST': 5, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-15': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 2, 'SklTyp': [1,3], 'MxWk': 5, 'UnDay': []},
    'E-16': {'ST': 20, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-17': {'ST': 19, 'LL': 1, 'ES': 12, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-18': {'ST': 4, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,8], 'MxWk': 5, 'UnDay': [day_map[5], day_map[7]]},
    'E-19': {'ST': 19, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[6], day_map[7]]},
    'E-20': {'ST': 6, 'LL': 1, 'ES': 1, 'LS': 6, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-21': {'ST': 19, 'LL': 1, 'ES': 12, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-22': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-23': {'ST': 28, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[1], day_map[1]]}, # E-23 tem UnDay [1,1] no paper, mantido aqui
    'E-24': {'ST': 20, 'LL': 1, 'ES': 1, 'LS': 1.5, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-25': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2,3,4,10], 'MxWk': 5, 'UnDay': [day_map[1], day_map[5]]},
    'E-26': {'ST': 6, 'LL': 2, 'ES': 1, 'LS': 2, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-27': {'ST': 4, 'LL': 1, 'ES': 1.5, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[5]]},
    'E-28': {'ST': 21, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-29': {'ST': 23, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,9], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-30': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': []},
    'E-31': {'ST': 24, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[2], day_map[7]]},
    'E-32': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[4], day_map[7]]},
    'E-33': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-34': {'ST': 37, 'LL': 1, 'ES': 1, 'LS': 8, 'SklTyp': [6,7], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-35': {'ST': 20, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,5,9], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-36': {'ST': 19, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[2], day_map[5]]},
    'E-37': {'ST': 11, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': []},
    'E-38': {'ST': 22, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,4,5,10,11], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-39': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [4,5,10,11], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-40': {'ST': 37, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [6,7], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-41': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[7]]},
    'E-42': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-43': {'ST': 26, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[6]]},
    'E-44': {'ST': 4, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2,8], 'MxWk': 5, 'UnDay': [day_map[1], day_map[4]]},
    'E-45': {'ST': 7, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[3]]},
    'E-46': {'ST': 37, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [6], 'MxWk': 3, 'UnDay': []},
    'E-47': {'ST': 16, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2,6], 'MxWk': 2, 'UnDay': []},
    'E-48': {'ST': 19, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2,6], 'MxWk': 2, 'UnDay': []},
    'E-49': {'ST': 19, 'LL': 1, 'ES': 4, 'LS': 2, 'SklTyp': [1,2,6], 'MxWk': 3, 'UnDay': []},
    'E-50': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-51': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-52': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 4, 'UnDay': []},
    'E-53': {'ST': 19, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[4]]},
    'E-54': {'ST': 19, 'LL': 1, 'ES': 8, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-55': {'ST': 22, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-56': {'ST': 18, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-57': {'ST': 25, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-58': {'ST': 18, 'LL': 1, 'ES': 6, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-59': {'ST': 18, 'LL': 1, 'ES': 2.7, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-60': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-61': {'ST': 3, 'LL': 1, 'ES': 1, 'LS': 3, 'SklTyp': [1,2,4], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-62': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-63': {'ST': 7, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-64': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[3], day_map[7]]},
    'E-65': {'ST': 15, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-66': {'ST': 4, 'LL': 1, 'ES': 2, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[1], day_map[7]]},
    'E-67': {'ST': 15, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-68': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-69': {'ST': 17, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 3, 'UnDay': []},
    'E-70': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-71': {'ST': 13, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-72': {'ST': 21, 'LL': 1, 'ES': 4, 'LS': 1, 'SklTyp': [1,2], 'MxWk': 2, 'UnDay': []},
    'E-73': {'ST': 5, 'LL': 1, 'ES': 1, 'LS': 2, 'SklTyp': [1,2], 'MxWk': 5, 'UnDay': [day_map[5]]},
}

# --- Dados da Tabela 3: Características dos Turnos ---
# Chave: SN (ID do Turno)
# ST: Horário de início do turno
# BL: Duração do almoço do turno (em meias horas)
# TT: Habilidade (Toll Type) necessária para o turno
shift_data = {
    1: {'ST': 37, 'BL': 1, 'TT': 6}, 2: {'ST': 37, 'BL': 1, 'TT': 6}, 3: {'ST': 3, 'BL': 1, 'TT': 1},
    4: {'ST': 4, 'BL': 1, 'TT': 1}, 5: {'ST': 4, 'BL': 1, 'TT': 2}, 6: {'ST': 4, 'BL': 2, 'TT': 2},
    7: {'ST': 5, 'BL': 1, 'TT': 1}, 8: {'ST': 5, 'BL': 2, 'TT': 1}, 9: {'ST': 6, 'BL': 1, 'TT': 1},
    10: {'ST': 6, 'BL': 1, 'TT': 1}, 11: {'ST': 6, 'BL': 2, 'TT': 1}, 12: {'ST': 7, 'BL': 1, 'TT': 1},
    13: {'ST': 7, 'BL': 1, 'TT': 1}, 14: {'ST': 7, 'BL': 1, 'TT': 1}, 15: {'ST': 7, 'BL': 1, 'TT': 1},
    16: {'ST': 7, 'BL': 1, 'TT': 1}, 17: {'ST': 7, 'BL': 2, 'TT': 1}, 18: {'ST': 8, 'BL': 1, 'TT': 1},
    19: {'ST': 8, 'BL': 1, 'TT': 1}, 20: {'ST': 10, 'BL': 2, 'TT': 1}, 21: {'ST': 9, 'BL': 1, 'TT': 1},
    22: {'ST': 11, 'BL': 2, 'TT': 1}, 23: {'ST': 19, 'BL': 1, 'TT': 1}, 24: {'ST': 19, 'BL': 1, 'TT': 1},
    25: {'ST': 19, 'BL': 1, 'TT': 1}, 26: {'ST': 19, 'BL': 1, 'TT': 1}, 27: {'ST': 20, 'BL': 1, 'TT': 1},
    28: {'ST': 20, 'BL': 1, 'TT': 1}, 29: {'ST': 23, 'BL': 1, 'TT': 1}, 30: {'ST': 23, 'BL': 1, 'TT': 1},
    31: {'ST': 24, 'BL': 1, 'TT': 1}, 32: {'ST': 24, 'BL': 1, 'TT': 1}, 33: {'ST': 24, 'BL': 1, 'TT': 1},
    34: {'ST': 25, 'BL': 1, 'TT': 2}, 35: {'ST': 25, 'BL': 1, 'TT': 1}, 36: {'ST': 28, 'BL': 1, 'TT': 1},
    37: {'ST': 37, 'BL': 1, 'TT': 6}, 38: {'ST': 37, 'BL': 1, 'TT': 6}, 39: {'ST': 4, 'BL': 1, 'TT': 2},
    40: {'ST': 4, 'BL': 2, 'TT': 1}, 41: {'ST': 5, 'BL': 1, 'TT': 1}, 42: {'ST': 6, 'BL': 1, 'TT': 1},
    43: {'ST': 6, 'BL': 1, 'TT': 1}, 44: {'ST': 7, 'BL': 1, 'TT': 1}, 45: {'ST': 7, 'BL': 1, 'TT': 1},
    46: {'ST': 7, 'BL': 2, 'TT': 1}, 47: {'ST': 8, 'BL': 1, 'TT': 1}, 48: {'ST': 9, 'BL': 6, 'TT': 1},
    49: {'ST': 10, 'BL': 2, 'TT': 1}, 50: {'ST': 11, 'BL': 2, 'TT': 1}, 51: {'ST': 13, 'BL': 2, 'TT': 1},
    52: {'ST': 20, 'BL': 1, 'TT': 1}, 53: {'ST': 20, 'BL': 1, 'TT': 1}, 54: {'ST': 21, 'BL': 1, 'TT': 1},
    55: {'ST': 22, 'BL': 1, 'TT': 1}, 56: {'ST': 24, 'BL': 1, 'TT': 1}, 57: {'ST': 25, 'BL': 1, 'TT': 1},
    58: {'ST': 25, 'BL': 1, 'TT': 2}, 59: {'ST': 25, 'BL': 1, 'TT': 1}, 60: {'ST': 27, 'BL': 1, 'TT': 1},
    61: {'ST': 28, 'BL': 1, 'TT': 1}, 62: {'ST': 37, 'BL': 1, 'TT': 6}, 63: {'ST': 37, 'BL': 1, 'TT': 6},
    64: {'ST': 37, 'BL': 1, 'TT': 6}, 65: {'ST': 4, 'BL': 1, 'TT': 2}, 66: {'ST': 4, 'BL': 2, 'TT': 1},
    67: {'ST': 6, 'BL': 1, 'TT': 1}, 68: {'ST': 6, 'BL': 1, 'TT': 1}, 69: {'ST': 7, 'BL': 1, 'TT': 1},
    70: {'ST': 7, 'BL': 1, 'TT': 1}, 71: {'ST': 7, 'BL': 1, 'TT': 1}, 72: {'ST': 8, 'BL': 1, 'TT': 1},
    73: {'ST': 9, 'BL': 1, 'TT': 1}, 74: {'ST': 11, 'BL': 2, 'TT': 1}, 75: {'ST': 11, 'BL': 2, 'TT': 1},
    76: {'ST': 13, 'BL': 2, 'TT': 1}, 77: {'ST': 19, 'BL': 1, 'TT': 1}, 78: {'ST': 21, 'BL': 1, 'TT': 1},
    79: {'ST': 21, 'BL': 1, 'TT': 1}, 80: {'ST': 21, 'BL': 1, 'TT': 1}, 81: {'ST': 22, 'BL': 1, 'TT': 1},
    82: {'ST': 23, 'BL': 1, 'TT': 1}, 83: {'ST': 23, 'BL': 1, 'TT': 1}, 84: {'ST': 24, 'BL': 1, 'TT': 1},
    85: {'ST': 25, 'BL': 1, 'TT': 2}, 86: {'ST': 26, 'BL': 1, 'TT': 1}, 87: {'ST': 28, 'BL': 1, 'TT': 1},
    88: {'ST': 4, 'BL': 2, 'TT': 4}, 89: {'ST': 5, 'BL': 2, 'TT': 3}, 90: {'ST': 7, 'BL': 2, 'TT': 4},
    91: {'ST': 22, 'BL': 1, 'TT': 11}, 92: {'ST': 24, 'BL': 1, 'TT': 5}, 93: {'ST': 4, 'BL': 2, 'TT': 10},
    94: {'ST': 4, 'BL': 2, 'TT': 8}, 95: {'ST': 24, 'BL': 1, 'TT': 9}, 96: {'ST': 37, 'BL': 1, 'TT': 7}
}

# --- Dados da Tabela 2: Requisitos de Turnos por Dia ---
# Mapeia cada dia para uma lista de IDs de turno que devem ser cobertos
shift_requirements = {
    'Sun': [62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 92, 93, 94, 95, 96],
    'Mon': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 88, 89, 90, 91, 92, 94, 95, 96],
    'Tue': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 88, 89, 90, 91, 92, 94, 95, 96],
    'Wed': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 88, 89, 90, 91, 92, 94, 95, 96],
    'Thu': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 88, 89, 90, 91, 92, 94, 95, 96],
    'Fri': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 87, 88, 89, 90, 91, 92, 94, 95, 96],
    'Sat': [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 87, 92, 93, 94, 95, 96],
}


# --- Estrutura de dados auxiliar ---
# Mapeia cada turno individual para o dia da semana em que ele ocorre
# (Esta foi uma adição sua, mas é redundante com 'shift_requirements', 
# então vamos recriá-la de forma robusta)
day_of_shift_char = {
    shift_id: day for day, shifts in shift_requirements.items() for shift_id in shifts
}


# ############################################################################
#
# --- INÍCIO DO CÓDIGO DE OTIMIZAÇÃO GUROBI ---
#
# ############################################################################

def solve_sap(employee_data, shift_data, shift_requirements):
    """
    Função principal para construir e resolver o Problema de Alocação de Turnos (SAP)
    baseado no Apêndice de Thompson (1997).
    """

    print("Iniciando a preparação do modelo...")
    start_time = time.time()

    # --- 1. Preparação dos Conjuntos (Sets) ---

    # E: Lista de empregados, JÁ ORDENADOS por senioridade
    # A ordem do dicionário é mantida nas versões modernas de Python (3.7+)
    EMPREGADOS = list(employee_data.keys()) # ['E-01', 'E-02', ...]
    print(f"Quantidade de empregados: {len(EMPREGADOS)}")

    # S: Lista de todos os turnos *únicos* (instâncias) a serem cobertos
    # Um turno é definido por (dia, id_caracteristica)
    # Ex: ('Mon', 1) e ('Tue', 1) são dois turnos DIFERENTES
    TURNOS = []
    for day, shift_ids in shift_requirements.items():
        for shift_id in shift_ids:
            TURNOS.append((day, shift_id)) # 's' no modelo é este tuplo
            
    DIAS = list(day_map.values())

    # --- 2. Preparação dos Parâmetros (Parâmetros do Modelo) ---

    # m_e: Máximo de turnos por empregado e
    m = {e: data['MxWk'] for e, data in employee_data.items()}

    # d_s: Dia em que o turno s (o tuplo) ocorre
    d = {s: s[0] for s in TURNOS}

    # c_s: Categoria (skill) do turno s (o tuplo)
    c = {s: shift_data[s[1]]['TT'] for s in TURNOS}

    # C_e: Conjunto de skills (categorias) que o empregado e possui
    C = {e: set(data['SklTyp']) for e, data in employee_data.items()}

    # D_e: Dias que o empregado e PODE trabalhar (disponibilidade)
    all_days = set(DIAS)
    D = {e: all_days - set(data['UnDay']) for e, data in employee_data.items()}

    # v_es: "Indesejabilidade" (custo) do empregado e trabalhar no turno s
    # Este é o cálculo de penalidade descrito no paper
    v = {}
    for e in EMPREGADOS:
        emp_pref = employee_data[e]
        v[e] = {}
        for s in TURNOS:
            s_day, s_id = s
            s_char = shift_data[s_id]
            
            cost = 0
            
            # Penalidade por Horário de Início
            pref_st = emp_pref['ST']
            actual_st = s_char['ST']
            diff = actual_st - pref_st # em unidades de meia hora
            
            if diff > 0: # Início atrasado
                cost += diff * emp_pref['LS']
            elif diff < 0: # Início adiantado
                cost += abs(diff) * emp_pref['ES']
            
            # Penalidade por Duração do Almoço
            if emp_pref['LL'] != s_char['BL']:
                cost += 1.0 # Conforme
            
            v[e][s] = cost

    # arcos_viaveis: Lista de pares (e, s) que são permitidos
    # 1. Empregado 'e' está disponível no dia 'd_s'
    # 2. Empregado 'e' tem o skill 'c_s'
    arcos_viaveis = []
    for e in EMPREGADOS:
        for s in TURNOS:
            if d[s] in D[e] and c[s] in C[e]:
                arcos_viaveis.append((e, s))
                
    # Transforma em Gurobi tuplelist para performance
    arcos_viaveis = gp.tuplelist(arcos_viaveis)

    print(f"Preparação concluída em {time.time() - start_time:.2f}s.")
    print(f"Empregados: {len(EMPREGADOS)}, Turnos a cobrir: {len(TURNOS)}, Arcos viáveis: {len(arcos_viaveis)}")

    # --- 3. Inicialização do Modelo Gurobi ---
    modelo = gp.Model("NBTel_SAP")

    # --- 4. Definição das Variáveis de Decisão ---

    # x_es: 1 se empregado e é alocado ao turno s, 0 caso contrário
    x = modelo.addVars(arcos_viaveis, vtype=GRB.BINARY, name="x")

    # u_s: 1 se o turno s NÃO for alocado, 0 caso contrário
    u = modelo.addVars(TURNOS, vtype=GRB.BINARY, name="u")

    # y_e: 1 se o empregado e for alocado ao seu nº máximo de turnos, 0 caso contrário
    y = modelo.addVars(EMPREGADOS, vtype=GRB.BINARY, name="y")

    # --- 5. Adição das Restrições ---

    print("Construindo restrições...")
    
    # (Eq 2) Atribuir todos os turnos (ou marcar como não atribuído)
    for s in TURNOS:
        modelo.addConstr(x.sum('*', s) + u[s] == 1, name=f"assign_shift_{s[0]}_{s[1]}")

    
    # (Eq 3) Pelo menos um turno para cada empregado
    for e in EMPREGADOS:
        modelo.addConstr(x.sum(e, '*') >= 1, name=f"min_shift_{e}")

    

    # (Eq 4) Não mais que o número máximo de turnos desejado por empregado
    for e in EMPREGADOS:
        modelo.addConstr(x.sum(e, '*') <= m[e], name=f"max_shift_{e}")

    

    # (Eq 5) Não mais que um turno por dia por empregado
    for e in EMPREGADOS:
        for dia in DIAS:
            # Seleciona apenas os arcos (e, s) que ocorrem neste 'dia'
            #turnos_no_dia = x.sum(e, dia, '*') # Rápido com Gurobi tuplelist
            #modelo.addConstr(turnos_no_dia <= 1, name=f"one_per_day_{e}_{dia}")
            turnos_no_dia = gp.quicksum(
                x[e_s] for e_s in arcos_viaveis.select(e, '*')
                if e_s[1][0] == dia  # e_s[1] é o turno 's', e_s[1][0] é o dia
            )
            
            modelo.addConstr(turnos_no_dia <= 1, name=f"one_per_day_{e}_{dia}")
    
#    #(Eq 6 e 7) Restrições de Senioridade
#     for i, e in enumerate(EMPREGADOS):

#         if i==0:
#             modelo.addConstr(y[e] == 1, name=f"link_y_{e}") 
#         # if i==0:

#         # (Eq 6) Vincula a variável y[e] ao total de turnos de 'e'
#         if i > 0: # Aplicável para todos, exceto o mais sênior (i=0)

#             e_anterior = EMPREGADOS[i-1] # O empregado mais sênior
            
#             modelo.addConstr(
#                 x.sum(e, '*') <= 1 + (m[e] - 1) * y[e_anterior],
#                 name=f"seniority_rule_{e}"
#             )
            
#             if x.sum(e, '*') == m[e]:
#                 modelo.addConstr(y[e] == 1, name=f"link_y_{e}")

#         if i < len(EMPREGADOS)-1:
#         # (Eq 7) Restrição de precedência de senioridade
#             modelo.addConstr(m[e] * y[e] <= x.sum(e, '*'), name=f"link_y_{e}")

# (Eq 6 e 7) Restrições de Senioridade
    for i, e in enumerate(EMPREGADOS):
        
        # --- INÍCIO DA CORREÇÃO (FORMULAÇÃO FORTE DA EQ 6) ---
        # Estas duas restrições substituem o seu "if x.sum == m[e]"
        # Elas forçam a ligação: y[e] = 1 se e só se x.sum = m[e]

        # 1. Força y[e] = 1 SE x.sum = m[e]
        #    (Lógica: x.sum <= (m[e] - 1) + y[e])
        #    Se x.sum = 5, a restrição é 5 <= 4 + y[e], o que FORÇA y[e] = 1.
        modelo.addConstr(x.sum(e, '*') <= (m[e] - 1) + y[e], name=f"link_y_upper_{e}")

        # 2. Força y[e] = 0 SE x.sum < m[e]
        #    (Lógica: x.sum >= m[e] * y[e])
        #    Se x.sum = 4, a restrição é 4 >= 5 * y[e], o que FORÇA y[e] = 0.
        modelo.addConstr(x.sum(e, '*') >= m[e] * y[e], name=f"link_y_lower_{e}")
        
        # --- FIM DA CORREÇÃO ---

        # (Eq 7) Restrição de precedência de senioridade
        # Esta regra agora funcionará, pois o y[e_anterior] estará correto.
        if i > 0: 
            e_anterior = EMPREGADOS[i-1] 
            
            modelo.addConstr(
                x.sum(e, '*') <= 1 + (m[e] - 1) * y[e_anterior],
                name=f"seniority_rule_{e}"
            )
    # --- 6. Definição da Função Objetivo (Múltiplos Objetivos) ---
    
    print("Definindo objetivos...")
    
    modelo.ModelSense = GRB.MINIMIZE
    num_objetivos = 0

    # --- Objetivo 1 (Prioridade P0 - A MAIS ALTA) ---
    # Minimizar o número de turnos não alocados
    obj_p0 = u.sum()
    prioridade_p0 = len(EMPREGADOS) + 1 # A maior prioridade
    modelo.setObjectiveN(obj_p0, index=num_objetivos, priority=prioridade_p0, name="MinUnassigned")
    num_objetivos += 1

    #  --- Objetivos 2 a N (Prioridades P1 a PE) ---
    # Satisfazer as preferências dos empregados EM ORDEM DE SENIORIDADE
    for i, e in enumerate(EMPREGADOS):

        obj_pe=0
        
        # Prioridade diminui com a senioridade (i=0 é o mais sênior)
        prioridade_pe = len(EMPREGADOS) - i # P. ex., E-01 tem prioridade 73, E-73 tem prioridade 1
        
        modelo.setObjectiveN(obj_pe, index=num_objetivos, priority=prioridade_pe, name=f"Pref_{e}")
        num_objetivos += 1 
        
    print(f"Modelo construído com {num_objetivos} objetivos.")

    # --- 7. Resolução do Modelo ---
    
    # Parâmetros para otimização de múltiplos objetivos
    # Bloco 1: Encontrar a melhor solução para P0
    # Bloco 2: Corrigir P0 e encontrar a melhor solução para P1 (E-01)
    # Bloco 3: Corrigir P1 e encontrar a melhor para P2 (E-02), etc.
    # O Gurobi faz isso automaticamente.
    
    print("\nIniciando otimização do SAP...")
    modelo.setParam("IntFeasTol", 1e-9)
    modelo.setParam("MIPGap", 0)
    modelo.setParam("FeasibilityTol", 1e-9)
    modelo.optimize()

    # --- 8. Análise dos Resultados ---
    
# --- 8. Análise dos Resultados ---
    
    if modelo.Status == GRB.OPTIMAL:
        print("\n--- SOLUÇÃO ÓTIMA ENCONTRADA ---")
        
        # --- ETAPA DE LEITURA (MOVEMOS ISSO PARA CIMA) ---
        # Primeiro, vamos construir as listas de resultados ANTES de imprimir
        
        turnos_alocados_count = 0
        alocacoes_por_empregado = {e: [] for e in EMPREGADOS}
        
        for e in EMPREGADOS:
            for (e_arco, s_arco) in arcos_viaveis.select(e, '*'): 
                if x[e_arco, s_arco].X > 0.5:
                    alocacoes_por_empregado[e].append(s_arco)
                    turnos_alocados_count += 1
        
        turnos_nao_alocados = []
        for s in TURNOS:
            if u[s].X > 0.5:
                turnos_nao_alocados.append(s)
        
        # --- FIM DA ETAPA DE LEITURA ---
        
        
        # 1. Verificar os valores dos objetivos (AGORA CORRETO)
        print("\nValores dos Objetivos (Hierárquicos):")
        
        # --- CORREÇÃO AQUI ---
        # Usamos o valor real que contamos
        print(f"  P0 (Turnos não alocados): {len(turnos_nao_alocados)}")
        # --- FIM DA CORREÇÃO ---
        
        # Foco nos objetivos P1 a PE
        total_insatisfacao = 0
        for i, e in enumerate(EMPREGADOS):
            modelo.setParam(GRB.Param.ObjNumber, i + 1)
            insatisfacao = modelo.ObjNVal
            total_insatisfacao += insatisfacao

        print(f"  Custo total de insatisfação (soma de P1..PE): {total_insatisfacao:.2f}")

        # 2. Imprimir a alocação de turnos (Agora usando a lista que criamos)
        print("\n--- Alocações por Empregado ---")
        for e, alocados in alocacoes_por_empregado.items():
            print(f"  {e} ({len(alocados)} / {m[e]} turnos): {alocados}")

        # 3. Verificar turnos não alocados (Agora usando a lista que criamos)
        print("\n--- Turnos NÃO Alocados ---")
        if turnos_nao_alocados:
            for s in turnos_nao_alocados:
                print(f"  Turno (Dia: {s[0]}, ID: {s[1]})")
        else:
            print("  Todos os turnos foram alocados!")
            
        print(f"\nVerificação: {turnos_alocados_count} turnos alocados, {len(turnos_nao_alocados)} não alocados. Total: {turnos_alocados_count + len(turnos_nao_alocados)} (de {len(TURNOS)})")
        modelo.write('model.lp')

    elif modelo.Status == GRB.INFEASIBLE:
        print("\nO modelo é inviável.")
        print("Computando IIS (Irreducible Inconsistent Subsystem) para depuração...")
        modelo.computeIIS()
        modelo.write("modelo_inviavel.ilp")
        print("Arquivo 'modelo_inviavel.ilp' escrito. Verifique este arquivo para ver as restrições conflitantes.")
    
    elif modelo.Status == GRB.INF_OR_UNBD:
        print("\nO modelo é inviável ou ilimitado.")

    else:
        print(f"\nOtimização terminada com status: {modelo.Status}")

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Chama a função de resolução principal passando os dados
    solve_sap(employee_data, shift_data, shift_requirements)