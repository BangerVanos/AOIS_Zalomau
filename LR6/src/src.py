from typing import Optional
from .cool_text_colors import BGcolors


class HashNode:
    def __init__(self, hash_key: str, data: Optional[str]):
        self.hash_key = hash_key
        self.data = data
        self.next: Optional[HashNode] = None

    def __str__(self):
        return f'{self.hash_key}: {self.data}'


class HashTable:
    def __init__(self, table_size: int):
        self.__table_size = table_size
        self.__table = [None] * table_size

    @staticmethod
    def __get_value_for_key(word: str) -> int:
        if len(word) == 0:
            return 0
        elif len(word) <= 2:
            return ord(word)
        else:
            return sum([ord(word[i]) * 2 ** i for i in range(len(word))])

    def __hash_func(self, hash_key: str):
        if not isinstance(hash_key, str):
            raise ValueError('Can hash only keys of str type')
        return self.__get_value_for_key(hash_key) % self.__table_size

    def __setitem__(self, hash_key: str, data: str):
        table_index: int = self.__hash_func(hash_key)
        hash_node: Optional[HashNode] = self.__table[table_index]
        while hash_node:
            if hash_node.hash_key == hash_key:
                hash_node.data = data
                return
            print(f'{BGcolors.WARNING}Key {hash_key} collided with key {hash_node.hash_key}{BGcolors.ENDC}')
            hash_node = hash_node.next
        new_hash_node = HashNode(hash_key, data)
        new_hash_node.next = self.__table[table_index]
        self.__table[table_index] = new_hash_node

    def __getitem__(self, hash_key: str):
        table_index = self.__hash_func(hash_key)
        hash_node: Optional[HashNode] = self.__table[table_index]
        while hash_node:
            if hash_node.hash_key == hash_key:
                return hash_node.data
            hash_node = hash_node.next
        raise KeyError(hash_key)

    def delete(self, hash_key: str):
        table_index = self.__hash_func(hash_key)
        hash_node: Optional[HashNode] = self.__table[table_index]
        prev_hash_node = None
        while hash_node:
            if hash_node.hash_key == hash_key:
                if prev_hash_node:
                    prev_hash_node.next = hash_node.next
                else:
                    self.__table[table_index] = hash_node.next
                return
            prev_hash_node = hash_node
            hash_node = hash_node.next
        raise KeyError(hash_key)

    def __str__(self):
        return_str = ''
        for i in range(len(self.__table)):
            return_str += f'\n[{i}]: {self.__table[i]}'
        return return_str
