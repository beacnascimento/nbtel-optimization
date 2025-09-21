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
    10: {'ST': 6, 'BL': 1, 'TT': 1}, 11: {'ST': 6, 'BL': 2, 'TT': 2}, 12: {'ST': 6, 'BL': 2, 'TT': 2},
    13: {'ST': 13, 'BL': 1, 'TT': 1}, 14: {'ST': 13, 'BL': 2, 'TT': 1}, 15: {'ST': 14, 'BL': 1, 'TT': 1},
    16: {'ST': 14, 'BL': 2, 'TT': 1}, 17: {'ST': 15, 'BL': 1, 'TT': 4}, 18: {'ST': 15, 'BL': 2, 'TT': 4},
    19: {'ST': 16, 'BL': 1, 'TT': 4}, 20: {'ST': 16, 'BL': 2, 'TT': 4}, 21: {'ST': 17, 'BL': 1, 'TT': 4},
    22: {'ST': 17, 'BL': 1, 'TT': 4}, 23: {'ST': 17, 'BL': 2, 'TT': 4}, 24: {'ST': 17, 'BL': 2, 'TT': 4},
    25: {'ST': 18, 'BL': 1, 'TT': 4}, 26: {'ST': 18, 'BL': 1, 'TT': 4}, 27: {'ST': 18, 'BL': 2, 'TT': 4},
    28: {'ST': 18, 'BL': 2, 'TT': 4}, 29: {'ST': 24, 'BL': 1, 'TT': 3}, 30: {'ST': 24, 'BL': 1, 'TT': 5},
    31: {'ST': 25, 'BL': 1, 'TT': 5}, 32: {'ST': 28, 'BL': 1, 'TT': 8}, 33: {'ST': 29, 'BL': 1, 'TT': 8},
    34: {'ST': 30, 'BL': 1, 'TT': 8}, 35: {'ST': 32, 'BL': 1, 'TT': 8}, 36: {'ST': 32, 'BL': 1, 'TT': 0},
    37: {'ST': 3, 'BL': 1, 'TT': 1}, 38: {'ST': 4, 'BL': 1, 'TT': 1}, 39: {'ST': 4, 'BL': 1, 'TT': 1},
    40: {'ST': 5, 'BL': 1, 'TT': 1}, 41: {'ST': 6, 'BL': 1, 'TT': 1}, 42: {'ST': 13, 'BL': 1, 'TT': 1},
    43: {'ST': 14, 'BL': 1, 'TT': 1}, 44: {'ST': 15, 'BL': 1, 'TT': 4}, 45: {'ST': 15, 'BL': 2, 'TT': 4},
    46: {'ST': 16, 'BL': 1, 'TT': 4}, 47: {'ST': 16, 'BL': 2, 'TT': 4}, 48: {'ST': 17, 'BL': 1, 'TT': 4},
    49: {'ST': 17, 'BL': 1, 'TT': 4}, 50: {'ST': 17, 'BL': 2, 'TT': 4}, 51: {'ST': 18, 'BL': 1, 'TT': 4},
    52: {'ST': 18, 'BL': 1, 'TT': 4}, 53: {'ST': 18, 'BL': 2, 'TT': 4}, 54: {'ST': 24, 'BL': 1, 'TT': 3},
    55: {'ST': 24, 'BL': 1, 'TT': 5}, 56: {'ST': 25, 'BL': 1, 'TT': 5}, 57: {'ST': 28, 'BL': 1, 'TT': 8},
    58: {'ST': 29, 'BL': 1, 'TT': 8}, 59: {'ST': 30, 'BL': 1, 'TT': 8}, 60: {'ST': 32, 'BL': 1, 'TT': 8},
    61: {'ST': 32, 'BL': 1, 'TT': 0}, 62: {'ST': 37, 'BL': 1, 'TT': 6}, 63: {'ST': 37, 'BL': 1, 'TT': 6},
    64: {'ST': 37, 'BL': 1, 'TT': 6}, 65: {'ST': 15, 'BL': 1, 'TT': 4}, 66: {'ST': 15, 'BL': 2, 'TT': 4},
    67: {'ST': 16, 'BL': 1, 'TT': 4}, 68: {'ST': 16, 'BL': 2, 'TT': 4}, 69: {'ST': 17, 'BL': 1, 'TT': 4},
    70: {'ST': 17, 'BL': 1, 'TT': 4}, 71: {'ST': 17, 'BL': 2, 'TT': 4}, 72: {'ST': 17, 'BL': 2, 'TT': 4},
    73: {'ST': 18, 'BL': 1, 'TT': 4}, 74: {'ST': 18, 'BL': 1, 'TT': 4}, 75: {'ST': 18, 'BL': 1, 'TT': 4},
    76: {'ST': 18, 'BL': 2, 'TT': 4}, 77: {'ST': 18, 'BL': 2, 'TT': 4}, 78: {'ST': 18, 'BL': 2, 'TT': 4},
    79: {'ST': 19, 'BL': 1, 'TT': 4}, 80: {'ST': 19, 'BL': 1, 'TT': 4}, 81: {'ST': 19, 'BL': 1, 'TT': 4},
    82: {'ST': 19, 'BL': 2, 'TT': 4}, 83: {'ST': 19, 'BL': 2, 'TT': 4}, 84: {'ST': 24, 'BL': 1, 'TT': 3},
    85: {'ST': 24, 'BL': 1, 'TT': 5}, 86: {'ST': 25, 'BL': 1, 'TT': 5}, 87: {'ST': 19, 'BL': 1, 'TT': 7},
    88: {'ST': 19, 'BL': 1, 'TT': 7}, 89: {'ST': 20, 'BL': 1, 'TT': 4}, 90: {'ST': 20, 'BL': 1, 'TT': 4},
    91: {'ST': 20, 'BL': 2, 'TT': 4}, 92: {'ST': 26, 'BL': 1, 'TT': 9}, 93: {'ST': 31, 'BL': 1, 'TT': 9},
    94: {'ST': 33, 'BL': 1, 'TT': 9}, 95: {'ST': 35, 'BL': 1, 'TT': 9}, 96: {'ST': 41, 'BL': 1, 'TT': 9}
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