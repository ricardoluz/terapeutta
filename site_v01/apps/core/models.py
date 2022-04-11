""" Modelos """
from email.utils import formatdate
from re import T
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User


class Terapeuta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True)
    sobrenome = models.CharField(max_length=150, blank=True)
    apelido = models.CharField(max_length=50, blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    num_conselho = models.CharField(max_length=10, blank=True)
    regiao_conselho = models.CharField(max_length=4, blank=True)

    def __str__(self):
        return self.nome


class Paciente(models.Model):
    terapeuta = models.ForeignKey(Terapeuta, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    nome = models.CharField(max_length=50, blank=True)
    sobrenome = models.CharField(max_length=150, blank=True)
    apelido = models.CharField(max_length=50, blank=True)

    cpf = models.CharField(max_length=11, blank=True)
    identidade = models.CharField(max_length=40, blank=True)
    modo_pagamento = models.CharField(max_length=15, blank=True)
    valor_padrao = models.FloatField(null=True, blank=True, default=None)

    email = models.EmailField(null=True, blank=True)
    celular_ddd = models.CharField(null=True, blank=True, max_length=3)
    celular_numero = models.CharField(null=True, blank=True, max_length=11)
    telefone_ddd = models.CharField(null=True, blank=True, max_length=3)
    telefone_numero = models.CharField(null=True, blank=True, max_length=11)

    cep = models.CharField(max_length=8, blank=True)
    endereco = models.CharField(max_length=60, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=40, blank=True)
    bairro = models.CharField(max_length=60, blank=True)
    cidade = models.CharField(max_length=60, blank=True)
    uf = models.CharField(max_length=2, blank=True)

    paciente_responsavel = models.BooleanField(blank=False, default=False)

    nome_responsavel = models.CharField(max_length=90, blank=True)
    cpf_responsavel = models.CharField(max_length=11, blank=True)

    email_responsavel = models.EmailField(null=True, blank=True)
    celular_ddd_responsavel = models.CharField(null=True, blank=True, max_length=3)
    celular_numero_responsavel = models.CharField(null=True, blank=True, max_length=11)
    telefone_ddd_responsavel = models.CharField(null=True, blank=True, max_length=3)
    telefone_numero_responsavel = models.CharField(null=True, blank=True, max_length=11)

    def __str__(self):
        return self.nome


class TipoOperacao(models.Model):
    class SinalOperacao(models.IntegerChoices):
        NEGATIVO = -1, "Negativo"
        NEUTRO = 0, "Neutro"
        POSITIVO = 1, "Positivo"

    tipo_operacao = models.AutoField(primary_key=True)
    desc_operacao = models.CharField(unique=True, max_length=40)
    sinal_operacao = models.SmallIntegerField(choices=SinalOperacao.choices)

    class Meta:
        verbose_name = "TipoOperacao"
        verbose_name_plural = "TipoOperacoes"

    def __str__(self):
        return self.desc_operacao


class Movimentacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True)
    tipo_operacao = models.ForeignKey(TipoOperacao, null=False, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(null=True)
    valor_mov = models.FloatField(null=True, blank=True)  # TODO: Rever este campo.
    observacao = models.TextField(null=True, blank=True, max_length=120)


