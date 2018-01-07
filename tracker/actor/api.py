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
        'name': actor.name,
        'type': actor.actor_type,
        'pseudonym': actor.pseudonym,
        'created': actor.created.isoformat(' '),
        'updated': actor.updated.isoformat(' '),
        'notes': actor.notes,
    }
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
