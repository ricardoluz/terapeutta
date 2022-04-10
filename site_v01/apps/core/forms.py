# from datetime import date, datetime
import datetime
from email import message
from pyexpat.errors import messages
from tkinter import PIESLICE

from django import forms
from django.contrib import messages
from django.forms import ValidationError
from django.forms.widgets import DateInput
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper

from .models import Terapeuta, Paciente, Movimentacao, TipoOperacao
from ..bibliotecas.validar_cpf import verificar_cpf

# from crispy_forms.layout import Submit
from crispy_forms.layout import (
    Layout,
    Fieldset,
    Field,
    ButtonHolder,
    Submit,
    MultiField,
    Div,
    Field,
    Button,
    Column,
    Row,
    HTML,
    Reset,
)
from crispy_forms.bootstrap import (
    FormActions,
    InlineCheckboxes,
    InlineRadios,
    PrependedText,
)


class TerapeutaFormCrispy(forms.ModelForm):
    class Meta:
        model = Terapeuta
        fields = ["nome", "sobrenome", "apelido"]  # , "email", "password1", "password2"
        # fields = "__all__"

    nome = forms.CharField(
        label="Nome",
        max_length=80,
        required=True,
    )
    sobrenome = forms.CharField(
        label="Sobrenome",
        max_length=40,
        required=True,
    )
    apelido = forms.CharField(
        label=" Apelido",
        max_length=40,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-Alteracao_Terapeuta"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_action = "submit_survey"

        self.helper.layout = Layout(
            Fieldset(
                "Alteração de dados",
                Row(
                    Column("nome", css_class="form-group col-md-6 mb-0"),
                    Column("sobrenome", css_class="form-group col-md-6 mb-0"),
                ),
                "apelido",
                ButtonHolder(Submit("submit", "Submit", css_class="button white")),
                # FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
            )
        )


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente

        fields = [
            "nome",
            "sobrenome",
            "apelido",
            "modo_pagamento",
            "valor_padrao",
            "cpf",
            "identidade",
            "email",
            "celular_ddd",
            "celular_numero",
            "telefone_ddd",
            "telefone_numero",
            "nome_responsavel",
            "cpf_responsavel",
            "email_responsavel",
            "celular_ddd_responsavel",
            "celular_numero_responsavel",
            "telefone_ddd_responsavel",
            "telefone_numero_responsavel",
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "paciente_responsavel",
        ]

    # Definição dos validadores.
    vld_numerico = RegexValidator(r"^[0-9+]", " Digite números.")
    vld_telefone = RegexValidator(r"(\d{5}|\d{4}|\d{3})[-. ]?\d{4}", "Número inválido ")

    # Definição dos campos
    nome = forms.CharField(
        label="Nome",
        max_length=80,
        required=True,
    )

    sobrenome = forms.CharField(
        label="Sobrenome",
        max_length=40,
        required=True,
    )
    apelido = forms.CharField(
        label="Apelido",
        max_length=40,
        required=False,
    )

    modo_pagamento = forms.CharField(
        label="Modo Pagamento",
        max_length=15,
        required=False,
    )

    valor_padrao = forms.FloatField(
        label="Consulta",
        min_value=0.0,
        initial=100.0,
        required=False,
    )

    cpf = forms.CharField(
        label="CPF Paciente",
        max_length=11,
        required=False,
    )

    identidade = forms.CharField(
        label="Identidade Paciente",
        max_length=11,
        required=False,
    )

    email = forms.EmailField(label="Email", required=True)

    celular_ddd = forms.CharField(
        label="DDD",
        max_length=3,
        required=True,
        validators=[vld_numerico],
        # help_text='Utilize...'
    )

    celular_numero = forms.CharField(
        label="Celular", max_length=11, required=True, validators=[vld_telefone]
    )

    telefone_ddd = forms.CharField(
        label="DDD", max_length=3, required=False, validators=[vld_numerico]
    )

    telefone_numero = forms.CharField(
        label="Telefone", max_length=11, required=False, validators=[vld_telefone]
    )

    cpf_responsavel = forms.CharField(
        label="CPF Responsável",
        max_length=11,
        required=False,
    )

    nome_responsavel = forms.CharField(
        label="Nome do Responsável",
        max_length=90,
        required=False,
    )

    # Dados do responsável
    # ---------------------
    email_responsavel = forms.EmailField(label="Email", required=False)

    celular_ddd_responsavel = forms.CharField(
        label="DDD",
        max_length=3,
        required=False,
        validators=[vld_numerico],
        # help_text='Utilize...'
    )

    celular_numero_responsavel = forms.CharField(
        label="Celular", max_length=11, required=False, validators=[vld_telefone]
    )

    telefone_ddd_responsavel = forms.CharField(
        label="DDD", max_length=3, required=False, validators=[vld_numerico]
    )

    telefone_numero_responsavel = forms.CharField(
        label="Telefone", max_length=11, required=False, validators=[vld_telefone]
    )

    # Endereço do paciente
    # --------------------
    cep = forms.CharField(
        label="CEP",
        max_length=8,
        required=False,
    )

    endereco = forms.CharField(
        label="Endereco",
        max_length=60,
        required=False,
    )

    numero = forms.CharField(
        label="Núm.",
        max_length=20,
        required=False,
    )

    complemento = forms.CharField(
        label="Complemento",
        max_length=40,
        required=False,
    )

    bairro = forms.CharField(
        label="Bairro",
        max_length=60,
        required=False,
    )

    cidade = forms.CharField(
        label="Cidade",
        max_length=60,
        required=False,
    )

    uf = forms.CharField(
        label="UF",
        max_length=2,
        required=False,
        error_messages={"error": "Enter whether your name has changed"},
    )

    # Campos auxiliares
    # -----------------

    paciente_responsavel = forms.ChoiceField(
        choices=((True, "Sim"), (False, "Não")),
        initial=True,
        widget=forms.RadioSelect,
        label="É responsável?",
        # help_text="This includes changing your last name or spelling your name differently.",
        # error_messages={"required": "Enter whether your name has changed"},
    )

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-Alteracao_Terapeuta"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_action = "submit_survey"

        self.helper.layout = Layout(
            Fieldset(
                "Dados do paciente",
                Row(
                    Column("nome", css_class="form-group col-md-3 mb-0"),
                    Column("sobrenome", css_class="form-group col-md-6 mb-0"),
                    Column("apelido", css_class="form-group col-md-3 mb-0"),
                ),
                Row(
                    Column("cpf", css_class="form-group col-md-2 mb-0"),
                    Column(
                        InlineRadios("paciente_responsavel"),
                        css_class="form-group col-md-2 mb-0",
                    ),
                    Column("identidade", css_class="form-group col-md-4 mb-0"),
                    Column("modo_pagamento", css_class="form-group col-md-2 mb-0"),
                    Column(
                        PrependedText("valor_padrao", "R$", ".00"),
                        css_class="form-group col-md-2 mb-0",
                    ),
                ),
                Row(
                    Column("email", css_class="form-group col-md-4 mb-0"),
                    Column("celular_ddd", css_class="form-group col-md-1 mb-0"),
                    Column("celular_numero", css_class="form-group col-md-3 mb-0"),
                    Column("telefone_ddd", css_class="form-group col-md-1 mb-0"),
                    Column("telefone_numero", css_class="form-group col-md-3 mb-0"),
                ),
                Div(
                    Row(
                        Column(
                            "nome_responsavel", css_class="form-group col-md-9 mb-0"
                        ),
                        Column("cpf_responsavel", css_class="form-group col-md-3 mb-0"),
                    ),
                    Row(
                        Column(
                            "email_responsavel", css_class="form-group col-md-4 mb-0"
                        ),
                        Column(
                            "celular_ddd_responsavel",
                            css_class="form-group col-md-1 mb-0",
                        ),
                        Column(
                            "celular_numero_responsavel",
                            css_class="form-group col-md-3 mb-0",
                        ),
                        Column(
                            "telefone_ddd_responsavel",
                            css_class="form-group col-md-1 mb-0",
                        ),
                        Column(
                            "telefone_numero_responsavel",
                            css_class="form-group col-md-3 mb-0",
                        ),
                    ),
                    style="background: #fafaf3;",
                    title="Dados do responsável",
                    css_class="bigdivs",
                    id="div_responsavel",
                ),
                Row(
                    Column("cep", css_class="form-group col-md-2 mb-0"),
                    Column("endereco", css_class="form-group col-md-6 mb-0"),
                    Column("numero", css_class="form-group col-md-1 mb-0"),
                    Column("complemento", css_class="form-group col-md-3 mb-0"),
                ),
                Row(
                    Column("bairro", css_class="form-group col-md-4 mb-0"),
                    Column("cidade", css_class="form-group col-md-4 mb-0"),
                    Column("uf", css_class="form-group col-md-1 mb-0"),
                ),
                # ButtonHolder(Submit("submit", "Submit", css_class="button white")),
                FormActions(
                    Submit("submit", "Salvar dados"),
                    Reset("Reset", "Dados iniciais"),
                    Button(
                        "cancel",
                        "Voltar",
                        onclick="window.history.back();return false;",
                    ),
                ),
                # InlineRadios("paciente_responsavel"),
                # FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
            )
        )

    def clean_cpf(self):
        data = self.cleaned_data["cpf"]

        if data is None or len(data) == 0:
            return data

        if not verificar_cpf(data):
            # If not, raise an error
            raise ValidationError("CPF inválido.")

        # Return data even though it was not modified
        return data

    def clean_cpf_responsavel(self):
        data = self.cleaned_data["cpf_responsavel"]

        if data is None or len(data) == 0:
            return data

        if not verificar_cpf(data):
            # If not, raise an error
            raise ValidationError("CPF inválido.")

        # Return data even though it was not modified
        return data

    # def clean(self) -> Optional[Mapping[str, Any]]:
    def clean(self):

        data_form = self.data

        # Validar existencia do CPF Paciente.
        if data_form["paciente_responsavel"] == "True" and len(data_form["cpf"]) == 0:
            raise ValidationError("CPF do paciente precisa ser preeenchido.")

        # Validar existencia dados do responsável.
        if data_form["paciente_responsavel"] == "False":
            msgerro = ["Preenha os campos do Responsável:"]

            if len(data_form["nome_responsavel"]) == 0:
                msgerro.append("  - Nome")

            if len(data_form["cpf_responsavel"]) == 0:
                msgerro.append("  - CPF")

            if len(data_form["email_responsavel"]) == 0:
                msgerro.append("  - E-mail")

            if len(data_form["celular_ddd_responsavel"]) == 0:
                msgerro.append("  - DDD do celular")

            if len(data_form["celular_numero_responsavel"]) == 0:
                msgerro.append("  - Número do celular")

            # if len(data_form["telefone_ddd_responsavel"]) == 0:
            #     msgerro.append("  - DDD do telefone")

            # if len(data_form["telefone_numero_responsavel"]) == 0:
            #     msgerro.append("  - Número de telefone")

            if len(msgerro) > 1:
                raise ValidationError(msgerro)

        return super().clean()
        return data_form


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao

        fields = [
            "tipo_operacao",
            "data_hora",
            "valor_mov",
        ]

    tipo_operacao = forms.ModelChoiceField(
        queryset=TipoOperacao.objects.all(), label="Operação"
    )

    data_hora = forms.DateField(
        input_formats=["%d/%m/%Y", "%Y-%m-%d"],
        label="Data",
        initial=datetime.date.today().strftime("%Y-%m-%d"),
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        localize=True,
    )

    valor_mov = forms.FloatField(
        label="Valor",
        min_value=0.0,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(MovimentacaoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-Movimentacao"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_action = "submit_survey"

        self.helper.layout = Layout(
            Fieldset(
                "Movimentação",
                Row(
                    Column("tipo_operacao", css_class="form-group col-md-3 mb-0"),
                    Column("data_hora", css_class="form-group col-md-2 mb-0"),
                    PrependedText(
                        "valor_mov", "R$", ".00", css_class="form-group col-md-6 mb-0"
                    ),
                ),
                FormActions(
                    Submit("submit", "Salvar movimento"),
                    Button(
                        "cancel",
                        "Voltar",
                        onclick="window.history.back();return false;",
                    ),
                ),
            )
        )
