import csv
import unicodecsv

with open('doctors.csv', 'r') as infile, open("doctors-new.csv", 'ab') as outfile:
    rows = unicodecsv.reader(infile, delimiter=',', encoding='ISO-8859-1')
    count = 0
    writer = unicodecsv.writer(outfile, delimiter=',')	
    for row in rows:
	newrow = []
	if(count == 0):
	    writer.writerow(row)
	    count = 1
	    continue 
	
	newrow.append(str(count))
	for i in row:
	    newrow.append(i.encode('utf-8'))
	writer.writerow(newrow)
	count = count + 1	
		

	    
