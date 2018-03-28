# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from users.models import User
# from currency.models import Opportunity


# @receiver(post_save, sender=User)
# def opportunities_on_register(sender, instance, created, **kwargs):
#     if created:
#         Opportunity.objects.create(user=instance, type=Opportunity.REGISTER)
