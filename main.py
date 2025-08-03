"""import config
from services.data_fetcher import fetch_data
from strategies.strategy import backtest
from services.sheet_logger import connect_to_sheet, log_dataframe
from services.notifier import send_alert
from services.ml_model import train_predictor
import pandas as pd

def run():
    try:
        sheet = connect_to_sheet(config.GOOGLE_SHEET_NAME, config.CREDENTIALS_FILE)
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheet: {e}")
        return

    for ticker in config.TICKERS:
        try:
            print(f"\n📊 Processing {ticker}...")
            df = fetch_data(ticker, config.PERIOD, config.INTERVAL)

            # Flatten MultiIndex columns if needed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(filter(None, col)).strip() for col in df.columns.values]

            result_df = backtest(df, config.INITIAL_CAPITAL)
            print(result_df.tail(5))  # Preview recent data

            log_dataframe(sheet, result_df.tail(30), f"{ticker}_Backtest")

            # Check if 'Signal' exists and the last signal is True
            if "Signal" in result_df.columns:
                last_signal = result_df["Signal"].iloc[-1]
                if pd.notna(last_signal) and bool(last_signal):
                    send_alert(f"📢 Buy Signal for {ticker} ✅")
            else:
                print("⚠️ 'Signal' column missing in result_df.")

            acc = train_predictor(result_df)
            print(f"✅ Prediction accuracy for {ticker}: {acc:.2f}")
        
        except Exception as e:
            print(f"❌ Error while processing {ticker}: {e}")

if __name__ == "__main__":
    run()"""



"""import config
import pandas as pd
from services.data_fetcher import fetch_data
from strategies.strategy import backtest
from services.sheet_logger import connect_to_sheet, log_dataframe
from services.notifier import send_alert
from services.ml_model import train_predictor
from visualization.plot import plot_signals  # 📈 Visualization

def run():
    try:
        sheet = connect_to_sheet(config.GOOGLE_SHEET_NAME, config.CREDENTIALS_FILE)
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheet: {e}")
        return

    for ticker in config.TICKERS:
        try:
            print(f"\n📊 Processing {ticker}...")
            df = fetch_data(ticker, config.PERIOD, config.INTERVAL)

            # 🔧 Flatten MultiIndex columns from yfinance if needed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(filter(None, col)).strip() for col in df.columns.values]

            # 🧼 Standardize column names if needed (e.g., Close_TICKER to Close)
            close_cols = [col for col in df.columns if "Close" in col]
            if len(close_cols) == 1 and close_cols[0] != "Close":
                df.rename(columns={close_cols[0]: "Close"}, inplace=True)

            if "Close" not in df.columns:
                raise ValueError(f"'Close' column missing in data for {ticker}. Available columns: {df.columns.tolist()}")

            result_df = backtest(df, config.INITIAL_CAPITAL)
            print(result_df.tail(5))  # Preview recent data

            log_dataframe(sheet, result_df.tail(30), f"{ticker}_Backtest")

            # 🚨 Alert if latest signal is True
            if "Signal" in result_df.columns:
                last_signal = result_df["Signal"].iloc[-1]
                if pd.notna(last_signal) and bool(last_signal):
                    send_alert(f"📢 Buy Signal for {ticker} ✅")
            else:
                print("⚠️ 'Signal' column missing in result_df.")

            acc = train_predictor(result_df)
            print(f"✅ Prediction accuracy for {ticker}: {acc:.2f}")

            # 📈 Plot chart with signals + RSI
            plot_signals(result_df, ticker)

        except Exception as e:
            print(f"❌ Error while processing {ticker}: {e}")

if __name__ == "__main__":
    run()"""

import config
from services.data_fetcher import fetch_data
from strategies.strategy import backtest
from services.sheet_logger import connect_to_sheet, log_dataframe
from services.notifier import send_alert
from services.ml_model import train_predictor
import pandas as pd

def run():
    try:
        sheet = connect_to_sheet(config.GOOGLE_SHEET_NAME, config.CREDENTIALS_FILE)
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheet: {e}")
        return

    for ticker in config.TICKERS:
        try:
            print(f"\n📊 Processing {ticker}...")
            df = fetch_data(ticker, config.PERIOD, config.INTERVAL)

            # Flatten MultiIndex columns if needed
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(filter(None, col)).strip() for col in df.columns.values]

            # Extend period to increase chance of variation
            if len(df) < 100:
                print("⚠️ Data might be too short. Consider extending the PERIOD.")

            result_df = backtest(df, config.INITIAL_CAPITAL)
            print(result_df.tail(5))  # Preview recent data

            log_dataframe(sheet, result_df.tail(30), f"{ticker}_Backtest")

            # Check if 'Signal' exists and the last signal is True
            if "Signal" in result_df.columns:
                last_signal = result_df["Signal"].iloc[-1]
                if pd.notna(last_signal) and bool(last_signal):
                    send_alert(f"📢 Buy Signal for {ticker} ✅")
            else:
                print("⚠️ 'Signal' column missing in result_df.")

            # Check variation before training ML
            if result_df['Signal'].nunique() < 2:
                print("⚠️ Not enough variation in 'Signal' to train ML model. Try loosening conditions or increasing period.")
                continue

            acc = train_predictor(result_df)
            print(f"✅ Prediction accuracy for {ticker}: {acc:.2f}")

        except Exception as e:
            print(f"❌ Error while processing {ticker}: {e}")

if __name__ == "__main__":
    run()


