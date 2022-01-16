#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 17:17:03 2022

@author: mevlut
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy import optimize

def callPrice(sigma, S, K, r, t):
    """
    

    Parameters
    ----------
    sigma : float
        Implied Volatility.
    S : float
        Stock Price.
    K : float
        Strike Price.
    r : float
        Interest rate.
    t : float
        Time to maturity.

    Returns
    -------
    C : float
        Black-Scholes Call Price.

    """
    
    d1 = 1 / (sigma * np.sqrt(t)) * (np.log(S/K) + (r + sigma**2/2) * t)
    d2 = d1 - sigma * np.sqrt(t)
    C = norm.cdf(d1) * S - norm.cdf(d2) * K * np.exp(-r * t)
    
    return C


def FitVol(sigma, S, K, r, t, p):
    '''    


    Parameters
    ----------
    sigma : float
        first guess.
    S : float
        Stock Price.
    K : float
        Strike Price.
    r : float
        Interest rate.
    t : float
        Time to maturity.
    p : float
        Market Price.

    Returns
    fit : float
    -------
        Market Implied Volatility.


    '''
    fit = callPrice(sigma, S, K, r, t) - p
    
    return fit
