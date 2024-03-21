present = datetime.now()

c_timestamp = os.path.getctime(local_path)
 
# convert creation timestamp into DateTime object
c_datestamp = datetime.fromtimestamp(c_timestamp)
duration = c_datestamp - present 
print(duration < timedelta(minutes=30))