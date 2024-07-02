from django.shortcuts import render


# For testing. changer it alter
apes = [{"id": 1, "name": "azir"}, {"id": 2, "name": "jax"}, {"id": 3, "name": "kaisa"}]


def home(request):
    context = {"apes": apes}
    return render(request, "base/home.html", context)


def zoo(request):
    return render(request, "base/zoo.html")


def ape(request, pk):
    ape = None
    for i in apes:
        if i["id"] == int(pk):
            ape = i
    context = {"ape": ape}
    return render(request, "base/ape.html", context)
