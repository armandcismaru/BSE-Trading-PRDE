import csv
import matplotlib.pyplot as plt
import numpy as np

new_k = 6
new_f = 1.6

def moving_average(arr, window_size):
    i = 0
    moving_averages = []
    
    while i < len(arr) - window_size + 1:
        window = arr[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)

        i += 1

    return moving_averages

with open('Trial_k%02d_F%2.2f_d007_0004_strats.csv' % (new_k, new_f), 'r') as f:
    reader = csv.reader(f)
    base_y = []
    new_y = []
    time = []
    last = []

    for row in reader:
        base_pps = 0
        new_pps = 0
        for k, elem in enumerate(row):
            if 'actvprof' in elem:
                if k % 2 == 0:
                    new_pps += float(row[k+1])
                else:
                    base_pps += float(row[k+1])
            if row[1] == '601200':
                if 'actvprof' in elem:
                    last.append(float(row[k+1]))

        base_y = np.append(base_y, float(base_pps))
        new_y = np.append(new_y, float(new_pps))
        time = np.append(time, float(row[1]))

        # print('PPS for all trades at time: ', row[1], 'is: ', seller_pps + buyer_pps)
        # print('PPS for seller trades at time: ', row[1], 'is: ', seller_pps)
        # print('PPS for buyer trades at time: ', row[1], 'is: ', buyer_pps)
        # print('--------------------------------------------')


    print(f'k={new_k} F={new_f} avg PPS for base per agent: ', (np.sum(base_y)/12))
    print(f'k={new_k} F={new_f} avg PPS for new per agent: ', (np.sum(new_y)/12))
    print('Percentage increase: ', (np.sum(new_y)/12) / (np.sum(base_y)/12) - 1)

    for i in range(1, len(base_y)-1):
            if base_y[i] == 0:
                base_y[i] = (base_y[i-1] + base_y[i+1]) / 2
            if new_y[i] == 0:
                new_y[i] = (new_y[i-1] + new_y[i+1]) / 2
    
    base_y = moving_average(base_y, 8)
    new_y = moving_average(new_y, 8)

    time = time / (60*60)
    time = time[:-7]

    # fig, ax = plt.subplots()
    # plt.ylabel('Profit per second')
    # plt.xlabel('Time (in hours)') 

    # line, = ax.plot(time, base_y, 'r-')  
    # line.set_label('base-profit')

    # line, = ax.plot(time, new_y, 'b-')
    # line.set_label('new-profit')
 
    # line, = ax.plot(time, [base_y[i] + new_y[i] for i in range(len(base_y))], 'g-')
    # line.set_label('Total PPS')

    # plt.legend()
    #plt.show() 

    #plot_sup_dem(12, [(65,190)], 12, [(65,190)], 'fixed')
   
    # x_axis = [i for i in range(0, 60)]
    # fig, ax = plt.subplots()
    # ax.plot(x_axis, last, color="gray")
    # ax.axvline(x=len(x_axis) / 2, color="red")

    # plt.xlabel('Buyer/Seller')
    # plt.ylabel('Profit per second') 
    # plt.show()