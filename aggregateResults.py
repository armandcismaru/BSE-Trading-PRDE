import csv
import matplotlib.pyplot as plt
import numpy as np

k_values = [4, 5, 6, 7]
F_values = [round(i * 0.1, 2) for i in range(21)]
resdump = open('exp_results.csv', 'w')

for k in k_values:
    for f in F_values:
        base_y = []
        new_y = []
        time = []
        with open(f'bgr_k0{k}_F{f}_d001_0001_strats.csv', 'r') as file:
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

        resdump.write('%2.2f,' % ((np.sum(base_y)/15/12) / (np.sum(new_y)/15/12)))
    resdump.write('\n')
resdump.close()