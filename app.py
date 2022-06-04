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

#########################
# IMPORTS
#########################
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
# Deployed online at : https://stock-comparison-tool-yahoofin.herokuapp.com/
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
    return render_template('stockhistory.html',graph_year=graph_year,graph_week=graph_week,graph_5yr=graph_5yr)

    

@app.route('/clear', methods = ['POST'])
def clear():

    stock_symbol_list.clear()
    stock_symbol_list.append("SPY")
    return render_template('clear.html')
    
#run flask server
if __name__ == '__main__':
    app.run()