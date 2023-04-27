import json
from collections import Counter
from queue import Queue
from threading import Thread, current_thread, Lock
from urllib.error import URLError
from urllib.request import urlopen

task_counter = 0


class Worker(Thread):
    def __init__(self, task_queue: Queue, top_k: int, **kwargs):
        super().__init__(**kwargs)
        self.task_queue = task_queue
        self.top_k = top_k
        self.lock = Lock()

    def run(self):
        while True:
            client_socket, address = self.task_queue.get()
            print(f"[+{current_thread().name}] Got connection from {address}")
            global task_counter

            while True:
                try:
                    data = client_socket.recv(10000)

                    url = data.decode()
                    print(f"[+{current_thread().name}] Started fetching {url}")

                    with urlopen(url) as doc:
                        word_counts = Counter(doc.read().decode().split()).most_common(
                            self.top_k
                        )

                    client_socket.send(json.dumps(dict(word_counts)).encode())
                    print(f"[+{current_thread().name}] Finished fetching {url}")
                    with self.lock:
                        task_counter += 1
                        print(
                            f"[={current_thread().name}]===TOTAL TASKS DONE: {task_counter}==="
                        )

                except ConnectionAbortedError:
                    break

                except URLError:
                    print(f"Invalid URL: {url}")
                    client_socket.send(f"Invalid URL {url}".encode())
                    with self.lock:
                        task_counter += 1
                        print(
                            f"[={current_thread().name}]===TOTAL TASKS DONE: {task_counter}==="
                        )
                    continue

                except Exception as e:
                    print(f"[-{current_thread().name}] Error: {e}")
                    break

            client_socket.close()
            self.task_queue.task_done()
            print(f"[+{current_thread().name}] closed connection from {address}")
