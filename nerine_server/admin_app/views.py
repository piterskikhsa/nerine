from django.shortcuts import render


def show_tepmlate_sites(request):
    page = 'sites'
    return render(request, 'sites.html', {'page': page})


def show_tepmlate_persons(request):
    page = 'persons'
    return render(request, 'persons.html', {'page': page})


def show_tepmlate_keywords(request):
    page = 'keywords'
    return render(request, 'keywords.html', {'page': page})
