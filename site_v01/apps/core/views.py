""" core - Views """
import datetime
import os
from django.utils import timezone
from django.forms import ValidationError, modelformset_factory
import requests
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q


from ..autenticacao.decorators import allowed_users_v01
from .decorators import terapeuta_eh_valido

from .forms import OSSelecaoForm, TerapeutaFormCrispy, PacienteForm, MovimentacaoForm
from .models import (
    QryListaOrdensServico, 
    Terapeuta,
    Paciente,
    Movimentacao,
    OrdemServico,
    QryMovimentacao,
    QryMovimentacaoAgregada
)
from ..bibliotecas.validar_cpf import verificar_cpf


def home(request):
    return render(request, "core/home.html")


def erro_01(request):
    return render(request, "erros/terapeuta_nao_autorizado.html")

def teste(request):
    return render(request, "core/popup.html")

def ler_api_cep(cep: str) -> dict:
    # https://www.delftstack.com/howto/python/python-get-json-from-url/

    url = requests.get("https://ws.apicep.com/cep.json?code=" + cep).text
    dados_cep = {}
    try:
        dados_cep = json.loads(url)
        # return dados_cep
    except:
        raise Exception("Erro no CEP")

    finally:
        return dados_cep


@allowed_users_v01()
@terapeuta_eh_valido
def alterar_terapeuta_view(request, id):
    context = {}
    terapeuta = Terapeuta.objects.get(id=id)

    if request.method == "POST":
        form = TerapeutaFormCrispy(request.POST, instance=terapeuta)
        if form.is_valid():
            form.save()
    else:
        form = TerapeutaFormCrispy(instance=terapeuta)

    # Add the formset to context dictionary
    context["form"] = form
    return render(request, "core/teste.html", context)


