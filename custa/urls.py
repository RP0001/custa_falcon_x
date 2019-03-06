from django.conf.urls import url
from custa import views

urlpatterns = [
url(r'^$', views.about, name='about'),
]

