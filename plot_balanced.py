import csv
import matplotlib.pyplot as plt
import numpy as np

new_k = 10
with open('balancedGroups_k%02d_d001_i05_0001_strats.csv' % (new_k), 'r') as f:
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
        
    time = time / (60*60)
    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, base_y, 'r-')  
    line.set_label('base-profit')

    line, = ax.plot(time, new_y, 'b-')
    line.set_label('new-profit')

    line, = ax.plot(time, base_y + new_y, 'g-')
    line.set_label('Total PPS')

    plt.legend()
    #plt.show() 

    print(f'k={new_k} avg PPS for base per agent: ', (np.sum(base_y)/15)/12)
    print(f'k={new_k} avg PPS for new per agent: ', (np.sum(new_y)/15)/12)