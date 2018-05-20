from django.contrib.auth.decorators import login_required

from .models import (
    Actor,
    Group,
)
from tracker.utils.json import (
    error,
    success,
)


@login_required
def list_groups(request):
    groups = []
    for group in Group.objects.all():
        groups.append({
            'id': group.id,
            'name': group.name,
            'type': group.type,
            'type_display': group.get_group_type_display(),
            'created': group.created.isoformat(' '),
            'updated': group.updated.isoformat(' '),
            'member_count': group.actor_set.count(),
        })
    return success(groups)


@login_required
def list_actors(request):
    actors = []
    for actor in Actor.objects.all():
        actors.append({
            'id': actor.slug,
            'name': actor.name,
            'type': actor.actor_type,
            'type_display': actor.get_actor_type_display(),
            'pseudonym': actor.pseudonym,
            'created': actor.created.isoformat(' '),
            'updated': actor.updated.isoformat(' '),
            'group_count': actor.groups.count(),
            'publication_count': actor.publication_set.count(),
        })
    return success(actors)


@login_required
def get_actor(request, slug):
    """Retrieve an actor and return a JSON blob of its info."""
    try:
        actor = Actor.objects.get(slug=slug)
    except Actor.DoesNotExist:
        return error(404, 'actor not found')
    return success(actor.json_repr())


@login_required
def get_group(request, group_id):
    """Retrieve an group and return a JSON blob of its info."""
    try:
        group = Group.objects.get(pk=group_id)
    except Group.DoesNotExist:
        return error(404, 'group not found')
    return success(group.json_repr())


@login_required
def create_actor(request):
    pass


@login_required
def create_group(request):
    pass


@login_required
def add_actor_to_group(request, group_id):
    """Add an actor to the specified group."""
    # actor = request.GET.get('actor')
    pass


@login_required
def remove_actor_from_group(request, group_id):
    """Remove an actor from the specified group."""
    # actor = request.GET.get('actor')
    pass
