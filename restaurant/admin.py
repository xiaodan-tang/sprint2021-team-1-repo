from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    InspectionRecords,
    Restaurant,
    UserQuestionnaire,
    YelpRestaurantDetails,
    Zipcodes,
    AccessibilityRecord,
)


admin.site.register(Restaurant)
admin.site.register(InspectionRecords)
admin.site.register(UserQuestionnaire)
admin.site.register(YelpRestaurantDetails)
admin.site.register(Zipcodes)



admin.site.register(AccessibilityRecord, FAQ)
@admin.register(AccessibilityRecord)
class ViewAdmin(ImportExportModelAdmin):
    pass
