import csv
import matplotlib.pyplot as plt
import numpy as np

new_k = 6
new_f = 0.2
trial = 1

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

with open('k%02d_F%2.2f_d007_00%02d_strats.csv' % (new_k, new_f, trial), 'r') as f:
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
                    # else:
                    #     new_pps += float(row[k+1])

        base_y = np.append(base_y, float(base_pps))
        new_y = np.append(new_y, float(new_pps))
        time = np.append(time, float(row[1]))

        # print('PPS for all trades at time: ', row[1], 'is: ', seller_pps + buyer_pps)
        # print('PPS for seller trades at time: ', row[1], 'is: ', seller_pps)
        # print('PPS for buyer trades at time: ', row[1], 'is: ', buyer_pps)
        # print('--------------------------------------------')


    print(f'k={new_k} F={new_f} avg PPS for base per agent: ', (np.sum(base_y)/15))
    print(f'k={new_k} F={new_f} avg PPS for new per agent: ', (np.sum(new_y)/15))
    print('Percentage increase: ', (np.sum(new_y)/15) / (np.sum(base_y)/15) - 1)

    # for i in range(1, len(base_y)-1):
    #     if base_y[i] == 0:
    #         base_y[i] = (base_y[i-1] + base_y[i+1]) / 2
    #     if new_y[i] == 0:
    #         new_y[i] = (new_y[i-1] + new_y[i+1]) / 2

    # base_y = moving_average(base_y, 2)
    # new_y = moving_average(new_y, 2)


    # print(f'k={new_k} F={new_f} avg PPS for base per agent: ', (base_y[len(base_y)-2]))
    # print(f'k={new_k} F={new_f} avg PPS for new per agent: ', (new_y[len(base_y)-2]))

    # nt = len(base_y) - 2
    # change = (new_y[nt]) / (base_y[nt]) - 1
    # print('Percentage increase: ', change)

    # for i in range(1, len(base_y)-1):
    #         if base_y[i] == 0:
    #             base_y[i] = (base_y[i-1] + base_y[i+1]) / 2
    #         if new_y[i] == 0:
    #             new_y[i] = (new_y[i-1] + new_y[i+1]) / 2
    # print(len(base_y + new_y))

    time = time / (60*60)
    # time = time[:-1]

    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, base_y, 'r-')  
    line.set_label('base-profit')

    line, = ax.plot(time, new_y, 'b-')
    line.set_label('new-profit')
 
    line, = ax.plot(time, [base_y[i] + new_y[i] for i in range(len(base_y))], 'g-')
    line.set_label('Total PPS')

    plt.legend()
    plt.show() 

    