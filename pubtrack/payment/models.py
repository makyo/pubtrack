from django.db import models

from actor.models import Actor
from publication.models import Publication


class Channel(models.Model):
    """Channel represents a sales channel such as a store, convention, etc."""

    CHANNEL_TYPES = (
        ('online_print', 'Online: Print'),
        ('online_ebook', 'Online: Ebook'),
        ('publisher', 'Publisher Direct'),
        ('author', 'Author Direct'),
    )

    name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    notes = models.TextField(blank=True)


class Structure(models.Model):
    """Structure represents a payment structure for an actor."""

    STRUCTURE_TYPES = (
        ('royalties', 'Royalties'),
        ('advance', 'Advance'),
        ('flat_fee', 'Flat fee'),
    )

    publication = models.ForeignKey(
        Publication,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    structure_type = models.CharField(max_length=10, choices=STRUCTURE_TYPES)
    channel = models.ForeignKey(
        Channel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    fee = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                              blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                     blank=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Sale(models.Model):
    """Sale represents a single or multiple sales of a publication."""

    publication = models.ForeignKey(
        Publication,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    amount = models.IntegerField(default=1)
    net = models.DecimalField(max_digits=6, decimal_places=2)
    gross = models.DecimalField(max_digits=6, decimal_places=2)
    channel = models.ForeignKey(
        Channel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    date_time = models.DateTimeField(auto_now_add=True)


class Share(models.Model):
    """Share represents the amount an actor gets from a sale"""

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE)
    actor = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=6, decimal_places=2)


class Payout(models.Model):
    """Payout represents a payment to an actor."""

    PAYMENT_TYPES = (
        ('royalties', 'Royalties'),
        ('overhead', 'Overhead'),
        ('flat_fee', 'Flat fee'),
    )

    pay_to = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        related_name="payments_to",
        on_delete=models.SET_NULL)
    pay_from = models.ForeignKey(
        Actor,
        blank=True,
        null=True,
        related_name="payments_from",
        on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)


class Report(models.Model):
    """Report represents a report of payment activity for a variety of types."""

    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    publications = models.ManyToManyField(Publication)
    actors = models.ManyToManyField(Actor)
    sales = models.ManyToManyField(Sale)
    payouts = models.ManyToManyField(Payout)
    notes = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Promotion(models.Model):
    """Promotion represents a sale, giveaway, etc."""

    PROMOTION_TYPES = (
        ('discount', 'Discount (percentage)'),
        ('amount', 'Amount (dollars off)'),
    )

    name = models.CharField(max_length=500)
    description = models.TextField()
    promotion_type = models.CharField(max_length=10, choices=PROMOTION_TYPES)
    date_start = models.DateField()
    date_end = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publications = models.ManyToManyField(Publication)
    actors = models.ManyToManyField(Actor)
    limit = models.IntegerField()
