def tema(request):
    tema_atual = request.session.get("tema", "dia")
    return {
        "tema": tema_atual,
        "tema_proximo": "noite" if tema_atual == "dia" else "dia",
    }