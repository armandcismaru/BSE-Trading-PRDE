import csv
import matplotlib.pyplot as plt
import numpy as np

with open('bse_d001_i05_0001_strats.csv', 'r') as f:
    reader = csv.reader(f)
    y = []
    for row in reader:
        y = np.append(y, float(row[0]))
        print(row[0], row[1])
        break
