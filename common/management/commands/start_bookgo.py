from django.core.management.base import BaseCommand

from users.models import User
from common.email import EmailStartBookgo


class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            context = {
                'user': user,
            }
            email = EmailStartBookgo(context, [user.email])
            email.send()
        self.stdout.write("Message was sent")
