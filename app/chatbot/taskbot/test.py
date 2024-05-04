from datetime import datetime, timedelta

time_now = datetime.now()

unix_time = int(time_now.timestamp())

print(unix_time)

# Convert Unix timestamp to datetime object
datetime_obj = datetime.fromtimestamp(unix_time)

print(datetime_obj)

i = 1714642223

datetime_obj = datetime.fromtimestamp(i)
print(datetime_obj)