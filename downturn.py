import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def downturn(df):
    df = df.set_index("date")
    scaled = MinMaxScaler().fit(df).transform(df)
    df_scaled = pd.DataFrame(scaled, columns=["pricemm", "kospimm"])
    # column 3 : priceMinMax, column 4 : kospiMinMax
    df = df.reset_index("date")
    df_scaled.insert(0, "date", df["date"])
    df = df.merge(df_scaled, how="left")

    for i in range(len(df) - 1):  # making the slope columns
        df.loc[i + 1, "price_slope"] = df.iloc[i + 1, 3] - df.iloc[i, 3]  # C_5
        df.loc[i + 1, "kospi_slope"] = df.iloc[i + 1, 4] - df.iloc[i, 4]  # C_6
    df = df.bfill()
    for i in range(len(df)):  # making the downturn(y) column
        if df.loc[i, "price_slope"] < df.loc[i, "kospi_slope"]:
            df.loc[i, "downturn"] = 1
        else:
            df.loc[i, "downturn"] = 0
    return "done"
