import csv
import matplotlib.pyplot as plt
import numpy as np

namelist = os.listdir('../doubleline_text/')

for item in namelist:
	csvfile = file('../doubleline_text/'+item)
	reader = csv.reader(csvfile)


