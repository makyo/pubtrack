from django.urls import path

from . import api


actor_api = [
    path('actor/<actor_id>', api.get_actor, name='get_actor'),
    path('group/<group_id>', api.get_group, name='get_group'),
]
