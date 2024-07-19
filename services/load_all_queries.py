import asyncio
from datetime import datetime
import requests

import config

from db.models import Query
from db.models import MetricsQuery
from db.session import async_session
from api.actions.queries import _add_new_urls
from api.actions.metrics_queries import _add_new_metrics
from db.utils import get_last_update_date, add_last_update_date

ACCESS_TOKEN = f"{config.ACCESS_TOKEN}"
USER_ID = f"{config.USER_ID}"
HOST_ID = f"{config.HOST_ID}"

date_format = "%Y-%m-%d"

# Формируем URL для запроса мониторинга поисковых запросов
URL = f"https://api.webmaster.yandex.net/v4/user/{USER_ID}/hosts/{HOST_ID}/query-analytics/list"


async def add_data(data, last_update_date):
    for query in data['text_indicator_to_statistics']:
        query_name = query['text_indicator']['value']
        new_url = [Query(query=query_name)]
        metrics = []
        date = query['statistics'][0]["date"]
        data_add = {
            "date": date,
            "ctr": 0,
            "position": 0,
            "impression": 0,
            "demand": 0,
            "clicks": 0,
        }
        for el in query['statistics']:
            if date != el['date']:
                date = datetime.strptime(date, date_format)
                if date > last_update_date:
                    metrics.append(MetricsQuery(
                        query=query_name,
                        date=date,
                        ctr=data_add['ctr'],
                        position=data_add['position'],
                        impression=data_add['impression'],
                        demand=data_add['demand'],
                        clicks=data_add['clicks']
                    ))
                date = el['date']
                data_add = {
                    "date": date,
                    "ctr": 0,
                    "position": 0,
                    "impression": 0,
                    "demand": 0,
                    "clicks": 0,
                }

            field = el["field"]
            if field == "IMPRESSIONS":
                data_add["impression"] = el["value"]
            elif field == "CLICKS":
                data_add["clicks"] = el["value"]
            elif field == "DEMAND":
                data_add["demand"] = el["value"]
            elif field == "CTR":
                data_add["ctr"] = el["value"]
            elif field == "POSITION":
                data_add["position"] = el["value"]
        await _add_new_urls(new_url, async_session)
        await _add_new_metrics(metrics, async_session)


async def get_data_by_page(page, last_update_date):
    body = {
        "offset": page,
        "limit": 500,
        "device_type_indicator": "ALL",
        "text_indicator": "QUERY",
        "region_ids": [],
        "filters": {}
    }

    response = requests.post(URL, json=body, headers={'Authorization': f'OAuth {ACCESS_TOKEN}',
                                                      "Content-Type": "application/json; charset=UTF-8"})

    # print(response.text[:100])
    data = response.json()

    await add_data(data, last_update_date)


async def get_all_data():
    body = {
        "offset": 0,
        "limit": 500,
        "device_type_indicator": "ALL",
        "text_indicator": "QUERY",
        "region_ids": [],
        "filters": {}
    }

    response = requests.post(URL, json=body, headers={'Authorization': f'OAuth {ACCESS_TOKEN}',
                                                      "Content-Type": "application/json; charset=UTF-8"})

    data = response.json()
    count = data["count"]
    last_update_date = await get_last_update_date(async_session, MetricsQuery)
    print("last update date:", last_update_date)
    if not last_update_date:
        last_update_date = datetime.strptime("1900-01-01", date_format)
    await add_data(data, last_update_date)
    for offset in range(500, count, 500):
        print(f"[INFO] PAGE{offset} DONE!")
        curr = datetime.now()
        await get_data_by_page(offset, last_update_date)
        print(datetime.now() - curr)


if __name__ == '__main__':
    asyncio.run(get_all_data())
