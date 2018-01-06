from django.contrib import admin

from .models import (
    Channel,
    Payout,
    Promotion,
    Report,
    Sale,
    Share,
    Structure,
)


admin.site.register(Channel)
admin.site.register(Payout)
admin.site.register(Promotion)
admin.site.register(Report)
admin.site.register(Sale)
admin.site.register(Share)
admin.site.register(Structure)
