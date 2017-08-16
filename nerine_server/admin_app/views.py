from django.shortcuts import render


def show_tepmlate_admins(request):
    page = 'admins'
    context = {'page': page}
    return render(request, 'admins.html', context)

def show_tepmlate_users(request):
    page = 'users'
    context = {'page': page}
    return render(request, 'users.html', context)

def show_tepmlate_sites(request):
    page = 'sites'
    fake_data = ['www.mail.ru', 'www.yandex.ru', 'www.rambler.ru', 'www.google.com', 'www.yahoo.com']
    context = {'page': page, 'data': fake_data}
    return render(request, 'sites.html', context)


def show_tepmlate_persons(request):
    page = 'persons'
    fake_data = ['Путин', 'Медведев', 'Навальный', 'Трамп']
    context = {'page': page, 'data': fake_data}
    return render(request, 'persons.html', context)


def show_tepmlate_keywords(request):
    page = 'keywords'
    fake_data = ['Путин', 'Путина', 'Путину',
                 'Медведев', 'Медведева', 'Медведеву',
                 'Навальный', 'Навальнова', 'Навальному',
                 'Трамп', 'Трампа', 'Трампу']
    context = {'page': page, 'data': fake_data}
    return render(request, 'keywords.html', context)
