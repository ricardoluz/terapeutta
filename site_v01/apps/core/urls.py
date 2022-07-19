from django.urls import path, include
from .views import (
    home,
    teste,
    alterar_terapeuta_view,
    erro_01,
    # ---------
    # Paciente
    listar_pacientes,
    editar_paciente_v01,
    excluir_paciente,
    verificar_apelido,
    #
    # -----------
    # Movimentos
    criar_movimentacao,
    editar_movimento,
    excluir_movimento,
    listar_movimentacoes,
    #
    # ------------
    # Ordem de serviço
    os_selecionar_movimentos,
    os_listar_ordensservico,
    #
    # ------------
    # Validações
    validar_CPF,
    ler_cep,
)

urlpatterns = [
    path("", home, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("erro", erro_01, name="erro_01"),
    path("teste", teste, name="teste"),
    path(
        "alterar_dados/<int:id>",
        alterar_terapeuta_view,
        name="core_alterar_dados_terapeuta",
    ),
    path("pacientes", listar_pacientes, name="core_listar_pacientes"),
    path(
        "paciente/<int:id_paciente>", editar_paciente_v01, name="core_editar_paciente"
    ),
    path(
        "excluir/paciente/<int:id_paciente>",
        excluir_paciente,
        name="core_excluir_paciente",
    ),
    #
    path("get/ajax/validate/apelido", verificar_apelido, name="verificar_apelido"),
    path("get/ajax/validate/cpf", validar_CPF, name="validar_CPF"),
    path("get/ajax/validate/cep", ler_cep, name="ler_cep"),
    path(
        "movimentos/<int:id_paciente>",
        listar_movimentacoes,
        name="core_listar_movimentos",
    ),
    path(
        "criar_movimento/<int:id_paciente>",
        criar_movimentacao,
        name="core_criar_movimentacao",
    ),
    path(
        "editar_movimento/<int:id_movimento>",
        editar_movimento,
        name="core_editar_movimento",
    ),
    path(
        "excluir_movimento/<int:id_movimento>",
        excluir_movimento,
        name="core_excluir_movimento",
    ),
    #
    # OrdemServico --------------------------------------------
    #
    path(
        "ordemservico/<int:id_paciente>",
        os_selecionar_movimentos,
        name="core_os_selecionar_movimentos",
    ),
        path(
        "ordemservico",
        os_listar_ordensservico,
        name="core_listar_ordensservico",
    ),


]
