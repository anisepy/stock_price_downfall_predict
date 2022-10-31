import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd


def yfloader(stock_code: str, start_d: str, end_d: str) -> pd.DataFrame:
    yf.pdr_override()
    df = pdr.get_data_yahoo([stock_code, "^KS11"], start=start_d, end=end_d)
    df = df.reset_index()
    df = df[["Date", "Close"]]
    df.columns = ["date", "price", "kospi"]

    df.date = pd.to_datetime(df.date)
    df["date"] = df["date"].dt.strftime("%Y-%m")  # C_0 : delete day
    df1 = pd.DataFrame(df.groupby("date")["price"].mean())
    df1 = df1.reset_index()  # C_1 : price monthly mean
    df2 = pd.DataFrame(df.groupby("date")["kospi"].mean())
    df2 = df2.reset_index()  # C_2 : stock monthly mean
    df = df1.merge(df2, how="left")
    return "done"


if __name__ == "__main__":  # pragma: no cover
    yfloader()
