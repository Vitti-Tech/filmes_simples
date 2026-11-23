from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Filme
from django.utils.http import url_has_allowed_host_and_scheme

def lista(request):
    tema = request.session.get("tema", "dia")
    if tema == "dia":
        tema_proximo = "noite"
    else:
        tema_proximo = "dia"
    filmes = Filme.objects.order_by("assistido", "titulo")
    return render(
        request,"filmes/lista.html",
    {
        "filmes": filmes,
        "tema": tema,
        "tema_proximo": tema_proximo,
    }
            )

def novo(request):
    return render(request, "filmes/novo.html")


@require_POST
def alterar_tema(request):
    tema_atual = request.session.get("tema", "dia")
    request.session["tema"] = "noite" if tema_atual == "dia" else "dia"

    destino = request.META.get("HTTP_REFERER", "")
    if destino and url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}
    ):
        return redirect(destino)
    return redirect("lista")
@require_POST
def salvar_novo(request):
    Filme.objects.create(
        titulo=request.POST["titulo"],
        genero=request.POST["genero"],
        ano=request.POST["ano"],
        assistido="assistido" in request.POST,
    )
    return redirect("lista")

def editar(request, id):
    filme = get_object_or_404(Filme, id=id)
    
    return render(request, "filmes/editar.html",
        {"filme": filme})

@require_POST
def salvar_edicao(request, id):
    filme = get_object_or_404(Filme, id=id)
    filme.titulo = request.POST["titulo"]
    filme.genero = request.POST["genero"]
    filme.ano = request.POST["ano"]
    filme.assistido = "assistido" in request.POST
    filme.save()
    
    return redirect("lista")

@require_POST
def excluir(request, id):
    filme = get_object_or_404(Filme, id=id)
    filme.delete()
    return redirect("lista")
