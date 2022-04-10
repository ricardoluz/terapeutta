def multiplicador(fator_1: list, fator_2: list):
    soma = sum(fator_1[i] * fator_2[i] * 10 for i in range(len(fator_1)))
    return soma % 11


def verificar_cpf(valor: str) -> bool:

    if len(valor) != 11:
        return False

    cpf_digitado = [int(x) for x in list(valor)]
    cpf_calculado = [int(x) for x in valor[0:9]]

    multiplicador_p10 = list(range(10, 1, -1))
    multiplicador_p11 = list(range(11, 1, -1))

    cpf_calculado.append(multiplicador(multiplicador_p10, cpf_calculado))
    cpf_calculado.append(multiplicador(multiplicador_p11, cpf_calculado))

    return cpf_digitado == cpf_calculado


# lista=['00310591713','00310591716','59372265004']

# for i in lista:
#     print(i, verificar_cpf(i))
