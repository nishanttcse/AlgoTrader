def train_predictor(df):
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split

    df = df.dropna().copy()

    # Check if 'Signal' column has at least 2 unique classes
    if df['Signal'].nunique() < 2:
        print("⚠️ Not enough variation in 'Signal' to train ML model.")
        df['Prediction'] = 0  # Use .loc to avoid SettingWithCopyWarning
        return 0.0

    X = df[['RSI', '20DMA', '50DMA']]
    y = df['Signal']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    # Use .loc to avoid SettingWithCopyWarning
    df.loc[y_test.index, 'Prediction'] = predictions

    accuracy = accuracy_score(y_test, predictions)
    return accuracy
