import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

csv.field_size_limit(sys.maxsize)
csvfile = file('../../rawdata/Wechat_OA/10544_20160101_mod1k.csv', 'r')
reader = csv.reader(csvfile)
count = 0
for line in reader:
  if line[0] == '20161020':
    count += 1
  
