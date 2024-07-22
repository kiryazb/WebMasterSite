import asyncio
from datetime import datetime, timedelta
from functools import reduce
from itertools import groupby

import requests

import config
from api.actions.indicators import _add_new_indicators, _add_top
from api.actions.metrics_queries import _get_top_data_query
from api.actions.metrics_url import _get_top_data_urls
from db.models import QueryIndicator, QueryUrlTop

from db.session import async_session
from db.utils import get_last_update_date, add_last_update_date

ACCESS_TOKEN = f"{config.ACCESS_TOKEN}"
USER_ID = f"{config.USER_ID}"
HOST_ID = f"{config.HOST_ID}"

date_format = "%Y-%m-%d"


def create_url(date_from):
    date_to = datetime.now() - timedelta(days=2)
    date_to = date_to.date()
    if date_to > date_from:
        date_from += timedelta(days=1)
        return (f"https://api.webmaster.yandex.net/v4/user/{USER_ID}/hosts/{HOST_ID}/search-queries/all/history?"
                f"query_indicator=TOTAL_SHOWS&"
                f"query_indicator=TOTAL_CLICKS&"
                f"query_indicator=AVG_SHOW_POSITION&"
                f"query_indicator=AVG_CLICK_POSITION&"
                f"date_from={date_from}&"
                f"date_to={date_to}")
    return -1


async def get_response(async_session):
    last_update_date = await get_last_update_date(async_session, QueryIndicator)
    print("last update date:", last_update_date)
    if not last_update_date:
        last_update_date = (datetime.now() - timedelta(days=60))
    print("Начало выгрузки")
    URL = create_url(last_update_date.date())
    if URL == -1:
        return -1
    response = requests.get(URL, headers={'Authorization': f'OAuth {ACCESS_TOKEN}',
                                          "Content-Type": "application/json; charset=UTF-8"})

    return response


async def add_data(response: requests.models.Response | int):
    if response == -1:
        print("Все данные Indicators уже в базе")
        return

    indicators = response.json()["indicators"]

    data_for_db = list()
    data_for_total_ctr = dict()
    for indicator in indicators:
        for element in indicators[indicator]:
            date = datetime.strptime(element["date"].split("T")[0], date_format)
            data_for_db.append(QueryIndicator(indicator=indicator,
                                              value=round(element["value"], 1),
                                              date=date))
            if date not in data_for_total_ctr:
                data_for_total_ctr[date] = [0, 0]
            if indicator == "TOTAL_CLICKS":
                data_for_total_ctr[date][0] = element["value"]
            elif indicator == "TOTAL_SHOWS":
                data_for_total_ctr[date][1] = element["value"]
    for key, value in data_for_total_ctr.items():
        value = round(value[0] * 100 / value[1], 2) if value[1] != 0 else 0
        data_for_db.append(QueryIndicator(
            indicator="TOTAL_CTR",
            value=value,
            date=key
        )
        )

    await _add_new_indicators(data_for_db, async_session)

    return data_for_db


async def add_top():
    last_update_date = await get_last_update_date(async_session, QueryUrlTop)
    print("last update date for top 3, 5, 10, 20, 30:", last_update_date)
    if not last_update_date:
        last_update_date = (datetime.now() - timedelta(days=60))

    top_position = 3, 5, 10, 20, 30
    add_values = []
    for top in top_position:
        queries_top = await _get_top_data_query(top, async_session)
        if queries_top:
            queries_top.sort(key=lambda x: x[-1])
        grouped_data = {k: list(v) for k, v in groupby(queries_top, key=lambda x: x[-1])}
        for key, value in grouped_data.items():
            if key > last_update_date:
                impression_sum = sum(x[0] for x in value)
                clicks_sum = sum(x[1] for x in value)
                position_sum = round(sum(x[2] for x in value) / len(value), 2)
                add_values.append(
                    QueryUrlTop(top=top, type="query", position=position_sum, clicks=clicks_sum,
                                impression=impression_sum,
                                date=key))

    top_position = 3, 5, 10, 20, 30
    for top in top_position:
        urls_top = await _get_top_data_urls(top, async_session)
        if urls_top:
            urls_top.sort(key=lambda x: x[-1])
        grouped_data = {k: list(v) for k, v in groupby(urls_top, key=lambda x: x[-1])}
        for key, value in grouped_data.items():
            if key > last_update_date:
                impression_sum = sum(x[0] for x in value)
                clicks_sum = sum(x[1] for x in value)
                position_sum = round(sum(x[2] for x in value) / len(value), 2)
                add_values.append(
                    QueryUrlTop(top=top, type="url", position=position_sum, clicks=clicks_sum,
                                impression=impression_sum,
                                date=key))

    await _add_top(add_values, async_session)


async def main():
    response = await get_response(async_session)
    await add_data(response)
    print("Indicators загружены. Начинаем загрузку TOP")
    await add_top()
    print("Выгрузка завершена")


if __name__ == '__main__':
    asyncio.run(main())
