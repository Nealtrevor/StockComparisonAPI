"""
Neal Trevor

ICT 4370-1

05/29/2022

PORTFOLIO PROGRAMMING ASSIGNMENT - IMPROVING THE STOCK PROBLEM WITH ADDITIONAL FUNCTIONALITY:
Python Files:
App.py:  the main file that executes code.  It starts the flask app server and imports the required functions from stocks.py
Stocks.py:  This file holds the stock class and contains all of the functions to import from the yahoo finance api, manipulate in pandas, then plot with plotly.

Templates:
stockhistory.html, index.html, clear.html :  These files provides a basic browser UI that allows the user to add stocks to the comparison.  It displays 3 line charts that make up one dashboard.  1 week, 1 year and 5 year stock history comparison.  
It also allows the user to clear the list of stocks and only compare one stock with the SPY.

Deployment files:
Procfile:  This file is required for deployment on heroku. it tells heroku to use the gunicorn server, which is a multithreaded flask app server. (web: gunicorn app:app)
requirements.txt :  This file tells heroku which libraries need to be installed in the cloud environment for the python code to run.  It does all the pip installs during the deployment.
gitignore: created when uploaded to github.  Can be used to hide api keys.

Deployed online at : https://stock-comparison-tool-yahoofin.herokuapp.com/ (it may take a second to load the first time because it is a free server that goes idle when not in use.)

Github files: https://github.com/Nealtrevor/StockComparisonAPI
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
plt.style.use('seaborn')
import yfinance as yf
import flask
from flask import Flask, render_template # for web app
from flask import Response
import io
import plotly
import plotly.express as px
import json # for graph plotting in website

#populate a few stocks for comparison.  can be cleared in the browser with the Clear button
try:
  stock_symbol_list = ["SPY", "MSFT", "TSLA","GOOGL"]
except Exception as e:
            print("Error. Exception found: "+str(e))
#set dates for different line charts
try:
  today = datetime.today().date()
  one_year_date = (datetime.today().date()-timedelta(days=365))
  one_wk_date = (datetime.today().date()-timedelta(days=7))
  five_year_date = (datetime.today().date()-timedelta(days=1825))
except Exception as e:
            print("Error. Exception found: "+str(e))

#stock class that users the ticker from the flask form to pull data from the yahoo finance api, populate a dataframe, then plot the data in a browser dashboard using plotly.
class Stock:
    def stock_append(stock_ticker):
        try:
          stock_symbol_list.append(stock_ticker)
        except Exception as e:
            print("Error. Exception found: "+str(e))
    
    def stock_data_yr():
        try:
          appended_data_yr = []
          for sym in stock_symbol_list:
          
            ticker_df = yf.Ticker(sym)
            
            #1yr
            ticker_close_df_yr = ticker_df.history(start=one_year_date, end=today)
            ticker_close_df_yr['Symbol'] = sym
            appended_data_yr.append(ticker_close_df_yr)
            
          #append to dfs
          appended_data_yr = pd.concat(appended_data_yr)
          stock_df_yr = appended_data_yr
          stock_df_yr = stock_df_yr.reset_index()

          # plot looped data
          #plotly
          #1
          all_stock_prices_yr = px.line(data_frame=(stock_df_yr),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (1 Year)'
                                      )
          graph_year = json.dumps(all_stock_prices_yr, cls=plotly.utils.PlotlyJSONEncoder)

          return graph_year;
        except Exception as e:
            print("Error. Exception found: "+str(e))

    def stock_data_wk():
        try:
          appended_data_wk = []
          
          for sym in stock_symbol_list:
          
            ticker_df = yf.Ticker(sym)
            #1wk
            ticker_close_df_wk = ticker_df.history(start=one_wk_date, end=today)
            ticker_close_df_wk['Symbol'] = sym
            appended_data_wk.append(ticker_close_df_wk)
            
          
          #append to dfs
          appended_data_wk = pd.concat(appended_data_wk)
          stock_df_wk = appended_data_wk
          stock_df_wk = stock_df_wk.reset_index()
            
          # plot looped data
          all_stock_prices_wk = px.line(data_frame=(stock_df_wk),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (1 Week)'
                                      )
          graph_week = json.dumps(all_stock_prices_wk, cls=plotly.utils.PlotlyJSONEncoder)

          return graph_week;
        except Exception as e:
            print("Error. Exception found: "+str(e))

    def stock_data_5yr():
        try:
          appended_data_five_yr = []
          for sym in stock_symbol_list:
            ticker_df = yf.Ticker(sym)
            #5yr
            ticker_close_df_5yr = ticker_df.history(start=five_year_date, end=today)
            ticker_close_df_5yr['Symbol'] = sym
            appended_data_five_yr.append(ticker_close_df_5yr)
          
          #append to dfs
          appended_data_five_yr = pd.concat(appended_data_five_yr)
          stock_df_5yr = appended_data_five_yr
          stock_df_5yr = stock_df_5yr.reset_index()
          
          # plot looped data
          all_stock_prices_5yr = px.line(data_frame=(stock_df_5yr),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (5 Years)'
                                      )
          graph_5yr = json.dumps(all_stock_prices_5yr, cls=plotly.utils.PlotlyJSONEncoder)
          return graph_5yr;
        except Exception as e:
            print("Error. Exception found: "+str(e))
        
    def stock_analysis(stock_ticker):
        try:
          stock_symbol_list.append(stock_ticker)

          ################################################
          #LOOP through list of stocks and append to DF
          ################################################
      
          appended_data_yr = []
          appended_data_wk = []
          appended_data_five_yr = []
          for sym in stock_symbol_list:
          
            ticker_df = yf.Ticker(sym)
            
            #1yr
            ticker_close_df_yr = ticker_df.history(start=one_year_date, end=today)
            ticker_close_df_yr['Symbol'] = sym
            appended_data_yr.append(ticker_close_df_yr)
            #1wk
            ticker_close_df_wk = ticker_df.history(start=one_wk_date, end=today)
            ticker_close_df_wk['Symbol'] = sym
            appended_data_wk.append(ticker_close_df_wk)
            
            #5yr
            ticker_close_df_5yr = ticker_df.history(start=five_year_date, end=today)
            ticker_close_df_5yr['Symbol'] = sym
            appended_data_five_yr.append(ticker_close_df_5yr)
          
          #append to dfs
          #yr
          appended_data_yr = pd.concat(appended_data_yr)
          stock_df_yr = appended_data_yr
          stock_df_yr = stock_df_yr.reset_index()
          #wk
          appended_data_wk = pd.concat(appended_data_wk)
          stock_df_wk = appended_data_wk
          stock_df_wk = stock_df_wk.reset_index()
          #5yr
          appended_data_five_yr = pd.concat(appended_data_five_yr)
          stock_df_5yr = appended_data_five_yr
          stock_df_5yr = stock_df_5yr.reset_index()
          
          # plot looped data
          all_stock_prices_yr = px.line(data_frame=(stock_df_yr),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (1 Year)'
                                      )
          graph_year = json.dumps(all_stock_prices_yr, cls=plotly.utils.PlotlyJSONEncoder)
          
          #wk
          all_stock_prices_wk = px.line(data_frame=(stock_df_wk),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (1 Week)'
                                      )
          graph_week = json.dumps(all_stock_prices_wk, cls=plotly.utils.PlotlyJSONEncoder)
          #5yr
          all_stock_prices_5yr = px.line(data_frame=(stock_df_5yr),
                                      x='Date', y='Close', color='Symbol',
                                      title='Stock Price History (5 Years)'
                                      )
          graph_5yr = json.dumps(all_stock_prices_5yr, cls=plotly.utils.PlotlyJSONEncoder)
        
          return [graph_year, graph_week,graph_5yr];
        except Exception as e:
            print("Error. Exception found: "+str(e))
        
        
   
