import socket
from queue import Queue
from threading import Thread
from worker import Worker


class Master(Thread):
    def __init__(self, host, port, w: int, k: int):
        super().__init__()
        self.host = host
        self.port = port
        self.num_of_workers = w
        self.task_queue = Queue()
        self.k = k
        self.workers = []

    def start(self):

        for i in range(self.num_of_workers):
            self.workers.append(Worker(self.task_queue, self.k))

        for w in self.workers:
            w.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((self.host, self.port))
            server_sock.listen()

            print(f"[+] Server is running on {self.host}:{self.port}")
            while True:
                client_socket, address = server_sock.accept()
                self.task_queue.put((client_socket, address))
                print(f"[+] Connection queue size: {self.task_queue.qsize()}")
