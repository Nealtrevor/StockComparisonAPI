# -*- coding: utf-8 -*-
"""
Created on Sun May 29 14:28:33 2022

@author: nealt

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
stock_symbol_list = ["SPY", "MSFT", "TSLA","GOOGL"]

#set dates for different line charts
today = datetime.today().date()
one_year_date = (datetime.today().date()-timedelta(days=365))
one_wk_date = (datetime.today().date()-timedelta(days=7))
five_year_date = (datetime.today().date()-timedelta(days=1825))


#stock class that users the ticker from the flask form to pull data from the yahoo finance api, populate a dataframe, then plot the data in a browser dashboard using plotly.
class Stock:
    def stock_append(stock_ticker):
        stock_symbol_list.append(stock_ticker)
    
    def stock_data_yr():
        appended_data_yr = []
        for sym in stock_symbol_list:
        
          ticker_df = yf.Ticker(sym)
          
          #1yr
          ticker_close_df_yr = ticker_df.history(start=one_year_date, end=today)
          ticker_close_df_yr['Symbol'] = sym
          appended_data_yr.append(ticker_close_df_yr)
          
        
        #append to dfs
        #yr
        appended_data_yr = pd.concat(appended_data_yr)
        #appended_data.to_csv('loop_bigDF.csv')
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
    
    def stock_data_wk():
        appended_data_wk = []
        
        for sym in stock_symbol_list:
        
          ticker_df = yf.Ticker(sym)
          #1wk
          ticker_close_df_wk = ticker_df.history(start=one_wk_date, end=today)
          ticker_close_df_wk['Symbol'] = sym
          appended_data_wk.append(ticker_close_df_wk)
          
        
        #append to dfs
        #wk
        appended_data_wk = pd.concat(appended_data_wk)
        #appended_data.to_csv('loop_bigDF.csv')
        stock_df_wk = appended_data_wk
        stock_df_wk = stock_df_wk.reset_index()
           
        # plot looped data
        #plotly
        #wk
        all_stock_prices_wk = px.line(data_frame=(stock_df_wk),
                                    x='Date', y='Close', color='Symbol',
                                    title='Stock Price History (1 Week)'
                                    )
        graph_week = json.dumps(all_stock_prices_wk, cls=plotly.utils.PlotlyJSONEncoder)

        return graph_week;
    
    def stock_data_5yr():
        appended_data_five_yr = []
        for sym in stock_symbol_list:
          ticker_df = yf.Ticker(sym)
          #5yr
          ticker_close_df_5yr = ticker_df.history(start=five_year_date, end=today)
          ticker_close_df_5yr['Symbol'] = sym
          appended_data_five_yr.append(ticker_close_df_5yr)
        #append to dfs
        #5yr
        appended_data_five_yr = pd.concat(appended_data_five_yr)
        #appended_data.to_csv('loop_bigDF.csv')
        stock_df_5yr = appended_data_five_yr
        stock_df_5yr = stock_df_5yr.reset_index()
        
        # plot looped data
        #plotly
        #5yr
        all_stock_prices_5yr = px.line(data_frame=(stock_df_5yr),
                                    x='Date', y='Close', color='Symbol',
                                    title='Stock Price History (5 Years)'
                                    )
        graph_5yr = json.dumps(all_stock_prices_5yr, cls=plotly.utils.PlotlyJSONEncoder)
        return graph_5yr;
    
        
    def stock_analysis(stock_ticker):
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
        #appended_data.to_csv('loop_bigDF.csv')
        stock_df_yr = appended_data_yr
        stock_df_yr = stock_df_yr.reset_index()
        #wk
        appended_data_wk = pd.concat(appended_data_wk)
        #appended_data.to_csv('loop_bigDF.csv')
        stock_df_wk = appended_data_wk
        stock_df_wk = stock_df_wk.reset_index()
        #5yr
        appended_data_five_yr = pd.concat(appended_data_five_yr)
        #appended_data.to_csv('loop_bigDF.csv')
        stock_df_5yr = appended_data_five_yr
        stock_df_5yr = stock_df_5yr.reset_index()
        
        # plot looped data
        #plotly
        #1
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
        
        
   
