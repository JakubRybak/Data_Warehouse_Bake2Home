import functions_framework
import pandas as pd
import urllib.request, urllib.parse, json, ssl
from google.cloud import bigquery


@functions_framework.http
def collect_weather_to_parquet(request):
    client = bigquery.Client(project="bake2home-data-warehouse")

    query_weather = "SELECT * FROM `bake2home-data-warehouse.bronze.weather`"

    df_results_weather = client.query(query_weather).to_dataframe()

    saved_weathers = {}

    for _, row in df_results_weather.iterrows():
        latitude = row["latitude"]
        longitude = row["longitude"]
        date = row["date"]
        saved_weathers[(latitude, longitude, date)] = row

    query = """
        SELECT longitude, latitude, FORMAT_DATE('%Y-%m-%d', sk_date_order) as date_str FROM `gold.fact_order_item` fact_orders
        LEFT JOIN `gold.dim_customer_address` dim_address ON dim_address.sk_customer_address = fact_orders.sk_customer_address
        WHERE weather_morning_was_rainy = -1 AND sk_date_order < CURRENT_DATE()
        GROUP BY longitude, latitude, date_str;
    """

    missing_data = client.query(query).result()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def get_weather(dict):
        date = dict["date_str"]
        latitude = dict["latitude"]
        longitude = dict["longitude"]
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "models": "best_match",
            "start_date": date,
            "end_date": date,
            "hourly": "precipitation,precipitation_probability",
            "timezone": "Europe/Warsaw",
            "previous_model_run": 1,
        }

        url = (
            "https://previous-runs-api.open-meteo.com/v1/forecast?"
            + urllib.parse.urlencode(params)
        )
        req = urllib.request.Request(url, headers={"User-Agent": "raszyn/1.0"})
        with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
            data = json.loads(r.read())
        prob = []
        for prec in data["hourly"]["precipitation_probability"][6:11]:
            if prec is not None:
                prob.append(prec)
        if len(prob) > 0:
            weather_morning_precip_prob = max(prob)
        else:
            weather_morning_precip_prob = -2

        sum_mm = []
        for mm in data["hourly"]["precipitation"][6:11]:
            if mm is not None:
                sum_mm.append(mm)
        if len(sum_mm) > 0:
            weather_morning_precip_sum_mm = sum(sum_mm)
        else:
            weather_morning_precip_sum_mm = -2
        if weather_morning_precip_sum_mm >= 0 or weather_morning_precip_prob > -0:
            if (
                weather_morning_precip_prob >= 50
                and weather_morning_precip_sum_mm >= 1.0
            ) or weather_morning_precip_sum_mm >= 2.5:
                weather_morning_was_rainy = 1
            else:
                weather_morning_was_rainy = 0

        else:
            weather_morning_was_rainy = -2
        return {
            "latitude": [latitude],
            "longitude": [longitude],
            "date": [date],
            "weather_morning_precip_prob": [weather_morning_precip_prob],
            "weather_morning_precip_sum_mm": [weather_morning_precip_sum_mm],
            "weather_morning_was_rainy": [weather_morning_was_rainy],
        }

    i = 0
    total = missing_data.total_rows
    for data in missing_data:
        print("Processing data: " + str(i) + "/" + str(total))
        result_row = get_weather(data)
        df_results_weather = pd.concat(
            [df_results_weather, pd.DataFrame(result_row)], ignore_index=True
        )
        if i % 10 == 0:
            df_results_weather.to_parquet(
                "gs://bake2home-raw-data/weather/weather.parquet"
            )
            # reload table
            query = """
            CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.weather`
            OPTIONS
            (
            format = 'PARQUET',
            uris = ['gs://bake2home-raw-data/weather/weather.parquet']
            );
            """
            client.query(query).result()
        i = i + 1
    df_results_weather.to_parquet("gs://bake2home-raw-data/weather/weather.parquet")
    # reload table
    query = """
    CREATE OR REPLACE EXTERNAL TABLE `bake2home-data-warehouse.bronze.weather`
    OPTIONS
    (
    format = 'PARQUET',
    uris = ['gs://bake2home-raw-data/weather/weather.parquet']
    );
    """
    client.query(query).result()
