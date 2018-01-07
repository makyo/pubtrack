from .models import (
    Actor,
    Group,
)
from tracker.utils.json import (
    success,
    error,
)


def get_actor(request, actor_id):
    # depth = request.GET.get('depth', 0)
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return error(404, 'actor not found')
    response = {
        'id': actor.id,
        'name': actor.name,
        'type': actor.actor_type,
        'pseudonym': actor.pseudonym,
        'created': actor.created.isoformat(' '),
        'updated': actor.updated.isoformat(' '),
        'notes': actor.notes,
        'publications': [],
    }
    for publication in actor.publication_set.order_by('updated'):
        publication_obj = {
            'id': publication.id,
            'title': publication.title,
            'type': publication.publication_type,
            'notes': publication.notes,
            'creator_id': publication.creator.id,
            'group_id': publication.group.id if publication.group else '',
            'parent_id': publication.parent.id if publication.parent else '',
            'created': publication.created.isoformat(' '),
            'updated': publication.updated.isoformat(' '),
            'steps': [],
        }
        for step in publication.step_set.order_by('created'):
            step_obj = {
                'type': step.step_type,
                'created': step.created.isoformat(' '),
                'notes': step.notes,
                'attachments': [],
            }
            for attachment in step.attachment_set.order_by('created'):
                attachment_obj = {
                    'type': attachment.attachment_type,
                    'created': attachment.created.isoformat(' '),
                    'name': attachment.attachment.name,
                    'size': attachment.attachment.size,
                    'url': attachment.attachment.url,
                    'notes': attachment.notes,
                }
                step['attachments'].append(attachment)
            publication_obj['steps'].append(step_obj)
        response['publications'].append(publication_obj)
    return success(response)


def get_group(request, group_id):
    # depth = request.GET.get('depth', 0)
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return error(404, 'group not found')
    response = {
        'name': group.name,
        'type': group.group_type,
        'created': group.created.isoformat(' '),
        'updated': group.updated.isoformat(' '),
        'notes': group.notes,
    }
    return success(response)
