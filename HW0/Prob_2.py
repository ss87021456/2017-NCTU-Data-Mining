#!/usr/bin/python
import MySQLdb, pprint, time


# Connect
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="********",
                     db="taipower")

cursor = db.cursor()

# Execute SQL select statement
print "----------- start 2a-1 problem -----------"

time.sleep(1)

print "\nFind the maximum power supply value and power usage value"
print "for each day and each area(North , Center , South , East)\n"
print "  Date\t\tNS\tNU\tCS\tCU\tSS\tSU\tES\tEU"

sql_2a = "SELECT DATE(timestamp) AS sdate, MAX(northSupply), MAX(northUsage),                       \
            MAX(centerSupply), MAX(centerUsage),  MAX(southSupply), MAX(southUsage),                \
            MAX(eastSupply), MAX(eastUsage) FROM Power WHERE                                        \
            timestamp >= '2016-10-01 00:00:00' AND timestamp <= '2017-06-30 23:59:59' GROUP BY sdate "
cursor.execute(sql_2a)

for row in cursor.fetchall():
    for element in row:
        print element,"\t",
    print ""


time.sleep(1)
print "----------- start 2b problem -----------"
time.sleep(1)
print "\nList all the locationName in Weather data.\n"

sql_2b = "SELECT DISTINCT(Location) FROM Weather_hour"
cursor.execute(sql_2b)
for row in cursor.fetchall():
    print row[0]

time.sleep(1)

print "----------- start 2c problem -----------"
time.sleep(1)
print "\nFind the maximum temperature value for each day and each area"
print "(North , Center , South , East) from 2016/10/01 to 2017/06/30."
print "(TAIPEI, SUN MOON LAKE, TAINAN, TAITUNG)\n"

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

for e1,e2,e3,e4 in zip(taipeis, sun_moon_lakes, tainans, taitungs) :
    print e1[0],e1[1],e1[2],e2[1],e2[2],e3[1],e3[2],e4[1],e4[2]
    
#time.sleep(1)
print "----------- start 2d problem -----------"
#time.sleep(1)
print "\nFind the highest and the lowest temperature value in Taiwan from 2016/10/01 to 2017/06/30.\n"
print "Max\tMin"
sql_2d = "  SELECT MAX(temp), MIN(temp)                                \
            FROM Weather_hour                                                               \
            WHERE Time >= '2016-10-01 00:00:00' AND Time <= '2017-06-30 23:59:59'           "
cursor.execute(sql_2d)
for row in cursor.fetchall():
    for element in row:
        print "{:.2f}".format(element),"\t",
    print ""

# Close the connection
db.close()