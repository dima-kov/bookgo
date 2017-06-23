from django.contrib.auth.models import AbstractUser

from currency.models import Opportunity


class User(AbstractUser):

    @property
    def opportunities(self):
        return Opportunity.objects.filter(user=self).count_values()
