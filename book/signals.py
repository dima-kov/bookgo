from django.db.models.signals import post_save
from django.dispatch import receiver

from book.models import Book
from book.models import BookReading
from currency.models import Opportunity


@receiver(post_save, sender=Book)
def opportunities_on_book_creating(sender, instance, created, **kwargs):
    if created:
        Opportunity.objects.create(
            user=instance.owner,
            type=Opportunity.ADD_BOOK,
            book=instance,
        )


@receiver(post_save, sender=BookReading)
def opportunities_on_book_reading(sender, instance, created, **kwargs):
    if created:
        Opportunity.objects.create(
            user=instance.user,
            type=Opportunity.READ_BOOK,
            reading=instance,
        )
