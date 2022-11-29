import csv
import matplotlib.pyplot as plt
import numpy as np

fileName = 'oneToMany_k05_d001_i05_0001_strats.csv'
with open(fileName, 'r') as f:
    reader = csv.reader(f)
    many_y = []
    defector_y = []
    time = []

    for row in reader:
        many_pps = 0
        defector_pps = 0
        for k, elem in enumerate(row):
            if 'actvprof' in elem:
                if k == 219:
                    defector_pps += float(row[k+1])
                else:
                    many_pps += float(row[k+1])
        many_y = np.append(many_y, float(many_pps))
        defector_y = np.append(defector_y, float(defector_pps))
        time = np.append(time, float(row[1]))

        print('PPS for many at time: ', row[1], 'is: ', many_pps)
        print('PPS for defector trades at time: ', row[1], 'is: ', defector_pps)
        print('PPS for all trades at time: ', row[1], 'is: ', many_pps + defector_pps)
        print('--------------------------------------------')

    time = time / (60*60)
    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, defector_y, 'r-')  
    line.set_label('defector-profit')

    line, = ax.plot(time, many_y, 'b-')
    line.set_label('many-profit')

    line, = ax.plot(time, many_y + defector_y, 'g-')
    line.set_label('Total PPS')

    plt.legend()
    plt.show() 