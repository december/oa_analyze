import csv

csvfile = file('../doubleline_text/'+item)
reader = csv.reader(csvfile)
for line in reader:
	singlefile.append(line)
csvfile.close()
