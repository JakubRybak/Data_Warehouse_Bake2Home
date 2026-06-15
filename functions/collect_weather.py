# main.py
import functions_framework
import urllib.request, urllib.parse, json, ssl
from google.cloud import bigquery


@functions_framework.http
def collect_weather(request):
    client = bigquery.Client(project="bake2home-data-warehouse")

    query = """
        SELECT sk_order_item, longitude, latitude, FORMAT_DATE('%Y-%m-%d', sk_date_order) as date_str FROM `gold.fact_order_item` fact_orders
        LEFT JOIN `gold.dim_customer_address` dim_address ON dim_address.sk_customer_address = fact_orders.sk_customer_address
        WHERE weather_morning_was_rainy = -1 AND sk_date_order < CURRENT_DATE()
        GROUP BY sk_order_item, longitude, latitude, date_str;
    """
    results = client.query(query).result()

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def get_weather(dict):
        date = dict["date_str"]
        params = {
            "latitude": dict["latitude"],
            "longitude": dict["longitude"],
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
            "weather_morning_precip_prob": weather_morning_precip_prob,
            "weather_morning_precip_sum_mm": weather_morning_precip_sum_mm,
            "weather_morning_was_rainy": weather_morning_was_rainy,
        }

    rows = list(results)

    i = 0
    for row in rows:
        print(str(i))
        res = get_weather(row)
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
            + str(row["sk_order_item"])
        )
        res = client.query(query).result()
        i = i + 1

    return 200
