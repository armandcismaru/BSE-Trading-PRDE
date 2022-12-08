import csv
import numpy as np

resdump = open('stats_test.csv', 'w')
resdump.write('JADE Profits,PRDE Profits\n')
trials = 28

for trial in range(1, trials):
    base_y = []
    new_y = []
    with open('jade_k%02d_F%2.2f_d07_%02d_strats.csv' % (4, 0.8, trial), 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            base_pps = 0
            new_pps = 0
            for k, elem in enumerate(row):
                if 'PRJADE' in elem:
                    new_pps += float(row[k+4])
                elif 'PRDE' in elem:
                    base_pps += float(row[k+4])

            base_y = np.append(base_y, float(base_pps))
            new_y = np.append(new_y, float(new_pps))
        
        resdump.write('%3.3f,' % (np.sum(new_y) / 12))
        resdump.write('%3.3f\n' % (np.sum(base_y) / 12))

    
resdump.close()
    