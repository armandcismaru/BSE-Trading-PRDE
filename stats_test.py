import csv
import numpy as np

resdump = open('stats_test.csv', 'w')
resdump.write('new_profits,base_profits\n')
trials = 22

for trial in range(trials):
    base_y = []
    new_y = []
    with open('Trial_k%02d_F%2.2f_d07_%02d_strats.csv' % (4, 1.8, trial), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            base_pps = 0
            new_pps = 0
            for k, elem in enumerate(row):
                if 'actvprof' in elem:
                    if k % 2 == 0:
                        new_pps += float(row[k+1])
                    else:
                        base_pps += float(row[k+1])

            base_y = np.append(base_y, float(base_pps))
            new_y = np.append(new_y, float(new_pps))
        
        resdump.write('%3.3f,' % (np.sum(new_y) / 12))
        resdump.write('%3.3f\n' % (np.sum(base_y) / 12))

    
resdump.close()
    