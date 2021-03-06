#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 11:29:27 2019

@author: tom verguts
goodness of recovery study for n-armed bandit model RW parameters
note: gradient-based algorithms don't work! use nelder-mead or powell (or solve the problem)
"""
#%% initialize
import numpy as np
from numpy import save
from ch6_generation import generate_learn
from ch6_estimation import estimate_learn

learning_rate, temperature = 0.6, 1

ntrials = [200]
n_sim = 10
algorithm = "Powell"
extra_label = algorithm + "_bayes_small"
data_filename = "simulation_data.csv"
results_filename = "simulation_results_" + str(n_sim) + "_" + extra_label
est_par = np.ndarray((n_sim, len(ntrials), 4)) # slice 0 = learn, slice 1 : temp, slice 2 : func_val, slice 3 : iterations
verbose = False

#%% generate and test
for n_loop in range(len(ntrials)):
    for sim_loop in range(n_sim):
        print(n_loop, sim_loop)
        generate_learn(alpha = learning_rate, beta = temperature, ntrials = ntrials[n_loop], \
                       file_name = data_filename, switch = False)
        res = estimate_learn(nstim = 4, maxiter = 10000, file_name = data_filename, algorithm = algorithm, prior = (0,10))
        est_par[sim_loop, n_loop, 0] = res.x[0]
        est_par[sim_loop, n_loop, 1] = res.x[1]
        est_par[sim_loop, n_loop, 2] = res.fun
        est_par[sim_loop, n_loop, 3] = res.success*1
        if verbose:
            print(res)
#%% the result
variables = ["learning rate", "temperature"]

for var_loop in range(len(variables)):
    par_str = ""
    for y in range(est_par.shape[1]):
        par_str = par_str + "{:.2f} ".format(np.mean(est_par[:, y, var_loop]))
    print("mean " + variables[var_loop] + " = " + par_str)

    std_str = ""
    for y in range(est_par.shape[1]):
        std_str = std_str + "{:.2f} ".format(np.std(est_par[:, y, var_loop])/np.sqrt(n_sim))
    print("standard error " + variables[var_loop] + " = " + std_str)
    
#%% wrap up
save(results_filename, est_par)