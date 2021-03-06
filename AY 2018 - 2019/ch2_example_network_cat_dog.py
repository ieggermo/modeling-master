#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 11:15:54 2018

@author: Mehdi Senoussi
"""
import numpy as np
import time
from course_functions import plot_network, update_network

timesleep = .2
n_tsteps = 100
times = np.arange(n_tsteps)
t = 1
# output units
ydog = np.zeros(n_tsteps)
ycat = np.zeros(n_tsteps)
incat = np.zeros(n_tsteps)
indog = np.zeros(n_tsteps)
# std of noise
sigma = .25
# learning rate
alpha = .2

#
layers = np.array([1, 1, 1, 2, 2])
n_units = len(layers)
activations = np.array([1., 0., 0., 0., 0.])
weights = np.zeros(shape=[n_units, n_units])

# setting up weights for the cat-dog detector; note example is different from in book.
weights[0, 3] = .4 # cats often bite visitors
weights[0, 4] = .1 # dogs rarely bite visitors
weights[1, 3] = .2 # cats often have four legs
weights[1, 4] = .2 # dogs often have four legs
weights[2, 3] = .1 # cats rarely have their pictures on FB
weights[2, 4] = .4 # dogs often have their pictures on FB
weights[3, 4] = -.2 # a cat cannot be a dog, and vice versa

# computing the initial y activation values
incat = weights[0, 3] * activations[0] + weights[1, 3] * activations[1] + weights[2, 3] * activations[2]
indog = weights[0, 4] * activations[0] + weights[1, 4] * activations[1] + weights[2, 4] * activations[2]
ycat[t] = ycat[t-1] + alpha * (incat + weights[3, 4] * ydog[t-1]) + np.random.randn()*sigma
ydog[t] = ydog[t-1] + alpha * (indog + weights[3, 4] * ycat[t-1]) + np.random.randn()*sigma
activations[3:] = [ycat[t], ydog[t]]
energy = -incat*ycat[t] - indog*ydog[t] - weights[3, 4]*ycat[t]*ydog[t]

fig, axs, texts_handles, lines_handles, unit_pos =\
    plot_network(figsize = [13, 7], activations = activations,
                  weights = weights, layers = layers, energy = energy)


for t in times[1:]:
    ycat[t] = ycat[t-1] + alpha * (incat + weights[3, 4] * ydog[t-1]) + np.random.randn()*sigma
    ydog[t] = ydog[t-1] + alpha * (indog + weights[3, 4] * ycat[t-1]) + np.random.randn()*sigma
    if ycat[t]<0 : ycat[t] = 0
    if ydog[t]<0: ydog[t] = 0
    activations[3:] = [ycat[t], ydog[t]]
    energy = -incat*ycat[t] - indog*ydog[t] - weights[3, 4]*ycat[t]*ydog[t]
    
    update_network(fig = fig, axs = axs, texts_handles = texts_handles,
        lines_handles = lines_handles, activations = activations,
        unit_pos = unit_pos, weights = weights, layers = layers, change = 0,
        cycle = t, energy = energy)

    time.sleep(timesleep)


