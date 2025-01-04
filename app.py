import numpy as np 
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st

model = load_model('/Users/alexandraspadafino/Desktop/Stock-Market-Predictor/Stock Predictions Model.keras')