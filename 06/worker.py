import json
from threading import Thread
from urllib.request import urlopen
from collections import Counter
import validators


class Worker(Thread):
    def __init__(self, task_queue, k: int):
        super().__init__()
        self.task_queue = task_queue
        self.k = k

    def run(self):

        client_socket, address = self.task_queue.get()

        print(f"[+] Got connection from {address}")
        while True:
            url = client_socket.recv(4096).decode()

            if not url:
                break

            if not validators.url(url):
                print(f"[-] Error: URL is malformed")
                continue

            with urlopen(url) as doc:
                res = Counter(doc.read().decode().split()) \
                    .most_common(self.k)

            client_socket.send(json.dumps(dict(res)).encode())

        client_socket.close()
        print(f"[+] Connection with {address} closed")
        self.task_queue.task_done()
