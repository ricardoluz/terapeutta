from django.shortcuts import redirect


def somente_usuario_nao_autenticado(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users_v01(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # Roles vazia: Apenas logado.
            if allowed_roles == [] and request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            group = None
            permissao = False
            if request.user.groups.exists():
                group = [n.name for n in request.user.groups.all()]

                for g in group:
                    for r in allowed_roles:
                        if g == r:
                            permissao = True

            if permissao:
                return view_func(request, *args, **kwargs)
            else:
                # return HttpResponse("You are not authorized to view this page")
                return redirect("home")

        return wrapper_func

    return decorator

