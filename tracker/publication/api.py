from django.contrib.auth.decorators import login_required

from .models import (
    Attachment,
    Publication,
    Step,
)
from tracker.utils.json import (
    error,
    success,
)


@login_required
def list_publications(request):
    publications = []
    for publication in Publication.objects.all():
        last_step = publication.step_set.order_by('-created')[0]
        to_add = {
            'id': publication.slug,
            'title': publication.title,
            'creator_id': publication.creator.slug,
            'creator_name': publication.creator.name,
            'type': publication.publication_type,
            'type_display': publication.get_publication_type_display(),
            'created': publication.created.isoformat(' '),
            'updated': publication.updated.isoformat(' '),
            'step_count': publication.step_set.count(),
            'last_step_type': last_step.step_type,
            'last_step_type_display': last_step.get_step_type_display(),
        }
        if publication.group:
            to_add['group_id'] = publication.group.id
            to_add['group_name'] = publication.group.name
        if publication.parent:
            to_add['parent_id'] = publication.parent.slug
            to_add['parent_title'] = publication.parent.title
        publications.append(to_add)
    return success(publications)


@login_required
def get_publication(request, slug):
    try:
        publication = Publication.objects.get(slug=slug)
    except Publication.DoesNotExist:
        return error(404, 'publication not found')
    return success(publication.json_repr())


@login_required
def get_step(request, step_id):
    try:
        step = Step.objects.get(pk=step_id)
    except Step.DoesNotExist:
        return error(404, 'step not found')
    return success(step.json_repr())


@login_required
def get_attachment(request, attachment_id):
    try:
        attachment = Attachment.objects.get(pk=attachment_id)
    except Step.DoesNotExist:
        return error(404, 'attachment not found')
    return success(attachment.json_repr())


@login_required
def create_publication(request):
    pass


@login_required
def create_step(request, publication_slug):
    pass


@login_required
def create_attachment(request, step_id):
    pass


@login_required
def delete_publication(request, publication_slug):
    pass


@login_required
def delete_step(request, step_id):
    pass


@login_required
def delete_attachment(attachment_id):
    pass
