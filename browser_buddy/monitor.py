import asyncio
import json

from watchfiles import awatch, Change
import redis
from sqlalchemy import select

from bookmark import BookmarkItem
from models import Session
from models.bookmarks import Bookmarks


class BookmarkMonitor(object):

    queue_name = 'bookmark_queue'

    def __init__(self, bookmark_path_list):
        self.bookmark_path_list = bookmark_path_list
        self.redis_client = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
        )
        self.bm_path_2_url_list = {}
        for bm_path in self.bookmark_path_list:
            url_list = [item.url for item in BookmarkItem.parse_bookmark_data(bm_path)]
            self.bm_path_2_url_list[bm_path] = url_list

    def sync_cur_bm_list(self):
        with Session() as session:
            old_bm_list = session.scalars(select(Bookmarks))
        old_url_list = [item.url for item in old_bm_list]
        for bm_path in self.bookmark_path_list:
            pass

    async def __call__(self):
        async for change in awatch(*self.bookmark_path_list):
            for item in change:
                if item[0] == Change.added:
                    cur_bm_path = item[1]
                    old_url_list = self.bm_path_2_url_list[cur_bm_path]
                    cur_bm_list = BookmarkItem.parse_bookmark_data(cur_bm_path)

                    new_bm_list = []
                    for bm_item in cur_bm_list:
                        if bm_item.url not in old_url_list:
                            new_bm_list.append(bm_item)

                    self.bm_path_2_url_list[cur_bm_path] = [item.url for item in cur_bm_list]

                    for bm_item in new_bm_list:
                        ret = await self.push_queue(bm_item)
                        print(ret)

    def push_queue(self, bm_item):
        bm_item_json = json.dumps(bm_item.serialize(), ensure_ascii=False)
        length = self.redis_client.lpush(self.queue_name, bm_item_json)
        return length


async def main(bookmark_path_list):
    bm_monitor = BookmarkMonitor(bookmark_path_list)
    await asyncio.create_task(bm_monitor())


if __name__ == '__main__':
    bm_path_list = [
        r'C:\Users\YinChan\AppData\Local\Microsoft\Edge\User Data\Default\Bookmarks',
    ]
    asyncio.run(main(bm_path_list))
