"""import pandas as pd
import ta

def backtest(df: pd.DataFrame, capital: float = 100000):
    df = df.copy()
    
    # Ensure 'Close' exists
    if "Close" not in df.columns:
        raise ValueError("'Close' column missing in the data")

    # Calculate indicators
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()

    # Generate buy signal: RSI < 30 and 20DMA crosses above 50DMA
    df['Signal'] = (
        (df['RSI'] < 30) &
        (df['20DMA'] > df['50DMA']) &
        (df['20DMA'].shift(1) <= df['50DMA'].shift(1))
    )

    df['Position'] = df['Signal'].astype(int).shift(1).fillna(0)

    # Portfolio logic
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Returns'] * df['Position']
    df['Cumulative'] = (1 + df['Strategy_Returns']).cumprod()

    return df"""

import pandas as pd
import ta

def backtest(df, initial_capital=100000):
    df = df.copy()

    # Technical Indicators
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
    df['20DMA'] = df['Close'].rolling(window=20).mean()
    df['50DMA'] = df['Close'].rolling(window=50).mean()

    # Drop rows with NaNs
    df.dropna(inplace=True)

    # Initialize Signal column
    df['Signal'] = ((df['RSI'] < 40) & (df['Close'] > df['50DMA'])).astype(int)


    # Generate Buy/Sell Signals
    for i in range(1, len(df)):
        # Buy Signal
        if (df['RSI'].iloc[i] < 45 and
            df['20DMA'].iloc[i] > df['50DMA'].iloc[i] and
            df['20DMA'].iloc[i-1] <= df['50DMA'].iloc[i-1]):
            df.at[df.index[i], 'Signal'] = 1

        # Sell Signal
        elif (df['RSI'].iloc[i] > 65 and
              df['20DMA'].iloc[i] < df['50DMA'].iloc[i] and
              df['20DMA'].iloc[i-1] >= df['50DMA'].iloc[i-1]):
            df.at[df.index[i], 'Signal'] = -1

    # Calculate positions (1 if holding, 0 otherwise)
    df['Position'] = df['Signal'].replace(to_replace=0, method='ffill').clip(lower=0)

    # Daily returns and strategy returns
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Returns'] * df['Position']
    df['Cumulative'] = (1 + df['Strategy_Returns']).cumprod()

    # Log signal count
    signal_count = df['Signal'].value_counts().to_dict()
    print(f"✅ Buy signals: {signal_count.get(1, 0)}, Sell signals: {signal_count.get(-1, 0)}")

    return df

