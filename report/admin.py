from django.contrib import admin

from report.models import MenuHours, Store, StoreStatus, UptimeReports

class StoreAdmin(admin.ModelAdmin):
    pass

class StoreStatusAdmin(admin.ModelAdmin):
    pass

class MenuHoursAdmin(admin.ModelAdmin):
    pass

class UptimeReportsAdmin(admin.ModelAdmin):
    pass



admin.site.register(Store, StoreAdmin)
admin.site.register(StoreStatus, StoreStatusAdmin)
admin.site.register(MenuHours, MenuHoursAdmin)
admin.site.register(UptimeReports, UptimeReportsAdmin)