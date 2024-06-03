import datetime
import math
from django.db import models
from django.db.models import Q
from pytz import timezone

from report.constants import CURRENT_DATETIME, DAY_OF_WEEK_CHOICES, STORE_STATUS_CHOICES, TIMEZONES, UPTIME_REPORT_STATUS_CHOICES


class Store(models.Model):
    store_id = models.CharField(max_length=30, blank=False, null=False)
    localTimezone= models.CharField(max_length=32, choices=TIMEZONES, default='UTC', blank=False, null=False)

class StoreStatus(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    status = models.CharField(max_length=16, choices=STORE_STATUS_CHOICES, blank=False, null=False,  help_text="Please use this field to mark wheter or not the store is active")
    timestamp_utc = models.DateTimeField(blank=False, null=False, help_text="Please enter the UTC timestamp")
#{'store_id': 1481966498820158979, 'day': 4, 'start_time_local': '00:00:00', 'end_time_local': '00:10:00'}    
class MenuHours(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    day = models.PositiveSmallIntegerField(choices=DAY_OF_WEEK_CHOICES, blank=False, null=False,  help_text="Please enter the day of the week b/w 0 and 6 (0=Monday & 6=Sunday)")
    start_time_local = models.TimeField(default=datetime.time(), blank=False, null=False, help_text="Please enter the local opening time for the store")
    end_time_local = models.TimeField(default=datetime.time(hour=23, minute=59, second=59, microsecond=999999), blank=False, null=False, help_text="Please enter the local closing time for the store")

class UptimeReports(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.PositiveBigIntegerField(default=0, blank=False, null=False, choices=UPTIME_REPORT_STATUS_CHOICES, help_text="The status of uptime report (0=Pending, 1=Processing, 2=Generated, 3=Failed, 4=Deleted)")


    @classmethod
    def generate_report_for_store_id(cls):
        uptime_report = UptimeReports.objects.create()
        
        #create a record in UptimeReports with stauts pending
        #change status to processing
        #start processing, for each store_id in Store table:
        #   Get the localTimezone for the store from store_id
        #   Get the Menu hours for the store from store_id
        #   Get StoreStatus for the last 7 days -> 7_day_data
        #   Fill in missing data:
        #       For each of the 7 days:
        #           Get records for observations b/w the business hours
        #           If data is missing for any of the observations then:
        #               use average of rest of the data to decide what to fill in the times
        #   update uptime_last_week using current data (hours active)
        #   update downtime_last_week using current data (hours active)
        #   update uptime_last_day using last days data 
        #   update downtime_last_day using last days data 
        #   update uptime_last_hour using data from last hour
        #   update downtime_last_hour using data from last hour

        try:
            uptime_report.status = 1
            uptime_report.save()
            stores = Store.objects.all()
            store_statuses = StoreStatus.objects.filter(Q(timestamp_utc__lte=CURRENT_DATETIME) & Q(timestamp_utc__gte=(CURRENT_DATETIME - datetime.timedelta(days=7)))).select_related('store_id').order_by('timestamp_utc')
            print("Store statuses: ", len(store_statuses))
            report = []
            for store in stores:
                store_report = [{"store_id": store.store_id}]
                local_timezone = store.localTimezone
                store_status_seven_days = store_statuses.filter(store_id__store_id=store.store_id).values()
                menu_hours = MenuHours.objects.filter(store_id__store_id=store.store_id).values()
                utc = timezone('UTC')
                #filling of data
                for i in range(0, 6):
                    curr_date = CURRENT_DATETIME.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=i)
                    day = curr_date.weekday()
                    start_datetime_utc = curr_date
                    end_datetime_utc = curr_date + datetime.timedelta(days=1)
                    menu_hour = list(filter(lambda x: (x['day'] == day), menu_hours))
                    
                    if(menu_hour):
                        menu_hour = menu_hour[0]
                        start_time_local = menu_hour['start_time_local']
                        end_time_local = menu_hour['end_time_local']
                        
                        start_datetime_utc = curr_date.replace(hour=start_time_local.hour, minute=start_time_local.minute, tzinfo=timezone(local_timezone)).astimezone(utc)
                        end_datetime_utc = curr_date.replace(hour=end_time_local.hour, minute=end_time_local.minute, tzinfo=timezone(local_timezone)).astimezone(utc)
                    
                    difference = end_datetime_utc - start_datetime_utc
                    difference_hours = math.floor(difference.total_seconds()/(60*60))
                    todays_status = list(filter(lambda x: ((x['timestamp_utc'] > start_datetime_utc )and x['timestamp_utc'] < end_datetime_utc ), store_status_seven_days))
                    if(len(todays_status)):
                        active_hours = len(list(filter(lambda x:(x['status'] == 'active'), todays_status)))
                    #fill missing data
                
                active_hours = len(list(filter(lambda x:(x['status'] == 'active'), store_status_seven_days)))
                inactive_hours = len(store_status_seven_days)
                store_report.append({'uptime_last_week': active_hours})
                store_report.append({'downtime_last_week': inactive_hours})

                active_hours = len(list(filter(lambda x:((x['status'] == 'active') and (x['timestamp_utc'] > CURRENT_DATETIME - datetime.timedelta(days=1))), store_status_seven_days)))
                inactive_hours = len(list(filter(lambda x:((x['status'] == 'inactive') and (x['timestamp_utc'] > CURRENT_DATETIME - datetime.timedelta(days=1))), store_status_seven_days)))
                store_report.append({'uptime_last_day': active_hours})
                store_report.append({'downtime_last_day': inactive_hours})

                active_entries_past_hour = list(filter(lambda x:((x['status'] == 'active') and (x['timestamp_utc'] > CURRENT_DATETIME - datetime.timedelta(hours=2))), store_status_seven_days))
                for data in active_entries_past_hour:
                    #check data for before and after the last 1 hour point
                    pass
                



                        
                    


                    

                    
                    
                        

                        
                    

                
                    
                    

            
        except Exception as e:
            print(e)
        else:
            uptime_report.status = 2
            uptime_report.save()
        
        pass