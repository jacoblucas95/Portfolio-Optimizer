#!/usr/bin/env python

import json, requests
import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize


pickle_path = os.path.join(os.path.dirname(__file__), '..', '..', 'setup', 'data', 'log_ret.pickle')
df_log_ret = pd.read_pickle(pickle_path)

def random_weights():
    data = []
    weight_dict = {}
    weights = np.array(np.random.random(9))
    weights = weights / np.sum(weights)
    for col in df_log_ret.columns:
        for weight in weights:
            weight_dict[col] = weight
    exp_ret = np.sum(df_log_ret.mean() * weights) * 252
    exp_vol = np.sqrt(np.dot(weights.T, np.dot(df_log_ret.cov() * 252, weights)))
    SR = exp_ret / exp_vol
    data.append(weight_dict)
    return data

def get_ret_vol_sr(weights):
    weights = np.array(weights)
    ret = np.sum(df_log_ret.mean() * weights) * 252
    vol = np.sqrt(np.dot(weights.T, np.dot(df_log_ret.cov() * 252, weights)))
    sr = ret / vol
    return np.array([ret,vol,sr])

def neg_sharpe(weights):
    return get_ret_vol_sr(weights)[2] * -1

def check_sum(weights):
    return np.sum(weights) -1

def check_sum_eq(weights):
    return np.sum(weights[0:4]) -0.9

cons = ({'type':'eq', 'fun': check_sum}, {'type':'eq','fun': check_sum_eq})
bounds = ((0,.5),(0,.5),(0,.5),(0,.5),(0,0.5),(0,.5),(0,.5),(0,.5),(0,.5))
init_guess = [(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9)]
opt_results = minimize(neg_sharpe,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
get_ret_vol_sr(opt_results.x)

def minimize_volatility(weights):
    return get_ret_vol_sr(weights)[1]


def ret_vol_allos():
    data = []
    frontier_y = np.linspace(0,0.05,10)
    frontier_volatility = []
    # vol_allo_dict = {}

    for possible_return in frontier_y:
        cons = ({'type':'eq','fun':check_sum},
                {'type':'eq','fun': check_sum_eq},
                {'type':'eq','fun':lambda w: get_ret_vol_sr(w)[0] - possible_return})

        result = minimize(minimize_volatility,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
        frontier_volatility.append(result['fun'])
        ret_vol_sr = get_ret_vol_sr(result.x)
        allo = result.x
        allo_ls = allo.tolist()
        vol_allo_dict = {
            'volatility': ret_vol_sr[1],
            'return': ret_vol_sr[0],
            'sharpe': ret_vol_sr[2],
            'allocations': allo_ls
        }
        # vol_allo_dict['volatility'] = ret_vol_sr[1]
        # vol_allo_dict['volatility'][ret_vol_sr[1]] = allo_ls

        data.append(vol_allo_dict)

    return data
