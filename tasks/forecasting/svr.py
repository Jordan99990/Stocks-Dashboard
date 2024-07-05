import numpy as np
import pandas as pd
from sklearn.svm import SVR

def forecast_stock_svr(data):
    close_prices = data['Close'].values.reshape(-1, 1)
    time = np.array(range(len(close_prices))).reshape(-1, 1)
    
    model = SVR(kernel='rbf', C=1000.0, gamma=0.1)
    model.fit(time, close_prices.ravel())
    
    future_time = np.array(range(len(close_prices), len(close_prices) + 90)).reshape(-1, 1)
    forecast = model.predict(future_time)
    
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=90)
    forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=['Forecasted Close'])
    
    return forecast_df