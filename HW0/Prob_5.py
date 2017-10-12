import MySQLdb, pprint, time, datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

plt.style.use("ggplot")
# Connect
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="********",
                     db="taipower")

cursor = db.cursor()

date_sql = "SELECT timestamp FROM Power WHERE timestamp >= '2016-10-01 00:00:00' AND timestamp <= '2017-06-30 23:59:59'"
Q_sql = "SELECT northSupply FROM Power WHERE timestamp >= '2016-10-01 00:00:00' AND timestamp <= '2017-06-30 23:59:59'"
C_sql = "SELECT northUsage FROM Power WHERE timestamp >= '2016-10-01 00:00:00' AND timestamp <= '2017-06-30 23:59:59'"

cursor.execute(date_sql)
date = [element[0] for element in cursor.fetchall()]
cursor.execute(Q_sql)
Q_data = [element[0] for element in cursor.fetchall()]
cursor.execute(C_sql)
C_data = [element[0] for element in cursor.fetchall()]

day_count = 2033 # missing data from 2017-01-25 02:10:00 to 2017-04-19 18:10:00
start = (2017,1,25,1,10,0,0,1,-1)
start_timestamp = time.mktime(start)

#date = np.asarray(date)
Q_std = np.std(np.asarray(Q_data))
C_std = np.std(np.asarray(C_data))
# y = ax + b
print date[2753:2755]
Q_a = (Q_data[2754] - Q_data[2753])/day_count
Q_b = Q_data[2753]
C_a = (C_data[2754] - C_data[2753])/day_count
C_b = C_data[2753]
print "y = ",Q_a,"x + ",Q_b
print "y = ",C_a,"x + ",C_b


for num in range(1,day_count+1,1):
	index = 2753 + num
	add_timestamp = datetime.datetime.fromtimestamp(start_timestamp + num*3600)
	date.insert(index,add_timestamp)
	Q_data.insert(index,Q_a*num+Q_b+Q_std*np.random.randn()*0.5)
	C_data.insert(index,C_a*num+C_b+C_std*np.random.randn()*0.5)

Q_data = np.asarray(Q_data)
C_data = np.asarray(C_data)

print Q_data.shape,C_data.shape,len(date)

plt.figure("Original")
plt.xticks(rotation=30)
plt.xlabel('Date')
plt.ylabel('Power')
plt.plot(date,Q_data, color = 'red', linewidth = 1.0, label='northSupply_ori')
plt.plot(date,C_data, color = 'blue', linewidth = 1.0, label='northUsage_ori')
plt.legend()


plt.show()