#!/usr/bin/env python

import json, requests
import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize

close_pickle_path = os.path.join(os.path.dirname(__file__), '..', '..', 'setup', 'data', 'stock_close.pickle')
df_stock_close = pd.read_pickle(close_pickle_path)
log_pickle_path = os.path.join(os.path.dirname(__file__), '..', '..', 'setup', 'data', 'log_ret.pickle')
df_log_ret = pd.read_pickle(log_pickle_path)


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
    return get_ret_vol_sr(weights)[2] * - 1

def check_sum(weights):
    return np.sum(weights) - 1

def check_sum_eq_25(weights):
    return np.sum(weights[0:4]) - 0.25

def check_sum_eq_50(weights, eq_pct):
    return np.sum(weights[0:4]) - 0.50

def check_sum_eq_75(weights):
    return np.sum(weights[0:4]) - 0.75

def check_sum_eq_90(weights):
    return np.sum(weights[0:4]) - 0.90

def minimize_volatility(weights):
    return get_ret_vol_sr(weights)[1]

def ret_vol_allos(portfolio_makeup, volatility):
    bounds = ((0,.5),(0,.5),(0,.5),(0,.5),(0,0.5),(0,.5),(0,.5),(0,.5),(0,.5))
    init_guess = [(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9),(1/9)]
    return_dict = {}
    data = []
    frontier_y = np.linspace(0,0.08,10)
    frontier_volatility = []

    if portfolio_makeup == .25:
        check_sum_eq = check_sum_eq_25
    elif portfolio_makeup == 0.50:
        check_sum_eq = check_sum_eq_50
    elif portfolio_makeup == 0.75:
        check_sum_eq = check_sum_eq_75
    else:
        check_sum_eq = check_sum_eq_90

    for possible_return in frontier_y:
        cons = ({'type':'eq','fun':check_sum},
                {'type':'eq','fun': check_sum_eq},
                {'type':'eq','fun':lambda w: get_ret_vol_sr(w)[0] - possible_return})

        result = minimize(minimize_volatility,init_guess,method='SLSQP',bounds=bounds,constraints=cons)
        frontier_volatility.append(result['fun'])
        ret_vol_sr = get_ret_vol_sr(result.x)
        allo = result.x
        allo_ls = allo.tolist()
        vol_allo_dict = [{
                'allocations': [
                    {'ticker':'VTI', 'weight': allo_ls[0]},
                    {'ticker':'VEA', 'weight': allo_ls[1]},
                    {'ticker':'VWO', 'weight': allo_ls[2]},
                    {'ticker':'VNQ', 'weight': allo_ls[3]},
                    {'ticker':'XLE', 'weight': allo_ls[4]},
                    {'ticker':'BND', 'weight': allo_ls[5]},
                    {'ticker':'SCHP', 'weight': allo_ls[6]},
                    {'ticker':'VTEB', 'weight': allo_ls[7]},
                    {'ticker':'VIG', 'weight': allo_ls[8]},
                ]},
                {
                'info': [
                {'volatility': ret_vol_sr[1]},
                {'return': ret_vol_sr[0]},
                {'sharpe': ret_vol_sr[2]}
                ]}
            ]
        data.append(vol_allo_dict)


    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

def historical_chart(portfolio_makeup, volatility):
    data = []
    with open('data.json', 'r') as json_file:
        json_data = json.load(json_file)
    allo_dict = json_data[volatility]
    allos = allo_dict[0]['allocations']
    for i in allos:
        ticker = i['ticker']
        w = i['weight']
        df_stock_close[ticker] *= w

    df_stock_close['total'] = df_stock_close.sum(axis=1)
    df_stock_close['daily_return'] = df_stock_close['total'].pct_change(1)
    df_stock_close['total_return'] = df_stock_close['daily_return'].cumsum(axis=0)
    df_stock_close1 = df_stock_close.fillna(0)

    for index,row in df_stock_close1.iterrows():
        chart_dict = {
            'date': index,
            'daily_return': row['daily_return'],
            'total_return': row['total_return']
        }
        data.append(chart_dict)
    return data

# ret_vol_allos(0.9,1)
