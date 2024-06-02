import pytz

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
STORE_STATUS_CHOICES = [("active","active"),("inactive","inactive")]
DAY_OF_WEEK_CHOICES = [(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday"),]
UPTIME_REPORT_STATUS_CHOICES = [(0, "Pending"), (1, "Processing"), (2, "Generated"), (3, "Failed"), (4, "Deleted")]