from pandas import to_datetime
from pandas.io.json import json_normalize
from requests import get


def chart(
    apiToken="demo",
    apiVersion="v0",
    host="api.fugle.tw",
    output="pandas",
    symbolId="2884",
):
    url = "https://{}/realtime/{}/intraday/chart".format(host, apiVersion)
    params = dict(apiToken=apiToken, symbolId=symbolId)
    response = get(url=url, params=params)
    json = response.json()
    if response.status_code != 200:
        if output == "pandas":
            return json_normalize(json)
        else:
            return json
    chart = json["data"]["chart"]
    if output == "pandas":
        chart = [dict(at=at, **rest) for at, rest in chart.items()]
        df = json_normalize(chart)
        df["at"] = to_datetime(df["at"])
        df = df.sort_values("at")
        df = df.reset_index(drop=True)
        return df
    else:
        return chart