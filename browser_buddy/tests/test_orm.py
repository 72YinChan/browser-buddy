import json
import random
import time
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime

import requests
from sqlalchemy import select, insert, update, delete

from models import Session
from models.bookmarks import Bookmarks


def parse_bookmark_bar_data(bookmark_bar_data):
    def dfs(bookmark_data):
        result = []
        bm_data_type = bookmark_data.get('type')
        if bm_data_type == 'folder':
            for child in bookmark_data.get('children') or []:
                result.extend(dfs(child))
        elif bm_data_type == 'url':
            item = dict(
                url=bookmark_data.get('url'),
                name=bookmark_data.get('name'),
                date_added=bookmark_data.get('date_added'),
                date_last_used=bookmark_data.get('date_last_used'),
            )
            result.append(item)
        else:
            print(f'catch new bm_data_type {bm_data_type}')

        return result

    return dfs(bookmark_bar_data)


edge_bookmark_path = r'C:\Users\YinChan\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks'
edge_history_path = r'C:\Users\YinChan\AppData\Local\Microsoft\Edge\User Data\Default\History'

with open(edge_bookmark_path, 'r', encoding='utf-8') as f:
    raw_bookmark_data = json.load(f)

bookmark_data = raw_bookmark_data.get('roots')
bookmark_bar_data = bookmark_data.get('bookmark_bar')
other_data = bookmark_data.get('other')
synced_data = bookmark_data.get('synced')

flatten_bookmark_list = parse_bookmark_bar_data(bookmark_bar_data)
random_flatten_bookmark_list1 = random.choices(flatten_bookmark_list[50:], k=10)
random_flatten_bookmark_list2 = random.choices(flatten_bookmark_list[50:], k=10)


base_url = 'https://r.jina.ai/'

def get_url_content(item):
    try:
        url = item.get('url')
        req_url = base_url + url
        res = requests.get(req_url)
        print(f'status_code: {res.status_code} | length: {len(res.text)} | url: {url}')
        return res.text
    except Exception as e:
        message = f'fxxk | {str(e)}'
        print(message)
        return message


# start_time = time.perf_counter()
# with ThreadPool(10) as pool:
#     result1 = pool.map(get_url_content, random_flatten_bookmark_list1)
# elapsed_time = time.perf_counter() - start_time
# print(f'elapsed_time: {elapsed_time}')
#
#
# insert_data_list1 = []
# for item, content in zip(random_flatten_bookmark_list1, result1):
#     insert_data = dict(
#         url=item.get('url'),
#         name=item.get('name'),
#         content=content,
#         date_added=item.get('date_added'),
#         date_last_used=item.get('date_added'),
#     )
#     insert_data_list1.append(insert_data)
#
#
# start_time = time.perf_counter()
# with ThreadPool(10) as pool:
#     result2 = pool.map(get_url_content, random_flatten_bookmark_list2)
# elapsed_time = time.perf_counter() - start_time
# print(f'elapsed_time: {elapsed_time}')
#
#
# insert_data_list2 = []
# for item, content in zip(random_flatten_bookmark_list2, result2):
#     insert_data = dict(
#         url=item.get('url'),
#         name=item.get('name'),
#         content=content,
#         date_added=item.get('date_added'),
#         date_last_used=item.get('date_added'),
#     )
#     insert_data_list2.append(insert_data)
#
#
# print(json.dumps(insert_data_list1, ensure_ascii=False))
# print(json.dumps(insert_data_list2, ensure_ascii=False))


with Session() as session, session.begin():
    # new_bookmarks1 = session.scalars(
    #     insert(Bookmarks).returning(Bookmarks),
    #     insert_data_list1,
    # )
    # print(new_bookmarks1)
    # for item in new_bookmarks1:
    #     print(item)
    #
    # time.sleep(5)
    #
    # new_bookmarks2 = session.scalars(
    #     insert(Bookmarks).returning(Bookmarks),
    #     insert_data_list2,
    # )
    # print(new_bookmarks2)
    # for item in new_bookmarks2:
    #     print(item)

    bookmarks = session.scalars(
        select(Bookmarks)
    )
    for item in bookmarks:
        print(item)
        print(item.create_date)
        print(item.update_date)

    # update_data_list = [
    #     {'id': index + 1, 'content': 'wtf'}
    #     for index in range(10)
    # ]
    # session.execute(
    #     update(Bookmarks),
    #     update_data_list,
    # )

    bookmarks = session.scalars(
        update(Bookmarks).where(Bookmarks.id <= 10).values(content='wtf').returning(Bookmarks))
    for item in bookmarks:
        print(item.id, item.content)
