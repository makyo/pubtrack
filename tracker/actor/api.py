from .models import (
    Actor,
    Group,
)
from tracker.utils.json import (
    success,
    error,
)


def get_actor(request, actor_id):
    """Retrieve an actor and return a JSON blob of its info."""
    try:
        actor = Actor.objects.get(pk=actor_id)
    except Actor.DoesNotExist:
        return error(404, 'actor not found')
    return success(actor.json_repr())


def get_group(request, group_id):
    """Retrieve an group and return a JSON blob of its info."""
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return error(404, 'group not found')
    return success(group.json_repr())
