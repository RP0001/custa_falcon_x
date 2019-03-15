from django.conf.urls import url
from custa import views

urlpatterns = [
    url(r'^$', views.about, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^custamise/$', views.custamise, name='custamise'),
    url(r'^order/$', views.order, name='order'),
    url(r'^checkout/$', views.checkout),
    url(r'^order-history/$', views.order_history, name='order-history'),
    url(r'^my-account/$', views.my_account, name='my-account'),
]
