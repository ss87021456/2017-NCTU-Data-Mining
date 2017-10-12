import csv, pprint

filenames = list()

for i in range(1, 24, 1):
	if i/10 :
		if i == 10:
			pass
		else:
			filenames.append("2017-09-"+str(i)+".csv")
	else :
		filenames.append("2017-09-0"+str(i)+".csv")

pprint.pprint(filenames)

with open('September.csv','w') as fw:
	powerWriter = csv.writer(fw)

	for filename in filenames:
		with open(filename,'r') as fr:
			powerReader = csv.reader(fr)
			for row in powerReader:
				if filename != '2017-09-01.csv':
					row[0] = filename[:-4]+" "+row[0]+":00"
				powerWriter.writerow(row)
		fr.close()

fw.close()
