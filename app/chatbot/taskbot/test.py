import datetime

time_now = datetime.datetime.now()
unix_time = int(time_now.timestamp())

print(unix_time)