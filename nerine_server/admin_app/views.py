from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import auth
from django.http import Http404
from django.shortcuts import render
from .db_conn import DBConnection


host = 'localhost'
user = 'newuser'
password = 'password'
db = 'nerine_db'
charset = 'utf8mb4'


def show_tepmlate_main(request):
    return render(request, 'main.html')


def show_tepmlate_admin_auth(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        passwd = request.POST.get('passwd')
        print(login, passwd)
        return HttpResponseRedirect('sites')
    else:
        return render(request, 'admin_auth.html')


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_admins(request):
    page = 'admins'
    context = {'page': page}
    return render(request, 'admins.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_users(request):
    page = 'users'
    context = {'page': page}
    return render(request, 'users.html', context)

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_sites(request):
    page = 'sites'
    data = DBConnection(host, user, password, db, charset)
    sites_list = data.get_list_sites()
    context = {'page': page, 'data': sites_list}
    return render(request, 'sites.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_persons(request):
    page = 'persons'
    data = DBConnection(host, user, password, db, charset)
    persons_list = data.get_list_persons()
    context = {'page': page, 'data': persons_list}
    return render(request, 'persons.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_keywords(request):
    page = 'keywords'
    data = DBConnection(host, user, password, db, charset)
    keywords_list = data.get_list_keywords()
    context = {'page': page, 'data': keywords_list}
    return render(request, 'keywords.html', context)


def login(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        passwd = request.POST.get('passwd')
        user = auth.authenticate(username=login, password=passwd)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'main.html', {'login': login, 'errors': True})
    raise Http404

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
