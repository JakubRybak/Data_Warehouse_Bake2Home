import functions_framework
import pandas as pd
from google.cloud import bigquery


@functions_framework.http
def weather_update_orders(request):
    client = bigquery.Client(project="bake2home-data-warehouse")

    query_weather = "SELECT * FROM `bake2home-data-warehouse.bronze.weather`"

    df_results_weather = client.query(query_weather).to_dataframe()

    saved_weathers = {}

    for _, row in df_results_weather.iterrows():
        latitude = row["latitude"]
        longitude = row["longitude"]
        date = row["date"]
        saved_weathers[str(latitude) + str(longitude) + str(date)] = row

    query = """
        SELECT sk_order_item, longitude, latitude, FORMAT_DATE('%Y-%m-%d', sk_date_order) as date_str FROM `gold.fact_order_item` fact_orders
        LEFT JOIN `gold.dim_customer_address` dim_address ON dim_address.sk_customer_address = fact_orders.sk_customer_address
        WHERE weather_morning_was_rainy = -1 AND sk_date_order < CURRENT_DATE()
        GROUP BY sk_order_item, longitude, latitude, date_str;
    """

    missing_data = client.query(query).result()

    i = 0
    for data in missing_data:
        longitude = data["longitude"]
        latitude = data["latitude"]
        date_str = data["date_str"]
        key = str(latitude) + str(longitude) + str(date)
        if key in saved_weathers:
            res = saved_weathers[str(latitude) + str(longitude) + str(date)]
            query = (
                "UPDATE `gold.fact_order_item` fact_orders "
                + "SET weather_morning_was_rainy = "
                + str(res["weather_morning_was_rainy"])
                + ", "
                + "weather_morning_precip_sum_mm = "
                + str(res["weather_morning_precip_sum_mm"])
                + ", "
                + "weather_morning_precip_prob = "
                + str(res["weather_morning_precip_prob"])
                + " "
                + "WHERE sk_order_item = "
                + str(data["sk_order_item"])
            )
            res = client.query(query).result()
    return 200
