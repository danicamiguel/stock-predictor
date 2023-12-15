
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class JSONToPandas:
        
        def __init__(self,data):
                self.data = data
                
        def convert_to_pandas(self):
                df = pd.DataFrame(self.data)
                self.df = df.T

        def get_closing_price(self):
                if not self.df.iloc[:1, 3][0]:        
                        return (f'Date: {self.df.index[1]}\n Closing Price: {self.df.iloc[:1, 3][1]}')
                else:
                        return (f'Date: {self.df.index[0]}\n Closing Price: {self.df.iloc[:1, 3][0]}')



class TickerDataFetcher:

        def __init__(self, ticker):
                self.ticker = ticker
                self.data = {}

        def get_ticker_data(self):
                url_realtime_stock = 'https://www.alphavantage.co/query'
                req = requests.get(url_realtime_stock,
                                params={'function': 'TIME_SERIES_DAILY',
                                        'symbol': self.ticker, 
                                        'apikey': 'WJPLYQLE8OIUN91A'})
                self.data = req.json()
                return self.data
                

class LinearClosePricePredictor:

        def __init__(self,df, transform=False):
                if transform:
                        self.df = df.T
                else:
                        self.df = df


        def predict(self, x_keys, y_key):
                X = self.df[x_keys]
                y = self.df[y_key]
                X_train, X_test, y_train, y_test = train_test_split(X,
                                                   y,
                                                   train_size=0.7,
                                                   random_state=42)
                lm = LinearRegression()
                lm.fit(X_train,y_train)
                y_train_pred = lm.predict(X_train)
                y_test_pred = lm.predict(X_test)   
                self.coefficients = lm.coef_
                self.intercept = lm.intercept_
        
        def calculate_closing(self, open):
                prediction = self.intercept + open*self.coefficients[0]
                return prediction
                
        




                
        

       
