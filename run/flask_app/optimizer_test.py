#!/usr/bin/env python

import json, requests
import os
import numpy as np
import pandas as pd

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

print(random_weights())
