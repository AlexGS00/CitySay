from django.contrib import admin
from .models import User, Poll, Option, Sesization, Institution

# Register your models here.
admin.site.register(User)
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Sesization)
admin.site.register(Institution)