import csv
import matplotlib.pyplot as plt
import numpy as np

with open('bse_d001_i05_0001_strats.csv', 'r') as f:
    reader = csv.reader(f)
    seller_y = []
    buyer_y = []
    time = []

    for row in reader:
        seller_pps = 0
        buyer_pps = 0
        for k, elem in enumerate(row):
            if 'actvprof' in elem:
                if k > 212:
                    seller_pps += float(row[k+1])
                else:
                    buyer_pps += float(row[k+1])
        seller_y = np.append(seller_y, float(seller_pps))
        buyer_y = np.append(buyer_y, float(buyer_pps))
        time = np.append(time, float(row[1]))

        print('PPS for all trades at time: ', row[1], 'is: ', seller_pps + buyer_pps)
        print('PPS for seller trades at time: ', row[1], 'is: ', seller_pps)
        print('PPS for buyer trades at time: ', row[1], 'is: ', buyer_pps)
        print('--------------------------------------------')

    time = time / (60*60)
    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, seller_y, 'r-')  
    line.set_label('S-profit')

    line, = ax.plot(time, buyer_y, 'b-')
    line.set_label('B-profit')

    line, = ax.plot(time, seller_y + buyer_y, 'g-')
    line.set_label('Total PPS')

    plt.legend()
    plt.show() 