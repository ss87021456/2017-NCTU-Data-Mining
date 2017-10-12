import MySQLdb, pprint, time, datetime
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("ggplot")

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="********",
                     db="taipower")

cursor = db.cursor()


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

x = [data[0] for data in taipeis]
y1 = [data[2] for data in taipeis]
y2 = [data[2] for data in sun_moon_lakes]
y3 = [data[2] for data in tainans]
y4 = [data[2] for data in taitungs]

#pprint.pprint(y1)
plt.figure()

plt.xticks(rotation=30)
plt.xlabel('Date')
plt.ylabel('MAX Temp')
#plt.xticks(new_ticks)
#plt.yticks([-2,-1,0,1,2],['really bad','bad','normal','good','really good'])
#plt.yticks([-2,-1,0,1,2],[r'$really\ bad$',r'$bad$',r'$normal$',r'$good$',r'$really\ good$'])

plt.plot(x,y1, color = 'red', linewidth = 1.0, label='NORTH')
plt.plot(x,y2, color = 'blue', linewidth = 1.0, label='CENTRAL')
plt.plot(x,y3, color = 'green', linewidth = 1.0, label='SOUTH')
plt.plot(x,y4, color = 'black', linewidth = 1.0, label='EAST')
#plt.plot(x,y2,label='down')
plt.legend()

plt.show()