import pandas as pd
import statsmodels.api as sm

def forecast_stock_sarimax(data): 
    close_prices = data['Close']
    
    model = sm.tsa.SARIMAX(close_prices, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12), exog=None)
    result = model.fit()
    
    forecast = result.forecast(steps=90)
    
    last_date = close_prices.index[-1]
    forecast_dates = pd.date_range(start=last_date, periods=90)
    forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=['Forecasted Close'])
    forecast_df['Forecasted Close'] = forecast.values
    
    return forecast_df