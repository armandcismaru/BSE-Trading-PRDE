import csv
import matplotlib.pyplot as plt
import numpy as np
from PRDE import plot_trades

new_k = 4
new_f = 0.8

def moving_average(arr, window_size):
    i = 0
    moving_averages = []
    
    while i < len(arr) - window_size + 1:
        window = arr[i : i + window_size]
        window_average = round(sum(window) / window_size, 2)
        moving_averages.append(window_average)

        i += 1

    return moving_averages

all = []
is_this_for_jade = True

for i in range(1,2):
    with open('jade_k%02d_F%2.2f_d07_%02d_strats.csv' % (new_k, new_f, 23), 'r') as f:
        reader = csv.reader(f)
        base_y = []
        new_y = []
        time = []
        last = []

        for row in reader:
            base_pps = 0
            new_pps = 0
            for k, elem in enumerate(row):
                if is_this_for_jade:
                    if 'PRJADE' in elem:
                        new_pps += float(row[k+4])
                    elif 'PRDE' in elem:
                        base_pps += float(row[k+4])
                else:
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


        print(f'k={new_k} F={new_f} avg PPS for base per agent: ', (np.sum(base_y)/12))
        print(f'k={new_k} F={new_f} avg PPS for new per agent: ', (np.sum(new_y)/12))
        print('Percentage increase: ', (np.sum(new_y)/12) / (np.sum(base_y)/12) - 1)
    
    all.append((np.sum(new_y)/12) / (np.sum(base_y)/12) - 1)
    print('Average percentage increase: ', np.average(all))

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
    line.set_label('PRDE profis')

    line, = ax.plot(time, new_y, 'b-')
    line.set_label('JADE profits')
 
    line, = ax.plot(time, [base_y[i] + new_y[i] for i in range(len(base_y))], 'g-')
    line.set_label('Total profits')

    plt.legend()
    plt.show() 

    #plot_sup_dem(12, [(65,190)], 12, [(65,190)], 'fixed')
   
    # x_axis = [i for i in range(0, 60)]
    # fig, ax = plt.subplots()
    # ax.plot(x_axis, last, color="gray")
    # ax.axvline(x=len(x_axis) / 2, color="red")

    # plt.xlabel('Buyer/Seller')
    # plt.ylabel('Profit per second') 
    # plt.show()