import MySQLdb, pprint, time, datetime
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("ggplot")

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="********",
                     db="taipower")

cursor = db.cursor()


sql_2a = "SELECT DATE(timestamp) AS sdate, MAX(northSupply), MAX(northUsage),                       \
            MAX(centerSupply), MAX(centerUsage),  MAX(southSupply), MAX(southUsage),                \
            MAX(eastSupply), MAX(eastUsage) FROM Power WHERE                                        \
            timestamp >= '2016-10-01 00:00:00' AND timestamp <= '2017-06-30 23:59:59' GROUP BY sdate "
cursor.execute(sql_2a)
datas = cursor.fetchall()


x = [data[0] for data in datas]
NS = [data[1] for data in datas]
NU = [data[2] for data in datas]
CS = [data[3] for data in datas]
CU = [data[4] for data in datas]
SS = [data[5] for data in datas]
SU = [data[6] for data in datas]
ES = [data[7] for data in datas]
EU = [data[8] for data in datas]


north_sql = "SELECT DATE(Time) AS sdate, Location, MAX(Temp) FROM Weather_hour WHERE    \
        Time >= '2016-10-01 00:00:00' AND Time <= '2017-06-30 23:59:59' AND             \
        Location = 'TAIPEI' GROUP BY sdate" 
center_sql = "SELECT DATE(Time) AS sdate, Location, MAX(Temp) FROM Weather_hour WHERE   \
        Time >= '2016-10-01 00:00:00' AND Time <= '2017-06-30 23:59:59' AND             \
        Location = 'SUN MOON LAKE' GROUP BY sdate" 
south_sql = "SELECT DATE(Time) AS sdate, Location, MAX(Temp) FROM Weather_hour WHERE    \
        Time >= '2016-10-01 00:00:00' AND Time <= '2017-06-30 23:59:59' AND             \
        Location = 'TAINAN' GROUP BY sdate" 
east_sql = "SELECT DATE(Time) AS sdate, Location, MAX(Temp) FROM Weather_hour WHERE     \
        Time >= '2016-10-01 00:00:00' AND Time <= '2017-06-30 23:59:59' AND             \
        Location = 'TAITUNG' GROUP BY sdate" 

cursor.execute(north_sql)
taipeis = cursor.fetchall()
cursor.execute(center_sql)
sun_moon_lakes = cursor.fetchall()
cursor.execute(south_sql)
tainans = cursor.fetchall()
cursor.execute(east_sql)
taitungs = cursor.fetchall()

x1 = [data[0] for data in taipeis]
TAIPEI = [data[2] for data in taipeis]
SUN_MOON_LAKE = [data[2] for data in sun_moon_lakes]
TAINAN = [data[2] for data in tainans]
TAITUNG = [data[2] for data in taitungs]

print len(x),len(x1)
#pprint.pprint(x)
#y1 = [data[2] for data in taipeis]
#y2 = [data[2] for data in sun_moon_lakes]
#y3 = [data[2] for data in tainans]
#y4 = [data[2] for data in taitungs]


#pprint.pprint(y1)
plt.figure()
plt.subplot(2,1,1)
plt.xticks(rotation=30)
plt.plot(x,NS, color = 'red', linewidth = 1.0, label='NS')
plt.plot(x,NU, color = 'blue', linewidth = 1.0, label='NU')
plt.xlabel('Date')
plt.ylabel('Power')
plt.legend()

plt.subplot(2,1,2)
plt.xticks(rotation=30)
plt.plot(x1,TAIPEI, color = 'green', linewidth = 1.0, label='TAIPEI')
plt.xlabel('Date')
plt.ylabel('MAX TEMP')
plt.legend()

plt.figure()
plt.subplot(2,1,1)
plt.xticks(rotation=30)
plt.plot(x,CS, color = 'red', linewidth = 1.0, label='CS')
plt.plot(x,CU, color = 'blue', linewidth = 1.0, label='CU')
plt.xlabel('Date')
plt.ylabel('Power')
plt.legend()

plt.subplot(2,1,2)
plt.xticks(rotation=30)
plt.plot(x1,SUN_MOON_LAKE, color = 'green', linewidth = 1.0, label='SUN_MOON_LAKE')
plt.xlabel('Date')
plt.ylabel('MAX TEMP')
plt.legend()

plt.figure()
plt.subplot(2,1,1)
plt.xticks(rotation=30)
plt.plot(x,SS, color = 'red', linewidth = 1.0, label='SS')
plt.plot(x,SU, color = 'blue', linewidth = 1.0, label='SU')
plt.xlabel('Date')
plt.ylabel('Power')
plt.legend()

plt.subplot(2,1,2)
plt.xticks(rotation=30)
plt.plot(x1,TAINAN, color = 'green', linewidth = 1.0, label='TAINAN')
plt.xlabel('Date')
plt.ylabel('MAX TEMP')
plt.legend()

plt.figure()
plt.subplot(2,1,1)
plt.xticks(rotation=30)
plt.plot(x,ES, color = 'red', linewidth = 1.0, label='ES')
plt.plot(x,EU, color = 'blue', linewidth = 1.0, label='EU')
plt.xlabel('Date')
plt.ylabel('Power')
plt.legend()

plt.subplot(2,1,2)
plt.xticks(rotation=30)
plt.plot(x1,TAITUNG, color = 'green', linewidth = 1.0, label='TAITUNG')
plt.xlabel('Date')
plt.ylabel('MAX TEMP')
plt.legend()

plt.show()