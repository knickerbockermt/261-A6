# Name: Paige Knickerbocker
# OSU Email: knickerp@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08-15-2023
# Description: Implementation of hashmap using dynamic array and open addressing
# with quadratic probing for collision resolution

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds key/value pair to map. If map already contains key,
        updates value of key.
        :param key: string representing key
        :param value: value to be added/updated
        :return: none
        """
        # resize if load factor >= .5
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        # find initial index
        hash = self._hash_function(key)
        index_initial = hash % self._capacity
        entry = self._buckets[index_initial]

        index = None
        next = 1

        # use quadratic programing to find valid index
        while entry is not None and entry.key != key\
                and entry.is_tombstone is False:
            index = (index_initial + next**2) % self._capacity
            entry = self._buckets[index]
            next += 1

        # no probing needed
        if index is None:
            index = index_initial

        # key not in map, make new entry
        if entry is None or entry.is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1

        # key in map, update value
        else:
            entry.value = value


    def table_load(self) -> float:
        """
        Returns the hash table load factor.
        :return: float representing load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in map
        :return: integer value of empty buckets
        """
        empty = 0

        # add empty buckets to count
        for index in range(self._capacity):
            if self._buckets[index] is None:
                empty += 1

        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes map to new capacity or closest prime number if
        not prime.
        :param new_capacity: integer representing new capacity
        :return: none
        """
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # store values of current map
        values = self.get_keys_and_values()

        # create new map with new capacity
        self._capacity = new_capacity
        self._buckets = DynamicArray()
        self._size = 0

        for _ in range(self._capacity):
            self._buckets.append(None)

        # add values to new map
        length = values.length()
        for index in range(length):
            key, value = values[index]
            self.put(key, value)

    def get(self, key: str) -> object:
        """
        Returns the value corresponding to the given key
        :param key: string representing key
        :return: value if key found, none if not found
        """
        # find initial index of key
        hash = self._hash_function(key)
        index_initial = hash % self._capacity
        entry = self._buckets[index_initial]

        next = 1

        # use quadratic probing to find key if necessary
        while entry is not None and entry.key != key:
            index = (index_initial + next ** 2) % self._capacity
            entry = self._buckets[index]
            next += 1

        # key not in map
        if entry is None or entry.is_tombstone:
            return None

        # key in map
        return entry.value

    def contains_key(self, key: str) -> bool:
        """
        Checks if key is found in map.
        :param key: string representing key to be found
        :return: true if map contains key, false if not
        """
        # find initial index of key
        hash = self._hash_function(key)
        index_initial = hash % self._capacity
        entry = self._buckets[index_initial]

        next = 1

        # use quadratic probing if necessary
        while entry is not None and entry.key != key:
            index = (index_initial + next ** 2) % self._capacity
            entry = self._buckets[index]
            next += 1

        # key not in map
        if entry is None or entry.is_tombstone:
            return False

        # key in map
        return True

    def remove(self, key: str) -> None:
        """
        Removes node corresponding to key from map.
        :param key: key corresponding to node to be removed
        :return: none
        """
        # find initial index
        hash = self._hash_function(key)
        index_initial = hash % self._capacity
        entry = self._buckets[index_initial]

        next = 1

        # use quadratic probing as necessary
        while entry is not None and entry.key != key:
            index = (index_initial + next ** 2) % self._capacity
            entry = self._buckets[index]
            next += 1

        # key not in map
        if entry is None or entry.is_tombstone:
            return

        # key in map
        entry.is_tombstone = True
        self._size -= 1

    def clear(self) -> None:
        """
        Empties buckets while maintaining capacity.
        :return: none
        """
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns Dynamic Array containing all key/value pairs in map
        :return: Dynamic Array containing tuples
        """
        key_arr = DynamicArray()

        # iterate through each list in map and add value to array
        for index in range(self._capacity):
            entry = self._buckets[index]
            if entry is not None and not entry.is_tombstone:
                key_arr.append((entry.key, entry.value))

        return key_arr

    def __iter__(self):
        """
        Create iterator for loop
        :return: self
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Iterate through array and return valid entries
        :return: valid entries
        """
        # check if index is within range
        try:
            entry = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        # find next valid index
        while entry is None or entry.is_tombstone is True:
            self._index += 1
            if self._index >= self._capacity:
                raise StopIteration
            entry = self._buckets[self._index]

        self._index += 1

        # return valid entry
        return entry



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
