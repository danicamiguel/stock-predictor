# Import flask.
from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
import base64
from io import BytesIO
from predictor import JSONToPandas, TickerDataFetcher, LinearClosePricePredictor
from datetime import date


app = Flask('stock-predictor')

@app.route('/<ticker>')
def get_ticker(ticker):
    ticker_fetcher = TickerDataFetcher(ticker)
    data = ticker_fetcher.get_ticker_data()
    table = JSONToPandas(data['Time Series (Daily)'])
    table.convert_to_pandas()
    predictor = LinearClosePricePredictor(table.df, False)
    predictor.predict(['1. open'], '4. close')
    
    open_price = float(request.args.get('open'))

    prediction = str(predictor.calculate_closing(open_price))

    table.df['date'] = pd.to_datetime(table.df.index)
    table.df['2. high'] = table.df['2. high'].astype(float)
    table.df['4. close'] = table.df['4. close'].astype(float)
    table.df['3. low'] = table.df['3. low'].astype(float)


    figure = Figure(figsize=(16,8))
    ax = figure.subplots()

    #ax.plot(table.df['date'][0:5], table.df['2. high'][0:5],linestyle='dashed', color='blue')
    ax.plot(table.df['date'][0:5], table.df['4. close'][0:5],color='green',linewidth=3)
    ax.plot(table.df['date'][0:5], predictor.predicted_train[0:5],color='orange',linewidth=3)
    ax.plot(table.df['date'][0:5], predictor.predicted_test[0:5],color='orange',linestyle='dashed',linewidth=3)
    #ax.plot(table.df['date'][0:5], table.df['3. low'][0:5],linestyle='dashed')
    ax.plot(date.today(), [float(prediction)], marker="o", markersize=20, color='green',)
    ax.text(date.today(), float(prediction), "Predicted price", horizontalalignment='center')
    ax.set_ylabel('Price (USD)', size=14, rotation = 0, ha='right', labelpad=10)
    ax.set_title('5-Day Performance',
            loc='left',
            size=18)
    buf = BytesIO()
    figure.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template(prediction=prediction, chart=f"<img src='data:image/png;base64,{data}'/>")
     

# Run our app!
app.run()

# Why? This tells us that we've made no errors
print('Got to the end of my file!')