# stock-predictor

1. Problem statement:
Someone wants to find the right time to buy or sell stock in the future. This person would like to know if today or tomorrow would either
be the best choice to buy or sell their desired stock.

2. Summary of solution:
This web server will allow someone to input an opening price for a stock and an output of a predicted closing price will help them decide whether they want to buy or sell. They can input an price at any time. For example, the opening price of the current date or the closing the price of the previous day to get a prediction.

3. Technical solution:
I used the AlphaVintage API, specifically the Time Series Daily data to get historical stock prices. Using this data, I converted it into 
a pandas dataframe in order to use the scikit-learn machine learning library. With this library, I split the Time Series Daily data into train and test sets with a training size of 70% and random selection of 42. I mainly leveraged linear regression to train and test the data and get the coefficients of the opening, high, low, and closing prices and the volume. I used the linear regression formula to add the y-intercept and the product of opening price input and its coefficient. 
I also added the mean squared errors for the train and test predicted closing price to show how good or bad the model is to help the use determine how they will use the predicted closing price to make a decision.

4. File summaries:
The predictor file has three classes. 
JSONToPandas convets the AlphaVintage API Time Series Daily data from json to pandas and transform the columns and rows to have the dates as rows and the different prices as columns.
TickerDataFetcher calls the AlphaVintage API and gets the Times Series Daily data.
LinearClosePricePredictor uses the sci-kit machine learning libary to train and test the stock prices and leverage linear regression to
predict the closing price.
The app file runs a flask server.
The use will have to input the stock ticker and input an opening price.
It creates a graph that shows a trend of 5-day stock performance with the actual closing prices, the train and testing prices, and the plots the predicted closing price.
It shows whether the use should buy or sell the stock. If predicted closing price is higher than the opening price, the user should sell the stock. However, if the predicted closing price is lower than opening price, the user should buy the stock.
It also shows where the model is right or wrong based on the actual opening and closing prices of the current day to help user gage how good and bad the model is that they are using.
Index file is written in html and shows the predicted closing price, the mean squared errors, and the graph.

5. Please reach out to danicavmiguel@gmail.com for any questions!