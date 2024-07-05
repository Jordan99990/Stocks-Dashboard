import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_stock_linear_regression(data):
    close_prices = data['Close'].values.reshape(-1, 1)
    time = np.array(range(len(close_prices))).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(time, close_prices)
    
    future_time = np.array(range(len(close_prices), len(close_prices) + 90)).reshape(-1, 1)
    forecast = model.predict(future_time)
    
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=90)
    forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=['Forecasted Close'])
    forecast_df['Forecasted Close'] = forecast
    
    return forecast_df