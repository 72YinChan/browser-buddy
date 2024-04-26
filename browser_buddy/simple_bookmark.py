import json
import sqlite3
import time
import random
from multiprocessing.dummy import Pool as ThreadPool

import requests
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


database_uri = r'sqlite:////F:/Projects/browser-buddy/browser_buddy/browser_buddy.db'
engine = create_engine(database_uri, echo=True)
Base = declarative_base()


class BookMark(Base):

    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    name = Column(String(255))
    content = Column(Text)
    date_added = Column(DateTime)
    date_last_used = Column(DateTime)

    def __repr__(self):
        return f"<BookMark(url={self.url}, name={self.name}>"


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

with open(edge_bookmark_path, 'r', encoding='utf-8') as f:
    raw_bookmark_data = json.load(f)

bookmark_data = raw_bookmark_data.get('roots')
bookmark_bar_data = bookmark_data.get('bookmark_bar')
other_data = bookmark_data.get('other')
synced_data = bookmark_data.get('synced')

flatten_bookmark_list = parse_bookmark_bar_data(bookmark_bar_data)
# print(json.dumps(flatten_bookmark_list, ensure_ascii=False))
print(len(flatten_bookmark_list))


base_url = 'https://r.jina.ai/'

random_flatten_bookmark_list = [
    {
        "url": "https://zhuanlan.zhihu.com/p/269201440",
        "name": "一文看懂架构图怎么画 - 知乎",
        "date_added": "13288383185385910",
        "date_last_used": "0"
    },
    {
        "url": "https://ddys.art/",
        "name": "低端影视 - 超清在线视频站",
        "date_added": "13321845079590881",
        "date_last_used": "13358519608820701"
    },
    {
        "url": "https://cloud.tencent.com/developer/article/2095442",
        "name": "Python 二次开发 AutoCAD 简介「建议收藏」 - 腾讯云开发者社区-腾讯云",
        "date_added": "13325618177283950",
        "date_last_used": "13325772656841349"
    },
    {
        "url": "https://blog.csdn.net/napoyong/article/details/86502649",
        "name": "ubuntu18.04安装 Broadcom Limited BCM43142 802.11b/g/n 驱动_napoyong的博客-CSDN博客",
        "date_added": "13263889284000000",
        "date_last_used": "0"
    },
    {
        "url": "https://www.cnpython.com/qa/228713",
        "name": "如何为自定义类的参数指定类型提示？ - 问答 - Python中文网",
        "date_added": "13310977323986689",
        "date_last_used": "0"
    },
    {
        "url": "https://blog.csdn.net/zmy941110/article/details/89639883",
        "name": "分享一个flask高并发部署方案_zmy941110的博客-CSDN博客_flask高并发部署",
        "date_added": "13277471561334401",
        "date_last_used": "0"
    },
    {
        "url": "https://yapi.test.starmerx.com/group/154",
        "name": "YApi-高效、易用、功能强大的可视化接口管理平台",
        "date_added": "13329159888617323",
        "date_last_used": "13334935194745898"
    },
    {
        "url": "https://blog.csdn.net/qq_29299767/article/details/104167429",
        "name": "python-snap7开发笔记_不约的小翔的博客-CSDN博客_python snap7开发手册",
        "date_added": "13270106991659800",
        "date_last_used": "0"
    },
    {
        "url": "https://developers.weixin.qq.com/miniprogram/dev/framework/",
        "name": "微信开放文档",
        "date_added": "13263323800000000",
        "date_last_used": "0"
    },
    {
        "url": "https://www.instructables.com/RPi-Pico-35-Inch-320x480-HVGA-TFT-LCD-ILI9488-Bitm/",
        "name": "RPi Pico – 3.5 Inch (320x480) HVGA TFT LCD (ILI9488) – Bitmap Image Photo Frame – Internal Flash : 8 Steps - Instructables",
        "date_added": "13307167552242628",
        "date_last_used": "0"
    }
]

def get_url_content(item):
    url = item.get('url')
    req_url = base_url + url
    res = requests.get(req_url)
    print(f'status_code: {res.status_code} | length: {len(res.text)} | url: {url}')


start_time = time.perf_counter()
with ThreadPool(5) as pool:
    pool.map(get_url_content, random_flatten_bookmark_list)
elapsed_time = time.perf_counter() - start_time
print(f'elapsed_time: {elapsed_time}')


# start_time = time.perf_counter()
# for item in random_flatten_bookmark_list:
#     url = item.get('url')
#     req_url = base_url + url
#     res = requests.get(req_url)
#     print(f'status_code: {res.status_code} | length: {len(res.text)} | url: {url}')
# elapsed_time = time.perf_counter() - start_time
# print(f'elapsed_time: {elapsed_time}')
