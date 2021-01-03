from flask import Flask, render_template, url_for, redirect, request
import requests
import json 
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
# select a palette
from bokeh.palettes import Dark2_5 as palette
# itertools handles the cycling
import itertools 
#app
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
#app.config['SECRET_KEY'] = '0000'
def index():

    if request.method == 'GET':
        return render_template('app_index.html')
    else:
        # request was a POST
        features= request.form.getlist('features')
        month = int(request.form['month'])
        # f = open('%s_%s.txt'%(features,month),'w')
        # f.write('Stock: %s\n'%(features))
        # f.write('Month: %s\n\n'%(month))
        # f.close()
        plots = [ ]
        plots.append(make_plot(features, month))
        return render_template('dashboard.html', plots=plots)
        #*********************************************************************************************
def make_plot(userfeatures, usermonth):
        key1 = config.key1
        ticker = str(request.form['ticker'])
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key1)
        response = requests.get(url)
        db=response.json()
        df = pd.json_normalize(db)
        df.reset_index(inplace=True)
        df=df.melt()
        df.columns
        df.dropna(inplace = True) 
        #new data frame with split value columns 
        new = df["variable"].str.split(".", n = 0, expand = True) 
        # making separate first name column from new data frame 
        df["Date"]= new[0] 
        # making separate last name column from new data frame 
        df["Type"]= new[1] 
        df["Type2"]= new[3]
        # Dropping old Name columns 
        df.drop(columns =["variable"], inplace = True) 
        df.style.set_caption("BRK.B")
        df.drop(columns =['Date'], inplace = True)
        df = df[6:] #get rid of first 5
        df=df.pivot(index='Type', columns='Type2')['value']
        df = df.rename_axis("Date", axis="columns")
        df.columns = ['adjusted close', 'close', 'dividend amount', 'high','low','open', 'split coefficient', 'volume']

        #us = user input 
        # a = request.form.getlist('features')
        # usmonth = int(request.form['month'])
        df.index = pd.to_datetime(df.index)
        usdf=df[df.index.month == usermonth]
        #output_file('Day10.html')
        usdf.index = pd.to_datetime(usdf.index)
        usdf.index.name = 'Date'
        usdf.sort_index(inplace=True)
        source = ColumnDataSource(usdf)
        colors = itertools.cycle(palette)    
        p = figure(title=str(ticker), x_axis_type='datetime', plot_width=800, plot_height=350)
      
        for element in userfeatures:
            p.line('Date',element, source=source,legend_label=element,line_color=next(colors))

        return show(p)


if  __name__ == '__main__' :
    app.run( port=33507)

