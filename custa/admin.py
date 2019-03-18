from django.contrib import admin
from custa.models import Base, Sauce, Top, Custa, UserProfile, Order

# register all models for use in the web application
admin.site.register(Base)
admin.site.register(Sauce)
admin.site.register(Top)
admin.site.register(Custa)
admin.site.register(UserProfile)
admin.site.register(Order)
