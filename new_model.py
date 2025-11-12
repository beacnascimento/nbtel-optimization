# -*- coding: utf-8 -*-
# Thompson (1997) adaptado às instâncias fornecidas
import gurobipy as gp
from gurobipy import GRB, quicksum

# -------------------------------------------------------------
# 0) DADOS (cole aqui exatamente os dicionários que você enviou)
# -------------------------------------------------------------
day_map = {
    1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'
}

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
for e in E:
    m.addConstr(quicksum(x[e, s] for s in S if (e, s) in ES) >= 1, name=f"atleast1_{e}")

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

if m.status in (GRB.OPTIMAL, GRB.INTERRUPTED):
    print("\nOtimização concluída com sucesso!")

    # --- 1. Processar resultados nas estruturas de dados desejadas ---
    
    # Dicionário: { 'E-01': [s1, s2], 'E-02': [s3] }
    alocacoes_por_empregado = {e: [] for e in E}
    turnos_alocados_count = 0
    
    # Itera sobre as variáveis de alocação (x)
    for (e, s), var in x.items():
        if var.X > 0.5:
            alocacoes_por_empregado[e].append(s)
            turnos_alocados_count += 1

    # Lista: [s4, s5, ...]
    turnos_nao_alocados = []
    
    # Itera sobre as variáveis de turnos não alocados (u)
    for s, var in u.items():
        if var.X > 0.5:
            turnos_nao_alocados.append(s)

    # --- 2. Imprimir a alocação de turnos (Usando as estruturas criadas) ---
    print("\n--- Alocações por Empregado ---")
    for e, alocados in alocacoes_por_empregado.items():
        # Usando m_e[e] do seu script principal
        print(f"  {e} ({len(alocados)} / {m_e[e]} turnos): {alocados}")

    # --- 3. Verificar turnos não alocados (Usando as estruturas criadas) ---
    print("\n--- Turnos NÃO Alocados ---")
    if turnos_nao_alocados:
        for s in turnos_nao_alocados:
            # s é uma tupla (dia, id)
            print(f"  Turno (Dia: {s[0]}, ID: {s[1]})")
    else:
        print("  Todos os turnos foram alocados!")
        
    # --- 4. Verificação final (Usando as estruturas criadas) ---
    # Usando S (conjunto total de ocorrências de turnos) do seu script principal
    print(f"\nVerificação: {turnos_alocados_count} turnos alocados, {len(turnos_nao_alocados)} não alocados. Total: {turnos_alocados_count + len(turnos_nao_alocados)} (de {len(S)})")
    
    # Salva o modelo (opcional, mas estava no seu exemplo)
    m.write('model.lp')
    print("\nModelo salvo em 'model.lp'")


elif m.status == GRB.INFEASIBLE:
    print("\nO modelo é inviável (INFEASIBLE).")
    print("Computando IIS (Irreducible Inconsistent Subsystem) para depuração...")
    m.computeIIS()
    m.write("modelo_inviavel.ilp")
    print("Arquivo 'modelo_inviavel.ilp' escrito. Verifique este arquivo para ver as restrições conflitantes.")

elif m.status == GRB.INF_OR_UNBD:
    print("\nO modelo é inviável ou ilimitado (INF_OR_UNBD).")

else:
    print(f"\nOtimização terminada com status: {m.status}")