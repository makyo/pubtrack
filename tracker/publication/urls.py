from django.urls import path

from . import api


publication_api = [
    path('publications', api.list_publications, name='list_publications'),
    path('publication/<slug>', api.get_publication, name='get_publication'),
    path('step/<step_id>', api.get_step, name='get_step'),
    path('attachment/<attachment_id>', api.get_attachment,
         name='get_attachment'),
]
