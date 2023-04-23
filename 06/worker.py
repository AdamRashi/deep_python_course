from threading import Thread
from urllib.request import urlopen
from json.encoder import JSONEncoder
from collections import Counter


class Worker(Thread):
    def __init__(self, url: str, k: int):
        super().__init__()
        self.url = url
        self.k = k

    def run(self):
        with urlopen(self.url) as f:
            res = Counter(f.read().decode('utf-8').split()) \
                .most_common(self.k)
        return JSONEncoder().encode(dict(res))
