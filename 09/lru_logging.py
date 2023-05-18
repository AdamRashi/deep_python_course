import argparse
import logging


class Node:
    """
    Узел двусвязного списка
    """

    def __init__(self, key=None, value=None, prev=None, next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next


class LRUCache:
    """
    Класс, реализующий структуру данных, работающую
    по принципу LRU (Least Recently Used).

    В качестве структуры данных для хранения значений
    используется словарь, а для учёта порядка использования
    значений по ключу используется двусвязный список.
    """

    def __init__(self, limit=42, enable_stdout=False, filter_logs=False):
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError("Limit must be an integer")

        if limit < 1:
            raise ValueError("Limit must be a positive integer number")

        self.data = {}
        self.limit = limit

        # инициализируем двусвязный список
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

        # инициализируем логирование
        self.logger = logging.getLogger("LRUCache")
        self.logger.setLevel(logging.DEBUG)

        # определяем формат для логов
        formatter = logging. \
            Formatter("%(asctime)s - %(levelname)-8s - %(message)s")

        # создаем обработчик для записи в файл
        file_handler = logging.FileHandler("cache.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if enable_stdout:
            # если флаг вывода в консоль активен, создаем обработчик
            # для вывода в консоль
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        if filter_logs:
            # реализуем свой собственный класс-фильтр
            class CustomFilter(logging.Filter):
                def filter(self, record):
                    # отфильтровываем только записи связанные с операцией set
                    return "SET" in record.msg

            custom_filter = CustomFilter()
            file_handler.addFilter(custom_filter)
            if enable_stdout:
                stream_handler.addFilter(custom_filter)

    def get(self, key):
        if key not in self.data:
            self.logger.error("GET - Key doesn't exist: %s", key)
            raise KeyError()

        # сдвигаем запрошенный элемент в начало и возвращаем его
        node = self.data[key]
        self._move_to_head(node)
        self.logger.debug("GET - <key: %s, value: %s>", key, node.value)
        return node.value

    def set(self, key, value):
        if key in self.data:
            node = self.data[key]
            # обновляем значение и сдвигаем в начало
            node.value = value
            self._move_to_head(node)
            self.logger.warning("SET - <key: %s, value: %s> (Key existed)",
                              key,
                              value)
        else:
            new_node = Node(key, value)
            self.data[key] = new_node
            self._add_node(new_node)
            if len(self.data) > self.limit:
                tail_node_key = self._pop_tail().key
                del self.data[tail_node_key]
                self.logger.warning(
                    "SET - <key: %s, value: %s> "
                    "(Cache overflow, key <%s> deleted)",
                    key,
                    value,
                    tail_node_key,
                )
            else:
                self.logger. \
                    info("SET - <key: %s, value: %s> (New key)", key, value)

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_node(node)

    def _remove_node(self, node):
        # получаем соседние узлы
        next_node = node.next
        prev_node = node.prev
        # исключаем переданный узел из цепочки связей
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_node(self, new_node):
        # вставляем новый элемент сразу после головы списка
        new_node.prev = self.head
        new_node.next = self.head.next

        # изменяем ссылку у исходного элемента после головы
        self.head.next.prev = new_node

        # ставим голову "до" нового элемента
        self.head.next = new_node

    def _pop_tail(self):
        node = self.tail.prev
        self._remove_node(node)
        return node

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Данный модуль реализует класс LRU-cache, "
                    "который логирует операции с кэшем в файл cache.log"
    )
    parser.add_argument("-s",
                        action="store_true",
                        help="Вывод логов в консоль")
    parser.add_argument(
        "-f",
        action="store_true",
        help="Фильтрация записей логов: "
             "оставляет только записи, cвязанные с операцией set",
    )
    args = parser.parse_args()

    cache = LRUCache(limit=5, enable_stdout=args.s, filter_logs=args.f)
    cache.set("a", "1")
    cache.get("a")
    try:
        cache.get("zzz")
    except:
        pass
    cache.set("b", "2")
    cache.set("c", "3")
    cache.set("a", "11")
    cache.set("d", "4")
    cache.set("e", "5")
    cache.set("f", "6")
