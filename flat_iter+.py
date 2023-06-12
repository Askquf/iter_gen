class FlatIterator:
    def __init__(self, list_of_list, parent=None):
        self.list_of_list = list_of_list
        self.iterator = None
        self.parent = parent

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.list_of_list):
            raise StopIteration
        if isinstance(self.list_of_list[self.index], list):
            if self.iterator is None:
                self.iterator = iter(FlatIterator(self.list_of_list[self.index], self))
            try:
                tmp = next(self.iterator)
            except StopIteration:
                self.index += 1
                if self.index >= len(self.list_of_list):
                    raise StopIteration
                if isinstance(self.list_of_list[self.index], list):
                    self.iterator = iter(FlatIterator(self.list_of_list[self.index], self))
                    tmp = next(self.iterator)
                else:
                    tmp = self.list_of_list[self.index]
                    self.parent.index += 1
            return tmp
        else:
            self.index += 1
            return self.list_of_list[self.index - 1]


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()
