# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:27:26 2021

@author: Diego Alvarez diego.alvarez@colorado.edu
"""

import itertools
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as web

#let's start by getting dates for our dataframe
end = dt.date.today()
start = dt.date(end.year - 10, end.month, end.day)

#we'll start with the S&P 500 which use the ticker ^GSPC
spx = yf.download("^GSPC", start, end)
spx[["Open", "Close"]].tail(10).plot(figsize = (24,10))
plt.title("Last 10 trading days of S&P 500 daily open and close")
plt.grid()
plt.show()

spx[["High", "Low"]].tail(10).plot(figsize = (24,10))
plt.title("Last 10 trading days of S&O 500 daily high and low")
plt.grid()
plt.show()

yf.download("aapl", start, end)[["Close", "Adj Close"]].plot(figsize = (24,10))
plt.title("Last 10 Years of Apple Stock daily close and adjusted close")
plt.grid()
plt.show()

#let's work with pandas_datareader this allows us to pull form other sources such as IMF. OECD, and FRED
#let's get the CPI rate from FRED

cpi = web.DataReader("CPIAUCSL", "fred", start, end)
cpi.plot(figsize = (24,10))
plt.title("Consumer Price Index for All Urban Consumers: All Items in US City Average last 10 years")
plt.grid()
plt.show()

#this function will return a dataframe of all of the companies that are listed in colorado
def colorado_cut():

    read_obj = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = read_obj[0]
    
    city = []
    state = []
    
    for i in df["Headquarters Location"]:
        
        i = i.split(",")
        city.append(i[0])
        state.append(i[1])
        
    data_dict = {"Symbol": df["Symbol"], "City": city, "State": state}
    output_df = pd.DataFrame(data = data_dict)
    
    for index, i in enumerate(output_df["State"]):
        
        if i.replace(" ", "") != "Colorado":
            output_df = output_df.drop(index)
            
    return output_df

#this dataframe will be all of colorado companies
df = colorado_cut()

#now we can get all of the stocks by passing the values as list
prices = yf.download(df["Symbol"].to_list(), start, end)["Adj Close"]

#save the dataframe for future
prices.to_csv("colorado_companies.csv")

#let's simulate a portfolio in this case we going to evenly invest the money

#start by making an allocation array
allocation_array = [1 / len(prices.columns) for i in range(len(prices.columns))]

#then multiply the returns by the allocation array
portfolio_return = prices.pct_change().dropna() * allocation_array

#then get the total return by summing the values
portfolio_return["total_return"] = portfolio_return.sum(axis = 1)

#let's plot it
plt.figure(figsize = (24,10))
plt.plot((1 + portfolio_return["total_return"]).cumprod() * 100)
plt.title("Portfolio Cumulative Return of evenly weighted portfolio over last 10 years")
plt.ylabel("Portfolio Return (%)")
plt.grid()
plt.show()

#let's keep track of the portfolio value 

#instead of multiplying the returns by the allocation size we'll multiply the stock by the number of shares
#to find the number of shares we need to find how many shares we are going to buy

#assume a portfolio of $100,000
starting_capital = 100000
share_array = []

#we want to loop through each column get the amount of starting cash and divded by the first price
for i in prices.columns:
    share_array.append((starting_capital / len(prices.columns)) / prices[i][0])
    
#let's multiply the share price by the number of shares and then get the total value
portfolio_value = prices * share_array
portfolio_value["sum"] = portfolio_value.sum(axis = 1)

#let's plot it
portfolio_value["sum"].plot(figsize = (24,10))
plt.title("Last 10 Years portfolio value evenly weighted portfolio")
plt.grid()
plt.ylabel("Portfolio Value ($)")
plt.show()

#now let's compare results we want the final values to be close to eachother
print("final portfolio value:", portfolio_value["sum"][len(portfolio_value) - 1])
print("final return value:", (portfolio_return["total_return"] + 1).cumprod()[len(portfolio_return) - 1] * 100000)

#you can see that we have a problem becuase they are off, they are off by too much

#we can fix that by using the close price
prices = yf.download(df["Symbol"].to_list(), start, end)["Close"]

#now do the same returns method using the close price
portfolio_return = prices.pct_change().dropna() * allocation_array
portfolio_return["total_return"] = portfolio_return.sum(axis = 1)
print((portfolio_return["total_return"] + 1).cumprod()[len(portfolio_return) - 1] * 100000)

#so you may ask yourself where do we get the portfolio with $323,000 that comes from reinvesting the dividends
#what we did was get the initial value of the stock on the start day and kept it but as we reinvest the dividends
#the number of shares will change as we reinvest the dividends therefore you have to update the portfolio 
#in real life you wouldn't always reinvest the dividends because it would lead to fractional shares
#this means after each transaction period you need to change the number of shares

#let's look at the distribution of the portfolio
plt.figure(figsize = (24,10))
portfolio_value["sum"].pct_change().plot(kind = "hist", bins = 100)
plt.title("Last 10 Years Portfolio Value evenly weighted portfolio returns")
plt.grid()
plt.show()

#something that we are interested in is the underlying performance of each stock
#we first need the returns of the stock
prices_returns = prices.pct_change().dropna()

#now we are going to compare all of the stocks agianst themselves to do that we'll use the itertools
combinations = list(itertools.combinations(prices_returns.columns, 2))

row_count = 5
col_count = 3
fig, axes = plt.subplots(row_count, col_count, figsize = (30,30))

for i in range(5):
    for j in range(3):
        axes[i,j].scatter(prices_returns[combinations[i+j][0]], prices_returns[combinations[i+j][1]])
        axes[i,j].set_title("{} vs. {}".format(combinations[i+j][0], combinations[i+j][1]))
        axes[i,j].grid()
        
plt.tight_layout()
plt.show()





