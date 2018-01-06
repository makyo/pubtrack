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
    pseudonym = models.CharField(max_length=250)
    groups = models.ManyToManyField(Group)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
