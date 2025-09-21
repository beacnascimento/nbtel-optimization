# modelo.py

# A biblioteca PuLP é excelente para modelagem, pois permite escrever as
# equações matemáticas de forma muito parecida com a notação formal.
import pulp

# Importa os dicionários de dados do seu arquivo de instâncias.
# Garanta que 'instancias.py' esteja na mesma pasta que este arquivo.
from instances import employee_data, shift_data, shift_requirements, day_of_shift

def definir_modelo_base():
    """
    Esta função define a estrutura do problema de otimização da NBTel,
    incluindo as variáveis de decisão e todas as restrições operacionais.

    Ela não define uma função objetivo final, pois isso será feito pelo
    solver para implementar a abordagem hierárquica.

    Retorna:
        prob (pulp.LpProblem): O objeto do problema, contendo as restrições.
        x (dict): Dicionário com as variáveis de decisão x_es.
        u (dict): Dicionário com as variáveis de decisão u_s.
    """
    print("--- [Modelo] Iniciando a definição da estrutura do problema ---")

    # --- 1. Preparação dos Conjuntos de Dados ---
    # Obtém listas de funcionários, turnos e dias para facilitar as iterações.
    employees = list(employee_data.keys())
    #print(employees)
    all_shifts = list(shift_data.keys())
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # --- 2. Inicialização do Modelo ---
    # Cria o objeto do problema. O nome é para identificação e LpMinimize
    # é o tipo de otimização (embora o objetivo específico mude depois).
    prob = pulp.LpProblem("Modelo_Base_NBTel", pulp.LpMinimize)
    print("[Modelo] Objeto do problema PuLP inicializado.")

    # --- 3. Definição das Variáveis de Decisão ---
    # x_es: Binária. 1 se funcionário 'e' é alocado ao turno 's', 0 caso contrário.
    x = pulp.LpVariable.dicts("x", (employees, all_shifts), 0, 1, pulp.LpBinary)

    # u_s: Binária. 1 se o turno 's' não for coberto, 0 caso contrário.
    # Esta variável é usada para medir a violação da cobertura de turnos.
    u = pulp.LpVariable.dicts("u", all_shifts, 0, 1, pulp.LpBinary)
    print(f"[Modelo] Variáveis de decisão 'x' e 'u' criadas.")

    # --- 4. Definição das Restrições ---
    # Aqui traduzimos todas as regras de negócio para equações matemáticas.
    print("[Modelo] Adicionando restrições...")

    # Restrição 1: Cobertura de Turnos (Hojati, Equação 2)
    # Para cada turno 's', a soma de todos os funcionários alocados a ele mais
    # a variável de 'não cobertura' (u_s) deve ser igual a 1.
    # Isso garante que um turno ou é coberto por 1 funcionário, ou é marcado como não coberto.
    for s in all_shifts:
        prob += pulp.lpSum(x[e][s] for e in employees) + u[s] == 1, f"Cobertura_Turno_{s}"

    # Restrição 2: Carga Horária Semanal Máxima (Hojati, Equação 3)
    # Para cada funcionário 'e', a soma de todos os turnos atribuídos a ele
    # durante a semana não pode exceder seu máximo permitido (MxWk).
    for e in employees:
        prob += pulp.lpSum(x[e][s] for s in all_shifts) <= employee_data[e]['MxWk'], f"Max_Turnos_Semana_{e}"

    # Restrição 3: Um Turno por Dia (Hojati, Equação 4)
    # Para cada funcionário 'e' e para cada dia 'd' da semana, a soma dos turnos
    # atribuídos a ele naquele dia não pode ser maior que 1.
    for e in employees:
        for day in days:
            shifts_on_day = [s for s in all_shifts if day_of_shift.get(s) == day]
            if shifts_on_day:
                prob += pulp.lpSum(x[e][s] for s in shifts_on_day) <= 1, f"Max_Um_Turno_Dia_{e}_{day}"

    # Restrições 4 e 5: Compatibilidade de Habilidade e Disponibilidade
    # Estas são restrições lógicas que fixam certas variáveis x_es em 0.
    for e in employees:
        for s in all_shifts:
            # Verifica se o funcionário tem a habilidade necessária para o turno.
            habilidade_necessaria = shift_data[s]['TT']
            habilidades_do_funcionario = employee_data[e]['SklTyp']
            if habilidade_necessaria not in habilidades_do_funcionario:
                prob += x[e][s] == 0, f"Incompatibilidade_Habilidade_{e}_{s}"

            # Verifica se o funcionário está de folga no dia do turno.
            dia_do_turno = day_of_shift.get(s)
            dias_de_folga = employee_data[e]['UnDay']
            if dia_do_turno in dias_de_folga:
                prob += x[e][s] == 0, f"Indisponibilidade_Folga_{e}_{s}"

    print("[Modelo] Todas as restrições foram adicionadas com sucesso.")

    # Retorna os componentes essenciais para que o solver possa usá-los
    return prob, x, u

# --- Bloco de Execução Principal ---
# Este bloco só será executado quando você rodar 'python modelo.py' diretamente.
# Ele serve para testar se a construção do modelo está funcionando.
if __name__ == "__main__":
    # Chama a função para criar a estrutura do modelo
    modelo_base, variaveis_x, variaveis_u = definir_modelo_base()

    # Imprime um resumo do modelo criado para verificação
    print("\n--- [Teste] Resumo do Modelo Base Estruturado ---")
    print(f"Nome do Problema: {modelo_base.name}")
    print(f"Número de Variáveis: {len(modelo_base.variables())}")
    print(f"  - Variáveis 'x' (atribuições): {len(variaveis_x) * len(variaveis_x['E-01'])}")
    print(f"  - Variáveis 'u' (não cobertura): {len(variaveis_u)}")
    print(f"Número de Restrições: {len(modelo_base.constraints)}")
    print("\n[Teste] O modelo foi construído com sucesso e está pronto para ser passado para um solver.")

    # Opcional: Para inspecionar todas as equações geradas, você pode descomentar a linha abaixo.
    # Isso criará um arquivo de texto com o modelo matemático completo.
    # modelo_base.writeLP("ModeloNBTel.lp")
    # print("\n[Teste] Modelo salvo em 'ModeloNBTel.lp' para análise detalhada.")