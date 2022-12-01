import csv
import matplotlib.pyplot as plt
import numpy as np

# k_values = [4, 5, 6, 7]
# F_values = [round(i * 0.1, 2) for i in range(21)]
k_values = [5]
# F_values = [0.00, 0.10, 0.20, 0.30, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
F_values = [0.00, 0.10, 0.20, 0.30, 0.4, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.1, 1.2, 1.3, 1.4, 1.5, 1.8, 1.9]


resdump = open('exp_results.csv', 'w')
n_eval_periods = 7 * 24 / 2

for kval in k_values:
    for f in F_values:
        base_y = []
        new_y = []
        time = []
        with open('bgr_k%02d_F%2.2f_d007_0001_strats.csv' % (kval, f), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                base_pps = 0
                new_pps = 0
                for k, elem in enumerate(row):
                    if 'actvprof' in elem:
                        if k > 212:
                            if k > 319:
                                base_pps += float(row[k+1])
                            else:
                                new_pps += float(row[k+1])
                        else:
                            if k > 109:
                                base_pps += float(row[k+1])
                            else:
                                new_pps += float(row[k+1])

                base_y = np.append(base_y, float(base_pps))
                new_y = np.append(new_y, float(new_pps))
                time = np.append(time, float(row[1]))

                # print('PPS for all trades at time: ', row[1], 'is: ', seller_pps + buyer_pps)
                # print('PPS for seller trades at time: ', row[1], 'is: ', seller_pps)
                # print('PPS for buyer trades at time: ', row[1], 'is: ', buyer_pps)
                # print('--------------------------------------------')

        change = (np.sum(new_y)/15/n_eval_periods) / (np.sum(base_y)/15/n_eval_periods) - 1
        resdump.write('%2.2f,' % (change))
        # resdump.write('%2.3f,' % ((np.sum(base_y)/15/12) / (np.sum(new_y)/15/12)))
    resdump.write('\n')
resdump.close()