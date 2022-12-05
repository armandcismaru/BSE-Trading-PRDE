import csv
import matplotlib.pyplot as plt
import numpy as np

def moving_average(arr, window_size):
    window_size = 2
    i = 0
    moving_averages = []
    
    while i < len(arr) - window_size + 1:
        window = arr[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)

        i += 1

    return moving_averages

k_values = [4, 5, 6, 7]
F_values = [round(i * 0.1, 2) for i in range(21)]

resdump = open('exp_results.csv', 'w')
n_eval_periods = 7 * 24 / 2

for kval in k_values:
    for f in F_values:
        base_y = []
        new_y = []
        time = []
        with open('Final_k%02d_F%2.2f_d007_0001_strats.csv' % (kval, f), 'r') as file:
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
                
                time = np.append(time, float(row[1]))

                # print('PPS for all trades at time: ', row[1], 'is: ', seller_pps + buyer_pps)
                # print('PPS for seller trades at time: ', row[1], 'is: ', seller_pps)
                # print('PPS for buyer trades at time: ', row[1], 'is: ', buyer_pps)
                # print('--------------------------------------------')

        # for i in range(1, len(base_y)-1):
        #     if base_y[i] == 0:
        #         base_y[i] = (base_y[i-1] + base_y[i+1]) / 2
        #     if new_y[i] == 0:
        #         new_y[i] = (new_y[i-1] + new_y[i+1]) / 2

        # base_y = moving_average(base_y, 2)
        # new_y = moving_average(new_y, 2)
        change = (np.sum(new_y)/15) / (np.sum(base_y)/15) - 1

        # nt = len(base_y) - 2
        # change = (new_y[nt]) / (base_y[nt]) - 1
        
        resdump.write('%2.3f,' % (change))
    resdump.write('\n')
resdump.close()