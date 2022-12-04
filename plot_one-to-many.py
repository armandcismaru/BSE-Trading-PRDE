import csv
import matplotlib.pyplot as plt
import numpy as np

k_value = 5
fileName = 'oneToMany_k%02d_d001_i05_0001_strats.csv' % (k_value)
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
                if k == 217:
                    defector_pps += float(row[k+1])
                else:
                    many_pps += float(row[k+1])
        many_y = np.append(many_y, float(many_pps))
        defector_y = np.append(defector_y, float(defector_pps))
        time = np.append(time, float(row[1]))

        # print('Avg PPS for many at time: ', row[1], 'is: ', many_pps/59)
        # print('PPS for defector trades at time: ', row[1], 'is: ', defector_pps)
        # print('Avg PPS for all trades at time: ', row[1], 'is: ', (many_pps + defector_pps)/60)
        # print('--------------------------------------------')

    for i in range(1, len(many_y)-1):
        if many_y[i] == 0:
            many_y[i] = (many_y[i-1] + many_y[i+1]) / 2
        if defector_y[i] == 0:
            defector_y[i] = (defector_y[i-1] + defector_y[i+1]) / 2
    
    time = time / (60*60)
    fig, ax = plt.subplots()
    plt.ylabel('Profit per second')
    plt.xlabel('Time (in hours)') 

    line, = ax.plot(time, defector_y, 'r-')  
    line.set_label('defector-profit')

    line, = ax.plot(time, many_y/59, 'b-')
    line.set_label('avg-many-profit')

    line, = ax.plot(time, (many_y + defector_y)/60, 'g-')
    line.set_label('Avg Total PPS')

    plt.legend()
    plt.show() 
    
    print('Avg PPS per delta_E for many per agent: ', (np.sum(many_y)/59) / 12)
    print('Avg PPS per delta_E for defector: ', np.sum(defector_y) / 12)
    print('% increase: ', np.sum(defector_y) / (np.sum(many_y)/59))