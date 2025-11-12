# thompson_instance.py
from typing import Dict, List, Tuple, Set

class ThompsonInstance:
    """
    Prepara a instância de Thompson:
    - Empregados E (ordem de senioridade)
    - Ocorrências de turno S = (day, sid)
    - Elegibilidade ES = {(e,s)}
    - Parâmetros por e e por s
    """
    def __init__(self, employee_data: Dict, shift_data: Dict, shift_requirements: Dict, lambda_lunch: float = 0.0):
        self.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
        def emp_key(eid): return int(eid.split('-')[1])

        self.employee_data = employee_data
        self.shift_data = shift_data
        self.shift_requirements = shift_requirements
        self.lambda_lunch = float(lambda_lunch)

        # empregados por senioridade
        self.E: List[str] = sorted(list(employee_data.keys()), key=emp_key)
        self.pos = {e:i for i,e in enumerate(self.E)}

        self.ST_e = {e: employee_data[e]['ST'] for e in self.E}
        self.LL_e = {e: employee_data[e]['LL'] for e in self.E}
        self.ES_e = {e: employee_data[e]['ES'] for e in self.E}
        self.LS_e = {e: employee_data[e]['LS'] for e in self.E}
        self.Ce_e = {e: set(employee_data[e]['SklTyp']) for e in self.E}
        self.m_e  = {e: employee_data[e]['MxWk'] for e in self.E}
        self.Un_e = {e: set(employee_data[e]['UnDay']) for e in self.E}
        self.De_e = {e: set(self.days) - self.Un_e[e] for e in self.E}

        # ocorrências de turno
        self.S: List[Tuple[str,int]] = [(day, sid) for day, ids in shift_requirements.items() for sid in ids]
        self.ST_s = {(day, sid): shift_data[sid]['ST'] for day, sid in self.S}
        self.BL_s = {(day, sid): shift_data[sid]['BL'] for day, sid in self.S}
        self.TT_s = {(day, sid): shift_data[sid]['TT'] for day, sid in self.S}
        self.day_of = {(day, sid): day for day, sid in self.S}

        # elegibilidade básica
        self.ES: Set[Tuple[str,Tuple[str,int]]] = {
            (e, s) for e in self.E for s in self.S
            if (self.TT_s[s] in self.Ce_e[e]) and (self.day_of[s] in self.De_e[e])
        }

    # insatisfação v_es
    def v_es(self, e, s) -> float:
        ste, sts = self.ST_e[e], self.ST_s[s]
        if sts < ste:
            pen = self.ES_e[e] * (ste - sts)
        else:
            pen = self.LS_e[e] * (sts - ste)
        pen += self.lambda_lunch * abs(self.BL_s[s] - self.LL_e[e])
        return float(pen)
