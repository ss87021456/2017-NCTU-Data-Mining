import json,pprint,csv

def convert(old_time):

	year = str(int(old_time[:3])+1911)
	month, day = old_time[4:6], old_time[7:9]
	time = old_time[-5:]+":00"
	new_time = year+"-"+month+"-"+day+" "+time

	return new_time

f = open('power.json','r')
s = f.read()

book = json.loads(s)
#pprint.pprint(book)
with open('2017-09-01.csv','w') as fw:
	powerWriter = csv.writer(fw)
	for day in book:
		time = convert(day['reserveData']['updateTime'])
		northSupply = day['regionData']['northSupply']
		northUsage = day['regionData']['northUsage']
		centerSupply = day['regionData']['centerSupply']
		centerUsage = day['regionData']['centerUsage']
		southSupply = day['regionData']['southSupply']
		southUsage = day['regionData']['southUsage']
		eastSupply = day['regionData']['eastSupply']
		eastUsage = day['regionData']['eastUsage']
		powerWriter.writerow([time,northSupply,northUsage,centerSupply,centerUsage,southSupply,southUsage,eastSupply,eastUsage])

fw.close()
