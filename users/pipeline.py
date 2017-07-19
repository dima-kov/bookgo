from django.core.files.base import ContentFile
from urllib.request import urlopen


def avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/{}/picture?type=large".format(
            response['id'])
        filename = 'fb_avatar_{}.jpg'.format(user.username)
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
        filename = url.split('/')[-1]
    if backend.name == 'google-oauth2':
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            filename = 'google_avatar_{}.jpg'.format(user.username)
    if url:
        user.avatar.save(
            filename,
            ContentFile(urlopen(url).read()),
            save=False,
        )
        user.save()
