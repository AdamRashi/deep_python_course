import logging


def configure_logging(enable_stdout=False, filter_logs=False):
    # инициализируем логирование
    logger = logging.getLogger("LRUCache")
    logger.setLevel(logging.DEBUG)

    # создадим обработчик для записи в файл
    file_handler = logging.FileHandler("cache.log")
    file_handler.setLevel(logging.DEBUG)

    # определим форматирование для записи в файл
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # добавим обработчика в логгер
    logger.addHandler(file_handler)

    if enable_stdout:
        # создадим обработчика для вывода в консоль
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        # форматирование для вывода в консоль
        stream_formatter = logging.Formatter("%(levelname)s - %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    if filter_logs:
        # реализация фильтра для отбрасывания записей
        class CustomFilter(logging.Filter):
            def filter(self, record):
                # оставляем только записи, связанные с операцией set
                return "SET" in record.msg

        custom_filter = CustomFilter()
        file_handler.addFilter(custom_filter)
        if enable_stdout:
            stream_handler.addFilter(custom_filter)
