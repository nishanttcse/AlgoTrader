import pandas as pd
import pandas_ta as ta

def add_indicators(df):
    df["RSI"] = ta.rsi(df["Close"], length=14)
    df["20DMA"] = df["Close"].rolling(20).mean()
    df["50DMA"] = df["Close"].rolling(50).mean()
    return df
