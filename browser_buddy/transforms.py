import time
import traceback

import httpx
from langchain.embeddings import OpenAIEmbeddings


reader_url = 'https://r.jina.ai/'

def reader_transform(bookmark_item):
    result = None
    error_message = None
    for _ in range(5):
        url = bookmark_item.url
        try:
            req_url = reader_url + url
            resp = httpx.get(req_url)
            if resp.status_code == 200:
                result = resp.text
                break
            else:
                error_message = f'status code: {resp.status_code} | url: {url} | resp content: {resp.content}'
                print(error_message)
                time.sleep(3)
        except Exception as e:
            error_message = f'error detail: {traceback.format_exc()}'
            print(error_message)
            time.sleep(3)

    if result:
        return result
    else:
        return Exception(error_message)


def embedding_transform(bookmark_item):
    content = bookmark_item.content
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_documents([content])
    return vector


def extract_keywords_transform(bookmark_item):
    content = bookmark_item.content
    return ['a', 'b', 'c']
