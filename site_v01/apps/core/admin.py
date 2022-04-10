from django.contrib import admin
from site_v01.apps.core.models import Terapeuta, Paciente, Movimentacao, TipoOperacao

admin.site.register(Terapeuta)
admin.site.register(Paciente)
admin.site.register(Movimentacao)
admin.site.register(TipoOperacao)
