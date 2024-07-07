import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def forecast_stock_random_forest(data):
    features = ['Open', 'High', 'Low', 'Close', 'Volume']
    X = data[features]
    X_train = X[:int(len(data) - 1)]
    y_train = data[['Open', 'High', 'Low', 'Close', 'Volume']][1:]
    
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    
    last_known_features = X.iloc[-1].values.reshape(1, -1)
    
    predictions = []
    
    for _ in range(90):
        next_day_prediction = model.predict(last_known_features)
        predictions.append(next_day_prediction[0])
        
        last_known_features = np.array(next_day_prediction).reshape(1, -1)
    
    predictions_df = pd.DataFrame(predictions, columns=features)
    
    last_date = data.index.max()
    future_dates = pd.date_range(start=last_date, periods=90)
    predictions_df.index = future_dates
    predictions_df.rename(columns={'Close': 'Forecasted Close'}, inplace=True)
    predictions_df.drop(columns=['Open', 'High', 'Low', 'Volume'], inplace=True)
    
    return predictions_df