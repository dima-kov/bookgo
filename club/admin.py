from django.contrib import admin

from club.models import Club, ClubInvite, ClubMember

admin.site.register(Club)
admin.site.register(ClubInvite)
admin.site.register(ClubMember)
