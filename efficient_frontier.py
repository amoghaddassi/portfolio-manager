import quandl
quandl.ApiConfig.api_key = "z-RmrRydTPQ5sWuSzUL3"
import pandas as pd
import numpy as np
#switches
NUM_PORTFOLIOS = 10000
START_DATE = "2016-1-1"
END_DATE = "2016-12-30"
tickers = ["AAPL", "TSLA"]

#gets the data
data = quandl.get_table("WIKI/PRICES", ticker=tickers, 
						qopts = {"columns":["date", "ticker", "adj_close"]},
						date = {"gte": START_DATE, "lte": END_DATE})
#cleans things up
data = data.set_index("date")
data = data.pivot(columns="ticker")
#compute some stats to use in the algo
returns_daily = data.pct_change()
returns_annual = returns_daily.mean() * 252
#compute covariance across columns
cov_daily = returns_daily.cov()
cov_annual = cov_daily * 252
#code to run the simulated portfolios
sample_returns = []
sample_var = []
sample_weights = []

num_assets = len(tickers)

for i in range(NUM_PORTFOLIOS):
	#initialize and normalize random weights vector
	weights = np.random.random(num_assets)
	weights /= sum(weights)
	sample_weights.append(weights)
	returns = np.dot(weights, returns_annual)
	sample_returns.append(returns)
	var = np.dot(weights.T, np.dot(cov_annual, weights))
	sample_var.append(var)

import matplotlib.pyplot as plt
#plot the frontier
plt.scatter(sample_var, sample_returns)
plt.xlabel("Portfolio variance")
plt.ylabel("Portfolio return")
plt.show()
	
	
