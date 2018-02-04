from django.contrib import admin
from django.urls import (
    include,
    path,
)

from actor.urls import actor_api
from publication.urls import publication_api


api = [
    path('actors/', include(actor_api)),
    # path('payments/', include(payment_api)),
    path('publications/', include(publication_api)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api)),
]
