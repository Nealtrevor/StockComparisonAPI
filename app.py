# -*- coding: utf-8 -*-
"""
Created on Sun May 29 11:23:24 2022

@author: nealt
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
plt.style.use('seaborn')
#import seaborn as sns
import yfinance as yf
import flask
from flask import Flask, render_template # for web app
from flask import Response

import io
#import random
import plotly
import plotly.express as px
import json # for graph plotting in website
from stocks import *




####################
# RUN FLASK APP ON http://127.0.0.1:5000/  
####################

app = Flask(__name__)

@app.route('/' )
def run_app():
    return render_template('index.html')


    
@app.route('/stockhistory', methods = ['POST'])
def stockhistory():
    
    ticker = flask.request.form['ticker'].upper()
    #Stock.stock_analysis(ticker)
    Stock.stock_append(ticker)
    graph_year=Stock.stock_data_yr()
    graph_week=Stock.stock_data_wk()
    graph_5yr=Stock.stock_data_5yr()
    return render_template('stockhistory.html',graph_year=graph_year,graph_week=graph_week,graph_5yr=graph_5yr)#,table=parsed_and_scored_news.to_html(classes='data'))

    

@app.route('/clear', methods = ['POST'])
def clear():

    stock_symbol_list.clear()
    stock_symbol_list.append("SPY")
    return render_template('clear.html')
    
#run flask server
if __name__ == '__main__':
    app.run()