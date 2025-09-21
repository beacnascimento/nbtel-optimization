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
    'E-23': {'ST': 28, 'LL': 1, 'ES': 3, 'LS': 1, 'SklTyp': [1], 'MxWk': 5, 'UnDay': [day_map[1], day_map[1]]},
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
day_of_shift = {
    shift: day for day, shifts in shift_requirements.items() for shift in shifts
}