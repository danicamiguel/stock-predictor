
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

# class that convert data in json format to pandas dataframe
class JSONToPandas:
        
        def __init__(self,data):
                self.data = data
                
        def convert_to_pandas(self):
                df = pd.DataFrame(self.data)
                self.df = df.T


# class that calls API and store data
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
                
# class that trains and tests data to predict stock price using linear regression
# gets coefficients and y-intercept for opening price
# finds mean squared erroers for training and testing
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
                self.predicted_train = lm.predict(X_train)
                self.predicted_test = lm.predict(X_test)   
                self.coefficients = lm.coef_
                self.intercept = lm.intercept_
                self.mse = metrics.mean_squared_error(y_train, self.predicted_train)
                self.msetest = metrics.mean_squared_error(y_test, self.predicted_test)
        
        # using linear regression formula
        # opening price is the independent variable
        # predicted closing variable is the dependant variable
        # plug in y-intercept and coefficients into formula
        def calculate_closing(self, open):
                prediction = self.intercept + open*self.coefficients[0]
                return prediction
                
        




                
        

       
