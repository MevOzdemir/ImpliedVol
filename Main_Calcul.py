#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 21:09:09 2022

@author: mevlut
"""

''' ---------------------- Import lib ----------------------'''

import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy import optimize

from BS_Price_Fit import callPrice
from BS_Price_Fit import FitVol

''' ---------------------- Reading the file ----------------------'''


df = pd.read_excel('Vol_Fit.xlsx',sheet_name='vol',\
                   usecols='A:M',skiprows=9,nrows=21,index_col=0)

''' --------------------------- Calcul ---------------------------'''


volGuess = 0.2

S = np.array([100] * (len(df.index) * len(df.columns)))
r = np.array([0.04] * (len(df.index) * len(df.columns)))
t = np.array([df.columns] * len(df.index)).flatten() / 365
K = np.array([df.index]).flatten()
K = (K[:, None] * np.ones((len(df.columns),))[None,: ]).flatten()
p = df.values.flatten()

implied_vol = list()

for i in range (len(df.index)*len(df.columns)):
    sol = optimize.root(FitVol, volGuess, args=(S[i],K[i],r[i],t[i],p[i]), method='hybr')
    implied_vol.append(sol.x[0])

implied_vol = np.array(implied_vol).reshape(len(df.index),len(df.columns))
df_implied_vol = pd.DataFrame(implied_vol,index=df.index,columns=df.columns)


''' ------------------------- Plotting -------------------------'''


strike = K.reshape(len(df.index),len(df.columns))
ttm = t.reshape(len(df.index),len(df.columns))*365
iv = np.array(implied_vol)*100

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize=(10,6))
ax = fig.gca(projection='3d')
surf = ax.plot_surface(strike, ttm, iv, rstride=2, cstride=2, cmap=plt.cm.coolwarm,linewidth=0.5)



ax.set_xlabel('$Strike$')
ax.set_ylabel('$Time To Maturity$')
ax.set_zlabel(r'$Implied Vol$')
