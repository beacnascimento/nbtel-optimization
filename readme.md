# Otimização da Atribuição de Turnos com Prioridade por Senioridade

Este repositório contém a implementação de um modelo de otimização para resolver o Problema de Atribuição de Turnos (*Shift Assignment Problem*), com foco em objetivos hierárquicos baseados na senioridade dos funcionários. O problema-base e os dados foram extraídos do caso de estudo da New Brunswick Telephone Company (NBTel).

## Contexto do Problema

O projeto se baseia em dois artigos fundamentais da área de Pesquisa Operacional:

1.  **Thompson, G. M. (1997). *Assigning Telephone Operators to Shifts at New Brunswick Telephone Company*.**
    - Este artigo seminal define o problema, as regras de negócio, as restrições e, mais importante, a complexa função objetivo com prioridades preemptivas, onde a satisfação dos funcionários é otimizada em estrita ordem de senioridade.

2.  **Hojati, M. (2010). *Near-optimal solution to an employee assignment problem with seniority*.**
    - Este trabalho propõe uma formulação matemática tratável e uma heurística de duas fases baseada em Programação Linear Inteira (PLI) para resolver o problema conceitual de Thompson de forma prática e computacionalmente eficiente.

Nosso objetivo é modelar e resolver este problema, utilizando a formulação de Hojati como base para futuras comparações com outras técnicas, como a metaheurística GRASP.