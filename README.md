# BSE Trading strategy PRDE, exploration of parameters k and F and extension of PRDE with JADE

This project was part of the Internet Economics & Financial Technology Masters module for Y4 TB1 MEng Computer Science, University of Bristol.

Link to the [report](ieft_report_fz19792.pdf).

## Running instructions:

All the simulations are performed by running PRDE.py. 
### Requirements: 
- python3
- numpy, matplotlib for plotting

The following command line flags are being used to specify simulation details:
- `--experiment-type` indicates the experiment to execute, namely:
  1. Balanced group tests, the default value, `--experiment-type bgr`
  2. Homogenuous group tests, `--experiment-type hmg`
  3. One-to-many tests, `--experiment-type otm`
  4. Balanced group using JADE, `--experiment-type jade`
  
- `--k-value` takes an `int` for the parameter `k` of DE
- `--F-value` takes a `float` for the parameter `F` of DE
- `--n-days` takes a `float` that specifies the number of days that the simulation will run

An example on running balanced group tests with `k=5` & `F=0.9` for a one day market would be:

`python PRDE.py --experiment-type bgr --k-value 5 --F-value 0.9 --n-days 1`
