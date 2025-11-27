from django.contrib import admin
from .models import (
    Staffs,
    Works,
    PlatForms,
    PlatformInfo,
    WorkSeason
)
# Register your models here.
admin.site.register(Staffs)
admin.site.register(Works)
admin.site.register(PlatForms)
admin.site.register(PlatformInfo)
admin.site.register(WorkSeason)
