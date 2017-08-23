from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .db_conn import DBConnection


host = 'localhost'
user = 'newuser'
password = 'password'
db = 'nerine_db'
charset = 'utf8mb4'


def show_tepmlate_admin_auth(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        passwd = request.POST.get('passwd')
        print(login, passwd)
        return HttpResponseRedirect('sites')
    else:
        return render(request, 'admin_auth.html')


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
    data = DBConnection(host, user, password, db, charset)
    sites_list = data.get_list_sites()
    context = {'page': page, 'data': sites_list}
    return render(request, 'sites.html', context)


def show_tepmlate_persons(request):
    page = 'persons'
    data = DBConnection(host, user, password, db, charset)
    persons_list = data.get_list_persons()
    context = {'page': page, 'data': persons_list}
    return render(request, 'persons.html', context)


def show_tepmlate_keywords(request):
    page = 'keywords'
    data = DBConnection(host, user, password, db, charset)
    keywords_list = data.get_list_keywords()
    context = {'page': page, 'data': keywords_list}
    return render(request, 'keywords.html', context)
