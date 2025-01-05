import numpy as np 
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

model = load_model('Stock Predictions Model.keras')

st.header('Stock Market Predictor')

stock = st.text_input('Enter Stock Symbol', 'GOOG')

start = '2018-01-01'
# Get the current date dynamically
end = datetime.today().strftime('%Y-%m-%d')  # Format today's date as 'YYYY-MM-DD'

data = yf.download(stock, start, end)

st.subheader('Stock Data')
st.write(data)

data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range= (0,1))

past_100_days = data_train.tail(100)
data_test = pd.concat([past_100_days, data_test], ignore_index=True)
data_test_scale = scaler.fit_transform(data_test)

st.subheader('Price vs Moving Average 50')
ma_50_days = data.Close.rolling(50).mean()
fig1 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r', label= 'MA50')
plt.plot(data.Close, 'g', label= 'ORIGINAL')
plt.legend()
plt.show()
st.pyplot(fig1)

st.subheader('Price vs Moving Average 50 vs Moving Average 100')
ma_100_days = data.Close.rolling(100).mean()
fig2 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r', label='MA50')
plt.plot(ma_100_days, 'b', label='MA100')
plt.plot(data.Close, 'g', label='ORIGINAL')
plt.legend()
plt.show()
st.pyplot(fig2)

st.subheader('Price vs Moving Average 100 vs Moving Average 200')
ma_200_days = data.Close.rolling(200).mean()
fig3 = plt.figure(figsize=(8,6))
plt.plot(ma_100_days, 'r', label= 'MA100')
plt.plot(ma_200_days, 'b', label= 'MA200')
plt.plot(data.Close, 'g', label= 'ORIGINAL')
plt.legend()
plt.show()
st.pyplot(fig3)

x = []
y = []
for i in range(100, data_test_scale.shape[0]):
    x.append(data_test_scale[i - 100:i])
    y.append(data_test_scale[i, 0])
x, y = np.array(x), np.array(y)

predict = model.predict(x)

scale = 1/scaler.scale_

predict = predict * scale
y = y * scale

st.subheader('Original Price vs Predicted Price')
fig4 = plt.figure(figsize=(8,6))
plt.plot(predict, 'r', label='Original Price')
plt.plot(y, 'g', label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
st.pyplot(fig4)

# Add in logic for short-term, medium-term, and long-term stocks to suggest the user to buy
current_price = data.Close.iloc[-1].item()
ma50 = ma_50_days.iloc[-1].item()
ma100 = ma_100_days.iloc[-1].item()
ma200 = ma_200_days.iloc[-1].item()

# Define your short-term, medium-term, and long-term buy logic based on price trends
if current_price > ma50 and current_price > ma100 and current_price > ma200: 
    suggestion = "Long-Term Buy: Stock is above all three moving averages, indicating a strong uptrend."
elif current_price > ma50 and current_price > ma100:
    suggestion = "Medium-Term Buy: Stock is above short-term and mid-term moving averages but may face resistance at the long-term moving average."
elif current_price > ma50: 
    suggestion = "Short-Term Buy: Stock is short-term moving average, but long-term trends are not favorable."
elif current_price < ma50 and current_price < ma100 and current_price < ma200:
    suggestion = "Short-Term Sell: Stock is below all three moving averages, indicating a downtrend."
else: 
    suggestion = "Hold: Stock is in neutral position"

# Display suggestion
st.subheader('Stock Buy Suggestion')
st.write(suggestion)