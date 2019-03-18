import json
from itertools import chain

from django.db.models.expressions import RawSQL
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from custa.forms import UserForm, UserProfileForm, CustaForm, RequirementForm
from custa.models import Base, Sauce, Top, Custa, Order, OrderCusta, UserProfile
from django.contrib.auth.models import User

context_dict = {}


# Index/about/home page.
def about(request):
    return render(request, 'custa/index.html')


@login_required
# custamise page is used create own custa from base, sauce and top ingredients
def custamise(request):
    user = request.user
    bases = Base.objects.all()
    sauces = Sauce.objects.all()
    tops = Top.objects.all()
    # convert django QuerySet to List so that it can be used in the django templates
    bases_list = list(bases.values())
    sauces_list = list(sauces.values())
    tops_list = list(tops.values())
    # add different variables to the context dictionary
    context_dict['bases'] = bases
    context_dict['bases_list'] = bases_list
    context_dict['sauces'] = sauces
    context_dict['sauces_list'] = sauces_list
    context_dict['tops'] = tops
    context_dict['tops_list'] = tops_list
    # custa form is attached to post request
    if request.method == "POST":
        custa_form = CustaForm(data=request.POST)
        context_dict['custa_form'] = custa_form
        if custa_form.is_valid():
            # commit=false here because the form cannot provide all info relevant to model
            custa = custa_form.save(commit=False)
            custa.user = user
            custa.save()
            # redirect your page to order after creating a new custa
            return HttpResponseRedirect(reverse('order'))
    return render(request, 'custa/custamise.html', context_dict)


@login_required
# this is an amalgamation of custas used to generate an order the order may be composed of preset
# custas as well as user defined custas
def order(request):
    user = request.user
    # get custas whose user_id=0, which are preset custas
    precustas = Custa.objects.filter(user=0)
    # get user's customised custa
    usercustas = Custa.objects.filter(user=user)
    # use chain() to connect the two QuerySets and parse it into list
    custas_list = list(chain(precustas, usercustas))
    context_dict['custa_list'] = custas_list
    return render(request, 'custa/order.html', context_dict)


@login_required
# customised checkout method does not render a page it uses json representation of object to get
# order information and therefore create order
def checkout(request):
    # get the json from the request body
    data = json.loads(request.body)
    # get the info of an order
    id_array = data.get('idArray')
    quantity_array = data.get('quantityArray')
    is_delivery_received = data.get('isDelivery')
    # the total price needs to be multiplied by 100 because it is saved as integer in the database
    total_received = data.get('total') * 100
    # create order
    new_order = Order(user=request.user, is_delivery=is_delivery_received, total=total_received)
    new_order.save()
    # for each custa inside the order, create a responding OrderCusta object (a row in database)
    for i in range(0, len(id_array)):
        OrderCusta.objects.create(quantity=quantity_array[i], custa_id=id_array[i], order=new_order)
    return HttpResponse(json.dumps({"message": "success"}))


@login_required
# shows the order history of the user in a separate page of the web application
# Nested dictionaries are used to simulate representations similar to SQL's "where in..." nested query
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    order_ids = orders.values("id")
    order_custas = OrderCusta.objects.filter(order_id__in=order_ids)
    order_custas_queryset_list = list();
    for o in orders:
        order_custas_queryset_list.append(OrderCusta.objects.filter(order=o))
    context_dict['orders'] = orders
    context_dict['order_custas'] = order_custas
    context_dict['range_of_orders'] = range(0, len(orders))
    context_dict['order_ids'] = order_ids
    context_dict['order_custas_queryset_list'] = order_custas_queryset_list
    return render(request, "custa/order-history.html", context_dict)


@login_required
# my_account page containing user information
def my_account(request):
    userprofile = UserProfile.objects.filter(user=request.user)
    context_dict['userprofile'] = userprofile
    return render(request, "custa/my-account.html", context_dict)


# customised method used to update user personal information
def edit_profile(request):
    data = json.loads(request.body)
    userprofile = UserProfile.objects.get(user=request.user)
    user = User.objects.get(username=request.user.username)
    user.email = data.get('email')
    userprofile.pref_name = data.get('pref_name')
    userprofile.phone = data.get('phone')
    userprofile.address = data.get('address')
    user.save()
    userprofile.save()
    return HttpResponse(json.dumps({"message": "success"}))


# Contact us page.
def contact(request):
    if request.user.id is not None:
        if request.method == 'POST':
            req_form = RequirementForm(data=request.POST)
            context_dict['req_form'] = req_form
            if req_form.is_valid():
                req = req_form.save(commit=False)
                req.user = request.user
                req.save()
    return render(request, 'custa/contact.html', context_dict)


# Register page, also contains a form for submitting user request to the company.
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
            profile.save()
            registered = True
            return HttpResponseRedirect(reverse('index'))
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
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'custa/login.html', {})


# Logout logic.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
