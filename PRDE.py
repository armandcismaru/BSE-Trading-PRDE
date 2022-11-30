import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import random
import argparse

from BSE import market_session

parser = argparse.ArgumentParser(
    description="Run market sessions on BSE",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--experiment-type", default='default', type=str, help="Type of experiment")
parser.add_argument("--k-value", default=4, type=int, help="Value of k")
parser.add_argument("--F-value", default=0.8, type=float, help="Value of F")

def plot_trades(trial_id):
    prices_fname = trial_id + '_tape.csv'
    x = np.empty(0)
    y = np.empty(0)
    with open(prices_fname, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            time = float(row[1])
            price = float(row[2])
            x = np.append(x,time)
            y = np.append(y,price)

    plt.plot(x, y, 'x', color='black') 
    
def n_runs_plot_trades(n, trial_id, start_time, end_time, traders_spec, order_sched):
    x = np.empty(0)
    y = np.empty(0)

    for i in range(n):
        trialId = trial_id + '_' + str(i)
        tdump = open(trialId + '_avg_balance.csv','w')

        market_session(trialId, start_time, end_time, traders_spec, order_sched, tdump, True, False)
        
        tdump.close()

        with open(trialId + '_tape.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                time = float(row[1])
                price = float(row[2])
                x = np.append(x,time)
                y = np.append(y,price)

    plt.plot(x, y, 'x', color='black');
   
def getorderprice(i, sched, n, mode):
    pmin = min(sched[0][0], sched[0][1])
    pmax = max(sched[0][0], sched[0][1])
    prange = pmax - pmin
    stepsize = prange / (n - 1)
    halfstep = round(stepsize / 2.0)

    if mode == 'fixed':
        orderprice = pmin + int(i * stepsize)
    elif mode == 'jittered':
        orderprice = pmin + int(i * stepsize) + random.randint(-halfstep, halfstep)
    elif mode == 'random':
        if len(sched) > 1:
            # more than one schedule: choose one equiprobably
            s = random.randint(0, len(sched) - 1)
            pmin = min(sched[s][0], sched[s][1])
            pmax = max(sched[s][0], sched[s][1])
        orderprice = random.randint(pmin, pmax)
    return orderprice    

def make_supply_demand_plot(bids, asks):
    # total volume up to current order
    volS = 0
    volB = 0

    fig, ax = plt.subplots()
    plt.ylabel('Price')
    plt.xlabel('Quantity')
    
    pr = 0
    for b in bids:
        if pr != 0:
            # vertical line
            ax.plot([volB,volB], [pr,b], 'r-')
        # horizontal lines
        line, = ax.plot([volB,volB+1], [b,b], 'r-')
        volB += 1
        pr = b
    if bids:
        line.set_label('Demand')
        
    pr = 0
    for s in asks:
        if pr != 0:
            # vertical line
            ax.plot([volS,volS], [pr,s], 'b-')
        # horizontal lines
        line, = ax.plot([volS,volS+1], [s,s], 'b-')
        volS += 1
        pr = s
    if asks:
        line.set_label('Supply')
        
    if bids or asks:
        plt.legend()
    plt.show()

# Use this to plot supply and demand curves from supply and demand ranges and stepmode
def plot_sup_dem(seller_num, sup_ranges, buyer_num, dem_ranges, stepmode):
    asks = []
    for s in range(seller_num):
        asks.append(getorderprice(s, sup_ranges, seller_num, stepmode))
    asks.sort()
    bids = []
    for b in range(buyer_num):
        bids.append(getorderprice(b, dem_ranges, buyer_num, stepmode))
    bids.sort()
    bids.reverse()
    
    make_supply_demand_plot(bids, asks) 

# plot sorted trades, useful is some situations - won't be used in this worksheet
def in_order_plot(trial_id):
    prices_fname = trial_id + '_tape.csv'
    y = np.empty(0)
    with open(prices_fname, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            price = float(row[2])
            y = np.append(y,price)
    y = np.sort(y)
    x = list(range(len(y)))

    plt.plot(x, y, 'x', color='black')   

# plot offset function
def plot_offset_fn(offset_fn, total_time_seconds):   
    x = list(range(total_time_seconds))
    offsets = []
    for i in range(total_time_seconds):
        offsets.append(offset_fn(i))
    plt.plot(x, offsets, 'x', color='black')  

def schedule_offsetfn(t):
        t /= 100
        pi2 = math.pi * 2
        c = math.pi * 3000
        wavelength = t / c
        gradient = 100 * t / (c / pi2)
        amplitude = 100 / (c / pi2)
        offset = gradient + amplitude * math.sin(wavelength)
        return int(round(offset, 0))

def run_experiments(experiment_type, k_value, F_value, traders_spec):
    n_days = 1.0
    start_time = 0.0
    end_time = 60.0 * 60.0 * 24 * n_days
    duration = end_time - start_time

    # sup_range = (60, 60)
    # dem_range = (140, 140)

    range1 = (65, 140)
    range2 = (200, 270)

    
    supply_schedule = [ {'from':start_time, 'to':duration/3, 'ranges':[range1], 'stepmode':'fixed'},
                        {'from':duration/3, 'to':2*duration/3, 'ranges':[range2], 'stepmode':'fixed'},
                        {'from':2*duration/3, 'to':end_time, 'ranges':[range1], 'stepmode':'fixed'}
                        ]
    demand_schedule = supply_schedule

    # supply_schedule = [{'from': start_time, 'to': end_time, 'ranges': [sup_range], 'stepmode': 'fixed'}]
    # demand_schedule = [{'from': start_time, 'to': end_time, 'ranges': [dem_range], 'stepmode': 'fixed'}]

    order_interval = 5
    order_sched = {'sup': supply_schedule , 'dem': demand_schedule, 'interval': order_interval, 'timemode': 'drip-jitter'}

    n_trials = 1
    trial = 1

    while trial < (n_trials + 1):
        trial_id = '%s_k%02d_F%2.2f_d%03d_%04d' % (experiment_type, k_value, F_value, n_days, trial)
        tdump = open(f'{trial_id}_avg_balance.csv','w')
        dump_all = False
        verbose = True

        market_session(trial_id, start_time, end_time, traders_spec, order_sched, tdump, dump_all, verbose)

        tdump.close()
        trial += 1

def main(args):
    experiment_type = args.experiment_type
    k_value = args.k_value
    F_value = args.F_value

    if experiment_type == 'default':
        sellers_spec = [('PRDE', 30, {'k': 4, 'F': 0.8, 's_min': -1.0, 's_max': +1.0})]
        buyers_spec = sellers_spec
        
    elif experiment_type == 'otm':
        sellers_spec = [('PRDE', 1, {'k': k_value, 'F': F_value, 's_min': -1.0, 's_max': +1.0}), 
                        ('PRDE', 29, {'k': 4, 'F': 0.8, 's_min': -1.0, 's_max': +1.0})]

        buyers_spec = [('PRDE', 30, {'k': 4, 'F': 0.8, 's_min': -1.0, 's_max': +1.0})]
    elif experiment_type == 'bgr':
        sellers_spec = [('PRDE', 15, {'k': k_value, 'F': F_value, 's_min': -1.0, 's_max': +1.0}), 
                        ('PRDE', 15, {'k': 4, 'F': 0.8, 's_min': -1.0, 's_max': +1.0})]

        buyers_spec = [('PRDE', 15, {'k': 4, 'F': 0.8, 's_min': -1.0, 's_max': +1.0}), 
                       ('PRDE', 15, {'k': k_value, 'F': F_value, 's_min': -1.0, 's_max': +1.0})]

    traders_spec = {'sellers': sellers_spec, 'buyers': buyers_spec}
    run_experiments(experiment_type, k_value, F_value, traders_spec)

if __name__ == "__main__":
    main(parser.parse_args())