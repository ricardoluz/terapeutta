"""
    Decorators para a aplicação core (Terapeuta)
"""
from django.shortcuts import redirect, HttpResponse
from site_v01.apps.core.models import Paciente, Movimentacao


def terapeuta_eh_valido(view_func):
    def wrapper_func(request, *args, **kwargs):

        terapeuta_id = request.user.terapeuta.id

        if "id_paciente" in kwargs and kwargs["id_paciente"]!=0:
            if Paciente.objects.get(id=kwargs["id_paciente"]).terapeuta.id != terapeuta_id:
                return redirect("erro_01")

        if "id_movimento" in kwargs:
            if Movimentacao.objects.get(id=kwargs["id_movimento"]).paciente.terapeuta.id != terapeuta_id:
                return redirect("erro_01")

        return view_func(request, *args, **kwargs)

    return wrapper_func
