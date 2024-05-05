import json
from typing import Optional, List

from dataclasses import dataclass


@dataclass
class BookmarkItem:

    url: str
    name: str
    date_added: str
    date_last_used: str
    content: Optional[str] = None
    embedding: Optional[List[float]] = None

    def serialize(self):
        return dict(
            url=self.url,
            name=self.name,
            date_added=self.date_added,
            date_last_used=self.date_last_used,
            content=self.content,
        )

    def __str__(self):
        url = self.url if len(self.url) <= 25 else self.url[:21] + ' ...'
        name = self.name if len(self.name) <= 25 else self.name[:21] + ' ...'
        return f"<BookMarkItem(url={url}, name={name})>"

    @staticmethod
    def parse_bookmark_data(bookmark_path):
        def dfs(bookmark_data):
            result = []
            bm_data_type = bookmark_data.get('type')
            if bm_data_type == 'folder':
                for child in bookmark_data.get('children') or []:
                    result.extend(dfs(child))
            elif bm_data_type == 'url':
                item = BookmarkItem(
                    url=bookmark_data.get('url'),
                    name=bookmark_data.get('name'),
                    date_added=bookmark_data.get('date_added'),
                    date_last_used=bookmark_data.get('date_last_used'),
                )
                result.append(item)
            else:
                print(f'catch new bm_data_type {bm_data_type}')

            return result

        with open(bookmark_path, 'r', encoding='utf-8') as f:
            raw_bookmark_data = json.load(f)
        bookmark_bar_data = raw_bookmark_data.get('roots').get('bookmark_bar')
        return dfs(bookmark_bar_data)
