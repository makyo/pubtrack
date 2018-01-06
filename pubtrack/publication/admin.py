from django.contrib import admin

from .models import (
    Attachment,
    Publication,
    Step,
)


admin.site.register(Attachment)
admin.site.register(Publication)
admin.site.register(Step)
