import xml.etree.ElementTree as ET
import pprint
import csv
import datetime, time

def correct_date(old):
	year, month = int(old[:4]), int(old[5:7])
	day, hour = int(old[8:10]), int(old[11:13])
	minu, sec = int(old[14:16]), int(old[17:19])
	old = (year,month,day,hour,minu,sec,0,1,-1)
	timestamp = time.mktime(old)
	new = datetime.datetime.fromtimestamp(timestamp)
	return new

Weather_data = 'Weather.xml'

tree = ET.parse(Weather_data)
root = tree.getroot()
dataset = root[0]

data_per_hour = []
data_per_day = []

per_hour_count = 0
per_day_count = 0

with open("Weather_hour.csv", "w") as hf, open("Weather_day.csv", "w") as df:
	hourWriter = csv.writer(hf)
	dayWriter = csv.writer(df)

	for locations in dataset:
		#print locations.tag
		#print len(locations)
		name = locations[0].text.split(",")[0]
		for location in locations:
			if location.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}weatherElement':
				for element in location:
					if element.tag == '{urn:cwb:gov:tw:cwbcommon:0.1}time':
						if len(element) == 7:
							daytime = element[0].text+":00"
							daytime = correct_date(daytime)
							print daytime
							pressure, temp = element[1][1][0].text, element[2][1][0].text
							rela_humid, wind_speed = element[3][1][0].text, element[4][1][0].text
							wind_dir, rainfall = element[5][1][0].text.split(',')[1], element[6][1][0].text
							if rainfall == 'T':
								rainfall = 0
							hourWriter.writerow([name, daytime, pressure, temp, rela_humid, wind_speed, wind_dir, rainfall, 0])
							per_hour_count += 1

						elif len(element) == 8:
							daytime = element[0].text+":00"
							daytime = correct_date(daytime)
							print daytime
							pressure, temp = element[1][1][0].text, element[2][1][0].text
							rela_humid, wind_speed = element[3][1][0].text, element[4][1][0].text
							wind_dir, rainfall = element[5][1][0].text.split(',')[1], element[6][1][0].text
							sun_time = element[7][1][0].text
							if rainfall == 'T':
								rainfall = 0
							hourWriter.writerow([name, daytime, pressure, temp, rela_humid, wind_speed, wind_dir, rainfall, sun_time])
							per_hour_count += 1

						elif len(element) == 4:
							daytime, max_temp = element[0].text,element[1][1][0].text
							min_temp, avg_temp = element[2][1][0].text, element[3][1][0].text
							dayWriter.writerow([name, daytime, max_temp, min_temp, avg_temp])
							per_day_count += 1
						print "per hour data num:",per_hour_count
						print "per day data num:",per_day_count

df.close()
hf.close()

print "per hour data num:",per_hour_count
print "per day data num:",per_day_count