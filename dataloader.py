import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def yfloader(stock_code: str, start_day: str, end_day: str) -> pd.DataFrame:

    yf.pdr_override()
    # 해당 종목의 종가 데이터 불러오기
    df = pdr.get_data_yahoo(
        [stock_code, "^KS11"], start=start_day, end=end_day
    )
    df = df.reset_index()
    df = df[["Date", "Close"]]
    df.columns = ["date", "price", "kospi지수"]

    # 월별 평균값 계산해서 새로운 열 생성
    df.date = pd.to_datetime(df.date)
    df["date"] = df["date"].dt.strftime("%Y-%m")
    df1 = pd.DataFrame(df.groupby("date")["price"].mean())
    df1 = df1.reset_index()
    df2 = pd.DataFrame(df.groupby("date")["kospi지수"].mean())
    df2 = df2.reset_index()
    df = df1.merge(df2, how="left")

    # MinMaxScaler로 price, kospi 데이터 정규화
    df = df.set_index("date")
    scaler = MinMaxScaler()
    scaler.fit(df)
    scaled = scaler.transform(df)
    df_scaled = pd.DataFrame(scaled, columns=["pricemm", "kospimm"])
    # 3열 : priceMinMax, 4열 : kospiMinMax
    df = df.reset_index("date")
    df_scaled.insert(0, "date", df["date"])

    df = df.merge(df_scaled, how="left")

    # 기울기 열을 만드는 for문
    for i in range(len(df) - 1):
        df.loc[i + 1, "price_slope"] = df.iloc[i + 1, 3] - df.iloc[i, 3]
        df.loc[i + 1, "kospi_slope"] = df.iloc[i + 1, 4] - df.iloc[i, 4]
        # 5열 : 주가 변화율, 6열 : kospi변화율

    df = df.bfill()

    # 주가 하락세 열을 만드는 for문
    for i in range(len(df)):
        df.loc[i, "k_s - p_s"] = df.iloc[i, 6] - df.iloc[i, 5]

        if df.loc[i, "price_slope"] < df.loc[i, "kospi_slope"]:
            df.loc[i, "downturn"] = 1
        else:
            df.loc[i, "downturn"] = 0

    df.to_csv("test.csv", index=False)
    return "done"


if __name__ == "__main__":  # pragma: no cover
    yfloader()

# def load_train():
#     data = pd.read_csv('data/emart_downturn.csv')
#     target = 'winPlacePerc'
#     df = data.copy()
#     # df = df.dropna()
#     # df = df.drop(['matchType','Id','matchId','groupId','killPlace'],axis=1)

#     return df, target

# def load_test():
#     test = pd.read_csv('./data/test_V2.csv')

#     submission = pd.read_csv("./data/sample_submission_V2.csv")

#     return test, submission
