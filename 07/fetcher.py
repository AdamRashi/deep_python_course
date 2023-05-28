import asyncio
import time
from collections import Counter

import aiohttp
import argparse


async def fetch_url(session, url_gen, results):
    """
    Асинхронная функция, обкачивающая url, и возвращающая кортеж
    состоящий из URL'а и самого часто встречающегося слова. В случае
    если при запросе произошла ошибка, возвращается только URL
    """
    while True:
        try:
            url = next(url_gen)
        except StopIteration:
            break

        try:
            async with session.get(url) as response:
                text = await response.read()
                most_common_word = Counter(text.split()).most_common(1)
                # в случае успешного запроса, вернём url и
                # самое часто встречающиеся слово
                results.append((url, most_common_word))
        except aiohttp.ClientError:
            # в случае ошибки при запросе к URL, вернём только url
            results.append((url,))


async def fetch_all(urls_file, workers_number):
    urls = url_gen(urls_file)

    async with aiohttp.ClientSession() as session:
        fetch_results = []

        workers = [
            asyncio.create_task(fetch_url(session, urls, fetch_results))
            for _ in range(workers_number)
        ]

        await asyncio.gather(*workers)

    return fetch_results


def url_gen(url_file):
    """
    Генератор, при обращении к которому возвращается один
    url из файла
    """
    with open(url_file, "r") as file:
        line = file.readline()
        while line:
            yield line.strip()
            line = file.readline()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async URL fetcher")
    parser.add_argument(
        "concurrent_requests",
        default=10,
        type=int,
        help="Number of concurrent requests",
    )
    parser.add_argument("url_file", type=str, help="Path to file with URLs")

    args = parser.parse_args()

    # команда для корректного запуска на Windows.
    # По умолчанию установлена политика WindowsProactorEventLoopPolicy,
    # с ней почему-то event loop закрывается раньше, чем надо
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    start_time = time.time()
    results = asyncio.run(fetch_all(args.url_file, args.concurrent_requests))
    end_time = time.time() - start_time

    for res in results:
        print(res)

    print(f"Время выполнения: {end_time} секунд")
