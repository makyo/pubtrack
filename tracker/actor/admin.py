from django.contrib import admin

from .models import (
    Actor,
    Group,
)


admin.site.register(Actor)
admin.site.register(Group)
