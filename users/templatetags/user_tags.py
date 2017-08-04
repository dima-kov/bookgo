from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.simple_tag
def user_social_link(user):
    socialauth = user.social_auth.all().first()
    provider = socialauth.provider
    if provider == 'facebook':
        url = 'https://www.facebook.com/{}'
    elif provider == 'twitter':
        url = 'https://www.twitter.com/intent/user?user_id={}'
    else:
        return ''

    url = url.format(socialauth.uid)
    return mark_safe(
        '<a href="{}" target="_blank" class="social">{}</a>'.format(
            url, provider
        ))
