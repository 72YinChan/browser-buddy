import json

import redis

from bookmark import BookmarkItem
from transforms import reader_transform, embedding_transform, extract_keywords_transform


class BookmarkProfile(object):

    queue_name = 'bookmark_queue'

    def __init__(self, transform_list):
        self.transform_list = transform_list
        self.redis_client = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0,
        )

    def __call__(self):
        while True:
            key, raw_bm_item_json = self.redis_client.brpop([self.queue_name], timeout=0)
            bm_item_json = raw_bm_item_json.decode()
            bm_item = BookmarkItem(**json.loads(bm_item_json))

            for transform in self.transform_list:
                transform(bm_item)


if __name__ == '__main__':
    transform_list = [
        reader_transform,
        embedding_transform,
        extract_keywords_transform,
    ]
    bm_profile = BookmarkProfile(transform_list)
    bm_profile()
