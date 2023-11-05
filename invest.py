import pandas as pd
import yfinance as yf
import pandas as pd
import plotly.express as px
from prophet import Prophet
import streamlit as st
import datetime
import matplotlib.pyplot as plt 

st.title('Buy or Sell')

watchlist = ['AH.BK','SPVI.BK','MEGA.BK','TISCO.BK','NTES','AON','other']
my_watchlist = st.selectbox("choose your watchlist", watchlist)
if my_watchlist == 'other':
    my_ticker = st.text_input('Type ticker')
else:
    my_ticker = my_watchlist

d_start = st.date_input("Select start date", value=None, format="MM-DD-YYYY", key=1)
d_end = st.date_input("Select end date", value=None, format="MM-DD-YYYY", key=2)
d_period = st.number_input("Period", min_value=30, max_value=180, value=30, placeholder="forcasting period")

# st.write('start date:', d_start)
# st.write('end date:', d_end)

if my_ticker =="" :
    pass
else:
    df = yf.download(my_ticker, start=d_start, end=d_end).reset_index()
    columns = ['Date','Close']
    ndf = pd.DataFrame(df, columns = columns)
    prophet_df = ndf.rename(columns={'Date':'ds','Close':'y'})

    m = Prophet()
    m.fit(prophet_df) #train data
    future = m.make_future_dataframe(periods=d_period) #future period
    forecast = m.predict(future) 

    px.line(forecast, x='ds', y='yhat')
    figure = m.plot(forecast,xlabel="ds",ylabel="y") #black dot = price of stock
    figure2 = m.plot_components(forecast)

    st.pyplot(figure)
    st.pyplot(figure2)
