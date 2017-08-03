from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def get_book_card_size():
    return '{}x{}'.format(
        settings.BOOK_CARD_IMAGE_WIDTH,
        settings.BOOK_CARD_IMAGE_HEIGHT,
    )


@register.assignment_tag
def get_book_full_size():
    return '{}x{}'.format(
        settings.BOOK_FULL_IMAGE_WIDTH,
        settings.BOOK_FULL_IMAGE_HEIGHT,
    )
