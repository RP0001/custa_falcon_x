from itertools import chain

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from custa.forms import UserForm, UserProfileForm, CustaForm
from custa.models import Base, Sauce, Top, Custa

context_dict = {}


# Index/about/home page.
def about(request):
    return render(request, 'custa/about.html')


# Contact us page.
def contact(request):
    return render(request, 'custa/contact.html')


# Custamise page.
def custamise(request):
    user = request.user
    bases = Base.objects.all()
    sauces = Sauce.objects.all()
    tops = Top.objects.all()
    bases_list = list(bases.values())
    sauces_list = list(sauces.values())
    tops_list = list(tops.values())
    context_dict['bases'] = bases
    context_dict['bases_list'] = bases_list
    context_dict['sauces'] = sauces
    context_dict['sauces_list'] = sauces_list
    context_dict['tops'] = tops
    context_dict['tops_list'] = tops_list
    if request.method == "POST":
        custa_form = CustaForm(data=request.POST)
        context_dict['custa_form'] = custa_form
        if custa_form.is_valid():
            custa_form.save(commit=True)

    print(user.username)
    return render(request, 'custa/custamise.html', context_dict)


def order(request):
    user = request.user
    precustas = Custa.objects.filter(user=0)
    usercustas = Custa.objects.filter(user=user)
    custas_list = list(chain(precustas, usercustas))
    context_dict['custa_list'] = custas_list
    return render(request, 'custa/order.html', context_dict)


# Register page.
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'custa/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


# Login page.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('about'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'custa/login.html', {})


# Text when logged in.
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this.")


# Logout logic.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('about'))
