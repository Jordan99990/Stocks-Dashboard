import pandas as pd
import statsmodels.api as sm

def forecast_stock_arima(data): 
    close_prices = data['Close']
    
    model = sm.tsa.ARIMA(close_prices, order=(1, 1, 1))
    result = model.fit()
    
    forecast = result.forecast(steps=90)
    
    last_date = close_prices.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=90)
    forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=['Forecasted Close'])
    forecast_df['Forecasted Close'] = forecast.values
    
    print(forecast_df)
    return forecast_df