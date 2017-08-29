from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import Http404
from .forms import RegistrationForm
from base.models import Site, Person, KeyWord


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
    admins = User.objects.all()
    data = []
    for admin in admins:
        if admin.is_superuser:
            data.append(admin)
    context = {'page': page, 'data': data}
    return render(request, 'admins.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_users(request):
    page = 'users'
    users = User.objects.all()
    data = []
    for user in users:
        if not user.is_superuser:
            data.append(user)
    context = {'page': page, 'data': data}
    return render(request, 'users.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_sites(request):
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        site_name = Site(Name=site_name)
        site_name.save()
    page = 'sites'
    data = Site.objects.all()
    context = {'page': page, 'data': data}
    return render(request, 'sites.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_persons(request):
    if request.method == 'POST':
        person_name = request.POST.get('person_name')
        person_name = Person(Name=person_name)
        person_name.save()
    page = 'persons'
    data = Person.objects.all()
    context = {'page': page, 'data': data}
    return render(request, 'persons.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def show_tepmlate_keywords(request):
    if request.method == 'POST':
        keyword_name = request.POST.get('keyword_name')
        keyword_choice = request.POST.get('select')
        new_keyword = KeyWord()
        new_keyword.Name = keyword_name
        new_keyword.PersonID = Person.objects.get(id=keyword_choice)
        new_keyword.save()

    page = 'keywords'
    data = KeyWord.objects.all()
    persons = Person.objects.all()
    context = {'page': page, 'data': data, 'persons': persons}
    return render(request, 'keywords.html', context)


def users_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'users_reg.html', context)
    context = {'form': RegistrationForm()}
    return render(request, 'users_reg.html', context)


def admins_registration(request):
    pass


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


def delete_admin(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return HttpResponseRedirect('/users/')


def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return HttpResponseRedirect('/users/')


def delete_site(request, id):
    site = get_object_or_404(Site, id=id)
    site.delete()
    return HttpResponseRedirect('/sites/')


def delete_person(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return HttpResponseRedirect('/persons/')


def delete_keyword(request, id):
    keyword = get_object_or_404(KeyWord, id=id)
    keyword.delete()
    return HttpResponseRedirect('/keywords/')

