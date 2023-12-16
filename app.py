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


# Create a Flask object
app = Flask('stock-predictor')

# add stock ticker
@app.route('/<ticker>')
def get_ticker(ticker):
    ticker_fetcher = TickerDataFetcher(ticker)
    data = ticker_fetcher.get_ticker_data()
    table = JSONToPandas(data['Time Series (Daily)'])
    table.convert_to_pandas()
    predictor = LinearClosePricePredictor(table.df, False)
    predictor.predict(['1. open'], '4. close')
    
    # get opening price input
    # convert to float
    open_price = float(request.args.get('open'))

    # predicted closing price output
    prediction = str(predictor.calculate_closing(open_price))

    # convert date to pandas datetime
    # convert close column from dataframe to float
    table.df['date'] = pd.to_datetime(table.df.index)
    table.df['4. close'] = table.df['4. close'].astype(float)
 

    # creating graph to show actual closing price
    # show training closing price
    # show testing closing price
    figure = Figure(figsize=(16,8))
    ax = figure.subplots()
    ax.plot(table.df['date'][0:5], table.df['4. close'][0:5],color='green',linewidth=3,label='Actual Closing Price')
    ax.plot(table.df['date'][0:5], predictor.predicted_train[0:5],color='orange',linewidth=3,label='Train Closing Price')
    ax.plot(table.df['date'][0:5], predictor.predicted_test[0:5],color='orange',linestyle='dashed',linewidth=3,label='Test Closing Price')
    ax.plot(date.today(), [float(prediction)], marker="o", markersize=20, color='green',)
    ax.text(date.today(), float(prediction), "Predicted price", horizontalalignment='center')
    ax.set_ylabel('Price (USD)', size=14, rotation = 0, ha='right', labelpad=10)
    ax.set_title('5-Day Performance',
            loc='left',
            size=18)
    ax.legend(loc='upper left')
    buf = BytesIO()
    figure.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    # if predicted opening price is higher than actual opening price sell stock else buy
    buy = "buy"
    if prediction < table.df['1. open'][0]:
        buy = "sell"
    
    # check if model is accurate
    wrong = "model is wrong"
    if ((float(table.df['1. open'][0]) < float(table.df['4. close'][0])) and buy == "buy") or ((float(table.df['1. open'][0]) > float(table.df['4. close'][0])) and buy == "sell"):
        wrong = "model is right"
        
    
    # produce graph image and predicted, training, and testing closing price
    return render_template("index.html", prediction=prediction, chart=f"data:image/png;base64,{data}", mse_train=predictor.mse, mse_test=predictor.msetest, buy=buy.upper(), wrong=wrong.upper())
     

# Run our app!
app.run()
