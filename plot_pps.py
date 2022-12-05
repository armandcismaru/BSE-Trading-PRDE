import csv
import matplotlib.pyplot as plt
import numpy as np
from plot_balanced import moving_average

with open('bgr_k04_F0.80_d007_0001_strats.csv', 'r') as f:
    reader = csv.reader(f)
    base_y = []
    new_y = []
    time = []
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
    for i in range(1, len(base_y)-1):
            if base_y[i] == 0:
                base_y[i] = (base_y[i-1] + base_y[i+1]) / 2
            if new_y[i] == 0:
                new_y[i] = (new_y[i-1] + new_y[i+1]) / 2
    
    base_y = moving_average(base_y, 8)
    new_y = moving_average(new_y, 8)


    time = time / (60*60)
    time = time[:-7]

    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, base_y, 'r-')  
    line.set_label('S-profit')

    line, = ax.plot(time, new_y, 'b-')
    line.set_label('B-profit')

    line, = ax.plot(time,[base_y[i] + new_y[i] for i in range(len(base_y))], 'g-')
    line.set_label('Total PPS')

    plt.legend()
    plt.show() 