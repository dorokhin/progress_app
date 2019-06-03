from django.contrib import admin
from progress.models import PassEntry, EntryType


class EntryTypeAdmin(admin.ModelAdmin):
    pass


class PassEntryAdmin(admin.ModelAdmin):
    pass


admin.site.register(EntryType, EntryTypeAdmin)
admin.site.register(PassEntry, PassEntryAdmin)
