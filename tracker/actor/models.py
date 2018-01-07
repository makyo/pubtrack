from django.db import models


class Group(models.Model):
    """Group represents a group of actors, such as a collection of authors."""

    GROUP_TYPES = (
        ('authors', 'Authors'),
        ('contributors', 'Contributors'),
        ('organization', 'Organization')
    )

    name = models.CharField(max_length=250)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(
            self.name,
            self.get_group_type_display())

    def json_repr(self):
        return {
            'name': self.name,
            'type': self.group_type,
            'type_display': self.get_group_type_display(),
            'created': self.created.isoformat(' '),
            'updated': self.updated.isoformat(' '),
            'notes': self.notes,
            'members': [
                actor.json_repr(
                    include_groups=False,
                    include_publications=False)
                for actor in self.actor_set.all()]
        }


class Actor(models.Model):
    """Actor represents an individual or entity such as an author, store or
    printer.
    """

    ACTOR_TYPES = (
        ('author', 'Author'),
        ('editor', 'Editor'),
        ('publisher', 'Publisher'),
        ('printer', 'Printer'),
        ('thirdparty', 'Third party')
    )

    name = models.CharField(max_length=250)
    actor_type = models.CharField(max_length=10, choices=ACTOR_TYPES)
    pseudonym = models.CharField(max_length=250, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{} ({})'.format(
            self.name,
            self.get_actor_type_display())

    def json_repr(self, include_groups=True, include_publications=True):
        actor_obj = {
            'id': self.id,
            'name': self.name,
            'type': self.actor_type,
            'type_display': self.get_actor_type_display(),
            'pseudonym': self.pseudonym,
            'created': self.created.isoformat(' '),
            'updated': self.updated.isoformat(' '),
            'notes': self.notes,
        }
        if include_groups:
            actor_obj['groups'] = [
                group.json_repr() for group in self.groups.all()]
        if include_publications:
            actor_obj['publications'] = [
                pub.json_repr() for pub in self.publication_set.all()]
        return actor_obj
