from django.urls import path

from . import api


actor_api = [
    path('actors', api.list_actors, name='list_actors'),
    path('groups', api.list_groups, name='list_groups'),
    path('actor/<actor_id>', api.get_actor, name='get_actor'),
    path('group/<group_id>', api.get_group, name='get_group'),
]
