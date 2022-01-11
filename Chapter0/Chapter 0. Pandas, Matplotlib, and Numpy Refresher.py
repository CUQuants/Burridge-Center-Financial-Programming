# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 21:24:20 2021

@author: Diego Alvarez diego.alvarez@colorado.edu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try: 
    #original code but there may be some problems with the urlopen
    read_obj = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    df = read_obj[0]

except: 
    #in the event that there is a problem wit urlopen use this code
    df = pd.read_csv("sp500_companies.csv")


#reference by column
symbols = df["Symbol"]

#reference by value
symbols = df.Symbol

#reference by column value
symbols = df[df.columns[0]]

#generate a new dataframe by passing column names
new_df = df[["Symbol", "Security", "SEC filings"]]

#generate a new dataframe by passing columns
new_df = df[df.columns[0:3]]

#generate new dataframe by passing dictionary
data_dict = {"Symbol": df["Symbol"], "Security": df["Security"], "SEC filings": df["SEC filings"]}
new_df = pd.DataFrame(data = data_dict)

#let's get all of the companies that are based out of California, we'll first start by referencing the california if we look at the data we see that the location is city and state, we'll have to loop through each value

#create to lists 
city = []
state = []

#loop through all of the values in specified column
for i in df["Headquarters Location"]:
    
    i = i.split(",")
    city.append(i[0])
    state.append(i[1])
    
#put all of that data into a new dataframe
data_dict = {"Symbol": df["Symbol"], "City": city, "State": state}
new_df = pd.DataFrame(data = data_dict)

#now let's loop through each value in the state column use negated logic to acces our values we have to keep track of the row index so we'll use the enumearte function
for index, i in enumerate(new_df["State"]):
    
    if i.replace(" ", "") != "California":
        new_df = new_df.drop(index)
        
#let's say we wanted to pass the information to a new dataframe first we have to recreate the original new_df because we "edited" it in the last line
new_df = pd.DataFrame(data = data_dict)
california_df = pd.DataFrame(columns = new_df.columns)

for index, i in enumerate(new_df["State"]):
    if i.replace(" ", "") == "California":
        california_df = california_df.append(new_df.iloc[index])
        
#in this case let's read the stocks from the S&P 500 companies that are based in Colorado
prices = pd.read_csv("colorado_companies.csv", index_col = 0)

#slice the dataframe down so that it is easier to make the plots
prices = prices["2019-01-01":"2020-01-01"]

#we are going to use the prices.describe() to model the companies together
print(prices.describe())

#now we want to plot these stock prices
prices.plot(figsize = (24,10))
plt.title("S&P 500 Companies headquartered in Colorado (Daily Adjusted Close) 2019 - 2020")
plt.grid()
plt.show()

#lets individually plot them
prices.plot(subplots = True, layout = (2,4), sharex = False, figsize = (24,12))
plt.tight_layout()

#lets look at calculating the returns
prices_returns = prices.pct_change().dropna()

#let's plot them
prices_returns.plot(figsize = (24,10))
plt.grid()
plt.title("S&P 500 Companies headquartered in Colorado (Daily Adjusted Close Returns) 2019 - 2020")
plt.show()

#lets individually plot them
prices_returns.plot(subplots = True, layout = (len(prices_returns.columns), 1), sharex = False, figsize = (10,12))
plt.tight_layout()

#in this case we aren't really interested in the time series of the returns we are intersted in the returns distribution
prices_returns.plot(kind = "hist", bins = 100, subplots = True, layout = (2,4), sharex = False, figsize = (24,10))
plt.tight_layout()
plt.show()

#this isn't really that interesting
prices_returns[prices_returns.columns[0]].plot(figsize = (24,10))
plt.title(prices_returns.columns[0] + " returns")
plt.ylabel("Percentage (%)")
plt.grid()
plt.show()

#instead we want the cumulative returns
prices_returns[prices_returns.columns[0]].cumsum().plot(figsize = (24,10))
plt.title(prices_returns.columns[0] + " Daily Adjusted Close Returns 2019 - 2020")
plt.ylabel("Percentage (%)")
plt.grid()
plt.show()

#we can compare the returns of all of our securities
prices_returns.cumsum().plot(figsize = (24,10))
plt.title("S&P 500 Companies headquartered in Colorado (Daily Adjusted Closed Returns) 2019 - 2020")
plt.ylabel("Percentage (%)")
plt.grid()
plt.show()

#keep in mind that this graph always starts at 0 and really what it is showing is who performanced the most let's take another example by slicing our dataframe
prices_returns_sliced = prices_returns[prices_returns.columns][:int(len(prices_returns) / 2)]
print("prices returns shape:", prices_returns.shape)
print("prices returns sliced shape:", prices_returns_sliced.shape)

#you can see that the sliced graph looks completely different 
prices_returns_sliced.cumsum().plot(figsize = (24,10))
plt.title("S&P 500 Companies headquartered in Colorado (Daily Adjusted Closed Returns)" + " " + prices_returns_sliced.index[0] + " - " + prices_returns_sliced.index[len(prices_returns_sliced) - 1])
plt.ylabel("Percentage (%)")
plt.grid()
plt.show()

