from django.db import models

from actor.models import (
    Actor,
    Group,
)


class Publication(models.Model):
    """Publication represents a book, story, or other publication. It may have
    a parent, such as for an anthology, series, or collection."""

    PUBLICATION_TYPES = (
        ('collection', 'Anthology, collection, or magazine'),
        ('book', 'Book'),
        ('series', 'Series'),
        ('story', 'Short Story',)
    )

    title = models.CharField(max_length=1000)
    creator = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE)
    publication_type = models.CharField(
        max_length=30, choices=PUBLICATION_TYPES)
    parent = models.ForeignKey(
        'Publication',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Step(models.Model):
    """Step represents a step in the process of publication."""

    STEP_TYPES = (
        ('solicited', 'Solicited'),
        ('query_received', 'Query received'),
        ('query_approved', 'Query approved'),
        ('query_rejected', 'Query rejected'),
        ('manuscript_received', 'Manuscript recieved'),
        ('manuscript_approved', 'Manuscript approved'),
        ('manuscript_rejected', 'Manuscript rejected'),
        ('contracted_created', 'Contract created'),
        ('contract_sent', 'Contract sent'),
        ('contract_approved', 'Contract approved'),
        ('contract_rejected', 'Contract rejected'),
        ('contract_changes_requested', 'Contract changes requested'),
        ('contract_signed', 'Contract signed'),
        ('content_edits_pass', 'Content edits pass'),
        ('content_edits_approved', 'Content edits approved'),
        ('content_edits_changes_requested', 'Content edits changes requested'),
        ('copy_edits_pass', 'Copy edits pass'),
        ('copy_edits_approved', 'Copy edits approved'),
        ('copy_edits_changes_requested', 'Copy edits changes requested'),
        ('layout_pass', 'Layout pass'),
        ('layout_test_pass', 'Layout test sent'),
        ('layout_test_approved', 'Layout test approved'),
        ('layout_test_changes_requested', 'Layout test changes requested'),
        ('ebook_pass', 'Ebook pass'),
        ('ebook_test_pass', 'Ebook test sent'),
        ('ebook_test_approved', 'Ebook test approved'),
        ('ebook_test_changes_requested', 'Ebook test changes requested'),
        ('cover_art_solicted', 'Cover art solicited'),
        ('cover_art_received', 'Cover art received'),
        ('cover_art_approved', 'Cover art approved'),
        ('cover_art_changes_requested', 'Cover art changes requested'),
        ('blurb_created', 'Blurb created'),
        ('blurb_approved', 'Blurb approved'),
        ('blurb_changes_requested', 'Blurb changes requested'),
        ('arc_sent', 'ARC sent'),
        ('arc_quote_received', 'ARC quote received'),
        ('ISBN_print', 'ISBN created for print'),
        ('ISBN_ebook', 'ISBN created for ebook'),
        ('listed_amazon', 'Listed on Amazon'),
        ('listed_bn', 'Listed on B&N'),
        ('listed_goodreads', 'Listed on Good Reads'),
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE)
    step = models.CharField(max_length=50, choices=STEP_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)


class Attachment(models.Model):
    """Attachment represents a file attached to a publication."""

    ATTACHMENT_TYPES = (
        ('manuscript', 'Manuscript'),
        ('image', 'Image'),
        ('contract', 'Contract'),
        ('amendment', 'Contract amendment'),
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