@allowed_users_v01()
def listar_pacientes(request):
    """Mostrar todos os pacientes"""
    pacientes = Paciente.objects.filter(terapeuta=request.user.terapeuta).order_by(
        "nome"
    )
    context = {"form": pacientes}
    return render(request, "core/pacientes.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def editar_paciente_v01(request, id_paciente):
    """Cria / Edita um paciente"""
    if id_paciente == 0:
        paciente = None
    else:
        paciente = Paciente.objects.get(id=id_paciente)


    if request.method != "POST":
        # Formulário em branco ou com dados iniciais do paciente.
        form = PacienteForm(instance=paciente)
    else:
        # Dados de POST submetidos; processa os dados
        form = PacienteForm(request.POST, instance=paciente)

        if (
            Paciente.objects.filter(
                apelido=form.data["apelido"], terapeuta=request.user.terapeuta.id
            )
            .exclude(id=id_paciente)
            .exists()
            and
            len(form.data["apelido"])>0
        ):

            form.add_error(
                field="apelido",
                error=ValidationError("Há outro paciente com este apelido."),
            )

        if form.is_valid():
            paciente = form.save(commit=False)
            paciente.terapeuta = request.user.terapeuta
            paciente.save()
            return HttpResponseRedirect(reverse("core_listar_pacientes"))

    context = {"form": form, "paciente_id": id_paciente}

    return render(request, "core/paciente_dados.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def excluir_paciente(request, id_paciente):
    query = Paciente.objects.get(id=id_paciente)
    query.delete()

    return redirect(request.META['HTTP_REFERER'])


@allowed_users_v01()
@terapeuta_eh_valido
def listar_movimentacoes(request, id_paciente):

    paciente = Paciente.objects.get(id=id_paciente)
    movimentos = QryMovimentacao.objects.filter(paciente=id_paciente)

    context = {"form": movimentos}
    context["id_paciente"] = id_paciente
    context["nome_paciente"] =  paciente.nome

    return render(request, "core/movimentos.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def criar_movimentacao(request, id_paciente):
    """Cria uma movimentacao"""

    paciente = Paciente.objects.get(id=id_paciente)

    if request.method == "POST":
        # form = MovimentacaoForm(request.POST, instance=movimentacao)
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            movimentacao = form.save(commit=False)

            movimentacao.paciente = paciente
            movimentacao.terapeuta_id = request.user.terapeuta.id

            movimentacao.save()

            return HttpResponseRedirect(reverse("core_listar_pacientes"))

    else:

        movimentacao = None
        form = MovimentacaoForm(instance=movimentacao)
        
        # Ler o valor padrão da consulta
        form.fields['valor_mov'].initial = paciente.valor_padrao

    context = {"form": form}
    return render(request, "core/movimentacao.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def editar_movimento(request, id_movimento):

    movimento = Movimentacao.objects.get(id=id_movimento)

    if request.method != "POST":
        # Formulário em branco ou com dados iniciais do paciente.
        form = MovimentacaoForm(instance=movimento)
    else:
        # Dados de POST submetidos; processa os dados
        form = MovimentacaoForm(request.POST, instance=movimento)

        if form.is_valid():
            movimento = form.save(commit=False)
            movimento.save()

            return redirect("core_listar_movimentos", id_paciente=movimento.paciente_id)

    context = {"form": form}

    return render(request, "core/movimentacao.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def excluir_movimento(request, id_movimento):
    query = Movimentacao.objects.get(id=id_movimento)

    query.delete()

    return redirect(request.META['HTTP_REFERER'])


@allowed_users_v01()
def os_selecionar_movimentos_tmp(request, id_paciente):

    paciente = Paciente.objects.get(id=id_paciente)
    form = Movimentacao.objects.filter(paciente=id_paciente).order_by("data_hora")

    if request.method != "POST":
        # form = Movimentacao.objects.filter(paciente=id_paciente).order_by("data_hora")
        print('Leitura')
    else:
        # values = [value for name, value in request.POST.iteritems()]
        for item in request.POST.keys():
            print(item)
        print(len(request.POST))
        # form = request.POST
        tmp = request.POST
        for item in tmp:
            print(item)

        print('*'*80)    

    context = {"form": form, "id_paciente": id_paciente}
    context["nome_paciente"] =  paciente.nome

    return render(request, "core/os_selecionar_movimentos.html", context)


@allowed_users_v01()
def os_listar_movimentos_agregados(request):
    """Listar os movimentos para criação de OS"""

    movimentos_agregados = QryMovimentacaoAgregada.objects.filter(terapeuta_id=request.user.terapeuta.id)

    context = {"form": movimentos_agregados}
    return render(request, "core/os_movimentos_agregados.html", context)


@allowed_users_v01()
# @terapeuta_eh_valido
def os_listar_ordensservico(request):
    terapeuta=request.user.terapeuta
    ordens = QryListaOrdensServico.objects.filter(terapeuta_id = terapeuta.id)

    context = {"form": ordens}

    return render(request, "core/os_listar_ordens.html", context)


@allowed_users_v01()
@terapeuta_eh_valido
def os_selecionar_movimentos(request, id_paciente):
    OrdemSet = modelformset_factory(Movimentacao,OSSelecaoForm,extra=0)

    paciente = Paciente.objects.get(id=id_paciente)
    os_aberta = OrdemServico.objects.filter(paciente=id_paciente, data_envio = None).order_by('data_ordem')
    num_os = None
    bln_existe_os = False

    # Se existir um OS aberta, acrescentar dados a ela.
    # 
    if os_aberta:
        num_os = os_aberta.all().values()[0]['id']
        bln_existe_os = True
        movimentos = Movimentacao.objects.filter(Q(paciente=id_paciente) & (Q(bln_selecionado=0) | Q(ordem_servico = num_os))).order_by("data_hora")
    else:
        movimentos = Movimentacao.objects.filter(paciente=id_paciente).filter(bln_selecionado=0).order_by("data_hora")


    if request.method != 'POST':
        formset = OrdemSet(queryset=movimentos)
    else:
        formset = OrdemSet(request.POST)
        itens_selecionados = []
        if formset.is_valid():

            for form in formset:
                if form.cleaned_data.get('bln_selecionado'):
                    itens_selecionados.append(form.cleaned_data['id'].id)

            if len(itens_selecionados) > 0 and bln_existe_os == False:
                os_nova = OrdemServico(paciente=paciente, data_ordem= timezone.localtime())
                os_nova.save()
                num_os = os_nova.pk

            #TODO: Verificar uma forma de executar através do formulário.
            for tmp in movimentos:
                if tmp.id in itens_selecionados:
                    tmp.ordem_servico_id = num_os
                    tmp.bln_selecionado = True
                else:
                    tmp.ordem_servico_id = None
                    tmp.bln_selecionado = False
                
                tmp.save()

            return redirect("home")
            return render(request,'core/os_selecionar_movimentos_tmp.html',{'formset':formset})
    
    context = {"formset": formset, "nome_paciente": paciente.nome}
    
    return render(request,'core/os_selecionar_movimentos.html', context)

# ----------------------------------
# Views de verificacao.

def verificar_apelido(request):
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "GET"
    ):
        apelido = request.GET.get("apelido", None)
        apelido_inicial = request.GET.get("apelido_inicial", None)
        if apelido != apelido_inicial:
            if Paciente.objects.filter(
                apelido=apelido, terapeuta=request.user.terapeuta.id
            ).exists():
                # if Paciente.objects.filter(apelido=apelido).exists():
                return JsonResponse({"valid": False}, status=200)
            else:
                # if nick_name not found, then user can create a new friend.
                return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


def validar_CPF(request):
    """Validação de CPF"""
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "GET"
    ):
        # get the nick name from the client side.
        cpf = request.GET.get("cpf", None)
        # check for the nick name in the database.
        if verificar_cpf(cpf) or len(cpf) == 0:
            return JsonResponse({"valid": True}, status=200)
        else:
            return JsonResponse({"valid": False}, status=200)

    return JsonResponse({}, status=400)


def ler_cep(request):
    """Ler dados do CEP"""
    if (
        request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
        and request.method == "GET"
    ):
        # get the nick name from the client side.
        cep = request.GET.get("cep", None)
        # check for the nick name in the database.
        dados_cep = ler_api_cep(cep)
        print(dados_cep)
        if len(dados_cep) > 0:
            dados_cep["valid"] = True
            return JsonResponse(dados_cep, status=200)
        else:
            return JsonResponse({"valid": False}, status=400)

    return JsonResponse({}, status=400)


# class TerapeutaCreateView(CreateView):
#     form_class = TerapeutaForm
#     template_name = 'core/teste.html'
#     model = Terapeuta
#     success_url = '/'

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         # book_form = BookFormset()
#         # book_formhelper = BookFormHelper()

#         return self.render_to_response(
#             # self.get_context_data(form=form, book_form=book_form)
#             self.get_context_data(form=form)
#         )

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         # book_form = BookFormset(self.request.POST)

#         # if (form.is_valid() and book_form.is_valid()):
#             # return self.form_valid(form, book_form)
#         if (form.is_valid()):
#             return self.form_valid(form)

#         # return self.form_invalid(form, book_form)
#         return self.form_invalid(form=form_class)

#     # def form_valid(self, form, book_form):
#     def form_valid(self, form):
#         """
#         Called if all forms are valid. Creates a Author instance along
#         with associated books and then redirects to a success page.
#         """
#         self.object = form.save()
#         # book_form.instance = self.object
#         # book_form.save()

#         return HttpResponseRedirect(self.get_success_url())

#     # def form_invalid(self, form, book_form):
#     def form_invalid(self, form):
#         """
#         Called if whether a form is invalid. Re-renders the context
#         data with the data-filled forms and errors.
#         """
#         return self.render_to_response(
#             # self.get_context_data(form=form, book_form=book_form)
#             self.get_context_data(form=form)
#         )

#     def get_context_data(self, **kwargs):
#         """ Add formset and formhelper to the context_data. """
#         # ctx = super(AuthorCreateView, self).get_context_data(**kwargs)
#         ctx = super(TerapeutaCreateView, self).get_context_data(**kwargs)
#         # book_formhelper = BookFormHelper()

#         if self.request.POST:
#             # ctx['form'] = AuthorForm(self.request.POST)
#             ctx['form'] = TerapeutaForm(self.request.POST)
#             # ctx['book_form'] = BookFormset(self.request.POST)
#             # ctx['book_formhelper'] = book_formhelper
#         else:
#             # ctx['form'] = AuthorForm()
#             ctx['form'] = TerapeutaForm()
#             # ctx['book_form'] = BookFormset()
#             # ctx['book_formhelper'] = book_formhelper

#         return ctx


# -------------------------
