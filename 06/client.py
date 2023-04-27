import argparse
import socket
from threading import Thread, current_thread, Lock

counter = 0


class Client:
    def __init__(self, file_path: str, n_threads: int = 1):
        super().__init__()
        self.file = file_path
        self.url_gen = self._get_url()
        self.n_threads = n_threads
        self.lock = Lock()
        self.a = 0

    def _get_url(self):
        with open(self.file, "r") as file:
            i = 0
            for url in file:
                yield url.strip()
                i += 1
            print(i)

    def _send_url(self):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect(("localhost", 16000))
        retry = False
        while True:
            try:
                # получаем следующий url
                if not retry:
                    with self.lock:
                        url_to_send = next(self.url_gen)
                retry = False

                client_sock.send(url_to_send.encode())
                print(f"[{current_thread().name}] sends: {url_to_send}")
                answer = client_sock.recv(10000).decode()
                print(f"[{current_thread().name}] receives {url_to_send}: {answer}")

            except StopIteration:
                # поток прекращает работу только тогда, когда больше не
                # останется урлов для обработки
                print(f"[-{current_thread().name}] " f"Поток завершает выполнение")
                break

            except Exception as e:
                print(f"[-{current_thread().name}] Возникла ошибка {e}")
                # если возникла ошибка или соединение оборвалось,
                # закрываем сокет и создаём новый
                client_sock.close()
                client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_sock.connect(("localhost", 16000))
                retry = True
                continue

    def send_urls(self):
        threads = []
        for i in range(self.n_threads):
            thread = Thread(target=self._send_url, name=f"T{i}")
            threads.append(thread)
            thread.start()

        for th in threads:
            th.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("threads", type=int, help="Number of threads")
    parser.add_argument("-f", type=str, help="Path to file with urls", required=True)
    args = parser.parse_args()

    client = Client(args.f, args.threads)
    client.send_urls()
