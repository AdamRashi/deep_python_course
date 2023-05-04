import asyncio
from collections import Counter

import aiohttp
import argparse


async def fetch_url(url, session):
    """
    Асинхронная функция, обкачивающая url, и возвращающая кортеж
    состоящий из URL'а и самого часто встречающегося слова. В случае
    если при запросе произошла ошибка, возвращается только URL
    """
    try:
        async with session.get(url) as response:
            text = await response.read()
            most_common_word = Counter(text.split()).most_common(1)
            # в случае успешного запроса, вернём url и
            # самое часто встречающиеся слово
            return url, most_common_word
    except aiohttp.ClientError as e:
        # в случае ошибки при запросе к URL, вернём только url
        return url


async def fetch_all(urls, concurrent_requests):
    async with aiohttp.ClientSession() as session:
        tasks = []
        sem = asyncio.Semaphore(concurrent_requests)

        async with sem:
            for url in urls:
                task = asyncio.create_task(fetch_url(url, session))
                tasks.append(task)

        return await asyncio.gather(*tasks)


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

    results = asyncio.run(fetch_all(url_gen(args.url_file), args.concurrent_requests))

    for result in results:
        print(result)
