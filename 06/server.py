import argparse
from master import Master


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Basic webserver that uses multiprocessing"
    )
    parser.add_argument("-w", type=int, help="Number of worker threads", required=True)
    parser.add_argument(
        "-k", type=int, help="Number of most frequent words to return", required=True
    )
    args = parser.parse_args()

    server = Master("localhost", 16000, args.w, args.k)
    server.start()
