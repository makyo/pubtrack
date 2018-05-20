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
        blank=True,
        null=True,
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
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Publication: {} ({}) by {}'.format(
            self.title,
            self.get_publication_type_display(),
            self.creator)

    def json_repr(self):
        publication_obj = {
            'id': self.id,
            'title': self.title,
            'type': self.publication_type,
            'type_display': self.get_publication_type_display(),
            'notes': self.notes,
            'creator': {
                'name': self.creator.name,
                'type': self.creator.actor_type,
                'type_display': self.creator.get_actor_type_display(),
                'id': self.creator.id,
            },
            'created': self.created.isoformat(' '),
            'updated': self.updated.isoformat(' '),
            'steps': [step.json_repr() for step in self.step_set.all()],
        }
        if self.group:
            publication_obj['group'] = {
                'id': self.group.id,
                'type': self.group.group_type,
                'type_display': self.group.get_group_type_display(),
                'name': self.group.name,
            }
        if self.parent:
            def build_parent(obj, parent):
                obj['parent'] = {
                    'id': parent.id,
                    'title': parent.title,
                }
                if parent.parent:
                    build_parent(obj['parent'], parent.parent)
            build_parent(publication_obj, self.parent)
        return publication_obj


class Step(models.Model):
    """Step represents a step in the process of publication."""

    # The type of step that is currently being taken.
    STEP_TYPES = (
        ('query_received', 'Query received'),
        ('query_approved', 'Query approved'),
        ('query_rejected', 'Query rejected'),
        ('solicited', 'Solicited'),
        ('manuscript_received', 'Manuscript recieved'),
        ('manuscript_approved', 'Manuscript approved'),
        ('manuscript_rejected', 'Manuscript rejected'),
        ('contract_pass', 'Contract pass'),
        ('contract_sent', 'Contract sent'),
        ('contract_changes_requested', 'Contract changes requested'),
        ('contract_approved', 'Contract approved'),
        ('contract_rejected', 'Contract rejected'),
        ('contract_signed', 'Contract signed'),
        ('content_edits_pass', 'Content edits pass'),
        ('content_edits_sent', 'Content edits sent'),
        ('content_edits_changes_requested', 'Content edits changes requested'),
        ('content_edits_approved', 'Content edits approved'),
        ('copy_edits_pass', 'Copy edits pass'),
        ('copy_edits_sent', 'Copy edits sent'),
        ('copy_edits_changes_requested', 'Copy edits changes requested'),
        ('copy_edits_approved', 'Copy edits approved'),
        ('layout_pass', 'Layout pass'),
        ('layout_sent', 'Layout sent'),
        ('layout_changes_requested', 'Layout changes requested'),
        ('layout_approved', 'Layout approved'),
        ('layout_skipped', 'Layout skipped'),
        ('ebook_pass', 'Ebook pass'),
        ('ebook_sent', 'Ebook sent'),
        ('ebook_changes_requested', 'Ebook changes requested'),
        ('ebook_approved', 'Ebook approved'),
        ('ebook_skipped', 'Ebook skipped'),
        ('cover_art_provided', 'Cover art provided'),
        ('cover_art_solicted', 'Cover art solicited'),
        ('cover_art_received', 'Cover art received'),
        ('cover_art_pass', 'Cover art pass'),
        ('cover_art_sent', 'Cover art sent'),
        ('cover_art_changes_requested', 'Cover art changes requested'),
        ('cover_art_approved', 'Cover art approved'),
        ('cover_art_skipped', 'Cover art skipped'),
        ('interior_art_provided', 'Interior art provided'),
        ('interior_art_solicted', 'Interior art solicited'),
        ('interior_art_received', 'Interior art received'),
        ('interior_art_pass', 'Interior art pass'),
        ('interior_art_sent', 'Interior art sent'),
        ('interior_art_changes_requested', 'Interior art changes requested'),
        ('interior_art_approved', 'Interior art approved'),
        ('blurb_pass', 'Blurb pass'),
        ('blurb_sent', 'Blurb sent'),
        ('blurb_changes_requested', 'Blurb changes requested'),
        ('blurb_approved', 'Blurb approved'),
        ('arc_sent', 'ARC sent'),
        ('arc_quote_received', 'ARC quote received'),
        ('ISBN_print', 'ISBN created for print'),
        ('ISBN_ebook', 'ISBN created for ebook'),
        ('print_service_pass', 'Print service file pass'),
        ('print_service_sent', 'Print service file sent'),
        ('print_service_changes_requested', 'Print service changes requested'),
        ('print_service_approved', 'Print service file approved'),
        ('listed_channel', 'Listed on sales channel'),
        ('listed_goodreads', 'Listed on Good Reads'),
        ('review_solicted', 'Review solicited'),
        ('review_received', 'Review received'),
        ('review_posted', 'Review posted'),
        ('sale_discount_created', 'Sale or discount created'),
        ('sale_discount_ended', 'Sale or discount ended'),
    )

    # The steps in proper order as a list for indexing.
    ORDERED_STEPS = [step[0] for step in STEP_TYPES]

    # The general flow that steps take. To not follow the flow requires a force
    # flag to be passed to save.
    STEP_FLOW = {
        'query_received': ['query_approved', 'query_rejected'],
        'query_approved': ['solicited'],
        'solicited': ['manuscript_received'],
        'manuscript_received': ['manuscript_approved', 'manuscript_rejected'],
        'manuscript_approved': ['contract_pass'],
        'contract_pass': ['contract_sent'],
        'contract_sent': [
            'contract_approved',
            'contract_changes_requested',
            'contract_rejected',
        ],
        'contract_changes_requested': ['contract_pass'],
        'contract_approved': ['contract_signed'],
        'contract_signed': ['content_edits_pass'],
        'content_edits_pass': ['content_edits_sent'],
        'content_edits_sent': [
            'content_edits_approved',
            'content_edits_changes_requested',
        ],
        'content_edits_changes_requested': ['content_edits_pass'],
        'content_edits_approved': ['copy_edits_pass'],
        'copy_edits_pass': ['copy_edits_sent'],
        'copy_edits_sent': [
            'copy_edits_approved',
            'copy_edits_changes_requested',
        ],
        'copy_edits_changes_requested': ['copy_edits_pass'],
        'copy_edits_approved': ['layout_pass', 'layout_skipped',],
        'layout_pass': ['layout_sent'],
        'layout_sent': [
            'layout_approved'
            'layout_changes_requested',
        ],
        'layout_changes_requested': ['layout_pass'],
        'layout_approved': ['ebook_pass', 'ebook_skipped'],
        'layout_skipped': ['ebook_pass'],
        'ebook_pass': ['ebook_sent'],
        'ebook_sent': [
            'ebook_approved',
            'ebook_changes_requested',
        ],
        'ebook_changes_requested': ['ebook_pass'],
        'ebook_approved': [
            'cover_art_provided',
            'cover_art_solicted',
            'cover_art_skipped',
        ],
        'ebook_skipped': [
            'cover_art_provided',
            'cover_art_solicted',
            'cover_art_skipped',
        ],
        'cover_art_provided': ['cover_art_received'],
        'cover_art_solicted': ['cover_art_received'],
        'cover_art_received': ['cover_art_pass'],
        'cover_art_pass': [
            'cover_art_approved',
            'cover_art_changes_requested',
        ],
        'cover_art_changes_requested': ['cover_art_pass'],
        'cover_art_approved': [
            'interior_art_provided',
            'interior_art_solicted',
            'interior_art_skipped',
        ],
        'cover_art_skipped': [
            'interior_art_provided',
            'interior_art_solicted',
            'interior_art_skipped',
        ],
        'interior_art_provided': ['interior_art_received'],
        'interior_art_solicted': ['interior_art_received'],
        'interior_art_received': ['interior_art_pass'],
        'interior_art_pass': [
            'interior_art_approved',
            'interior_art_changes_requested',
        ],
        'interior_art_changes_requested': ['interior_art_pass'],
        'interior_art_approved': [
            'blurb_pass',
            'arc_sent',
        ],
        'interior_art_skipped': [
            'blurb_pass',
            'arc_sent',
        ],
        'blurb_pass': ['blurb_sent'],
        'blurb_sent': ['blurb_approved', 'blurb_changes_requested'],
        'blurb_changes_requested': ['blurb_pass'],
        'blurb_approved': ['arc_sent', 'ISBN_print', 'ISBN_ebook'],
        'arc_sent': [
            'arc_quote_received',
            'blurb_pass',
            'ISBN_print',
            'ISBN_ebook',
        ],
        'ISBN_print': ['ISBN_ebook', 'print_service_pass'],
        'ISBN_ebook': ['ISBN_print', 'print_service_pass', 'listed_channel'],
        'print_service_pass': ['print_service_sent'],
        'print_service_sent': [
            'print_service_approved',
            'print_service_changes_requested',
        ],
        'print_service_changes_requested': ['print_service_pass'],
        'print_service_approved': ['listed_channel'],
        'listed_channel': [
            'listed_goodreads',
            'review_solicted',
            'review_received',
            'sale_discount_created',
        ],
        'review_solicted': [
            'review_solicted',
            'review_received',
            'sale_discount_created',
            'sale_discount_ended',
        ],
        'review_received': ['review_posted'],
        'review_posted': [
            'review_solicted',
            'review_received',
            'sale_discount_created',
            'sale_discount_ended',
        ],
        'sale_discount_created': [
            'review_solicted',
            'review_received',
            'sale_discount_created',
            'sale_discount_ended',
        ],
        'sale_discount_ended': [
            'review_solicted',
            'review_received',
            'sale_discount_created',
            'sale_discount_ended',
        ],
    }

    # Steps which have no following step. To follow these steps requires a force
    # flag to be passed to save.
    FINAL_STEPS = (
        'query_rejected',
        'manuscript_rejected',
        'contract_rejected',
    )

    # Steps from which you cannot go backward in the order. To get around this
    # requires a force flag to be passed to save.
    IRREVERSABLE_STEPS = (
        'query_approved',
        'manuscript_approved',
        'contract_approved',
        'content_edits_approved'
        'copy_edits_approved',
        'layout_test_approved',
        'ebook_test_approved',
        'cover_art_approved',
        'interior_art_approved',
        'blurb_approved',
        'print_service_approved',
    )

    class StepOrderViolation(Exception):
        pass

    class StepFinalViolation(Exception):
        pass

    class StepReverseViolation(Exception):
        pass

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE)
    step_type = models.CharField(max_length=50, choices=STEP_TYPES)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def save(self, force=False, *args, **kwargs):
        if not force:
            try:
                prev_step = self.publication.step_set.order_by('-created')[0]
                prev = prev_step.step_type
            except (Publication.DoesNotExist, IndexError):
                super(Step, self).save()
                return
            if prev in FINAL_STEPS:
                raise Step.StepFinalViolation(prev)
            if (prev in IRREVERSABLE_STEPS and
                    ORDERED_STEPS.index(self.step_type) <
                    ORDERED_STEPS.index(prev)):
                raise Step.StepReverseViolation(prev)
            if self.step_type not in STEP_FLOW[prev]:
                raise Step.StepOrderViolation(prev)
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Step: {} for {}'.format(
            self.get_step_type_display(),
            self.publication.title)

    def json_repr(self):
        return {
            'type': self.step_type,
            'type_display': self.get_step_type_display(),
            'created': self.created.isoformat(' '),
            'notes': self.notes,
            'attachments': [
                attachment.json_repr() for attachment in
                self.attachment_set.all()],
        }


class Attachment(models.Model):
    """Attachment represents a file attached to a publication."""

    ATTACHMENT_TYPES = (
        ('manuscript', 'Manuscript'),
        ('image', 'Image'),
        ('contract', 'Contract'),
        ('amendment', 'Contract amendment'),
    )

    step = models.ForeignKey(
        Step,
        on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPES)
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return 'Attachment: {} attached to {}'.format(
            self.get_attachment_type_display(),
            self.step)

    def json_repr(self):
        return {
            'type': self.attachment_type,
            'type_display': self.get_attachment_type_display(),
            'created': self.created.isoformat(' '),
            'name': self.attachment.name,
            'size': self.attachment.size,
            'url': self.attachment.url,
            'notes': self.notes,
        }
