from django.contrib import admin

from currency.models import Opportunity


class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'value', )


admin.site.register(Opportunity, OpportunityAdmin)
