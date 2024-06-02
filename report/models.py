import datetime
from django.db import models

from report.constants import DAY_OF_WEEK_CHOICES, STORE_STATUS_CHOICES, TIMEZONES, UPTIME_REPORT_STATUS_CHOICES


class Store(models.Model):
    store_id = models.CharField(max_length=30, blank=False, null=False)
    localTimezone= models.CharField(max_length=32, choices=TIMEZONES, default='UTC', blank=False, null=False)

class StoreStatus(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=16, choices=STORE_STATUS_CHOICES, blank=False, null=False,  help_text="Please use this field to mark wheter or not the store is active")
    timestamp_utc = models.DateTimeField(blank=False, null=False, help_text="Please enter the UTC timestamp")
    
class MenuHours(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    day = models.PositiveSmallIntegerField(choices=DAY_OF_WEEK_CHOICES, blank=False, null=False,  help_text="Please enter the day of the week b/w 0 and 6 (0=Monday & 6=Sunday)")
    start_time_local = models.TimeField(default=datetime.time(), blank=False, null=False, help_text="Please enter the local opening time for the store")
    end_time_local = models.TimeField(default=datetime.time(hour=23, minute=59, second=59, microsecond=999999), blank=False, null=False, help_text="Please enter the local closing time for the store")

class UptimeReports(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False, help_text="Please enter the local opening time for the store")
    status = models.PositiveBigIntegerField(default=0, blank=False, null=False, choices=UPTIME_REPORT_STATUS_CHOICES, help_text="The status of uptime report (0=Pending, 1=Processing, 2=Generated, 3=Failed, 4=Deleted)")


