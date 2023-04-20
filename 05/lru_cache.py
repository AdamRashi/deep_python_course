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

    def __init__(self, limit=42):
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError('Limit must be an integer')

        if limit < 1:
            raise ValueError("Limit must be a positive integer number")

        self.data = {}
        self.limit = limit

        # инициализируем двусвязный список
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key not in self.data:
            raise KeyError()

        # сдвигаем запрошенный элемент в начало
        # и возвращаем его
        node = self.data[key]
        self._move_to_head(node)
        return node.value

    def set(self, key, value):
        if key in self.data:
            node = self.data[key]
            # обновляем значение и сдвигаем в начало
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.data[key] = new_node
            self._add_node(new_node)
            if len(self.data) > self.limit:
                tail_node_key = self._pop_tail().key
                del self.data[tail_node_key]

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
