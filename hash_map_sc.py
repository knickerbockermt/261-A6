# Name: Paige Knickerbocker
# OSU Email: knickerp@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 08-15-2023
# Description: Implementation of hashmap using dynamic array and chaining
# for collision resolution


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # double size if table load >= 1
        if self.table_load() >= 1:
            self.resize_table(self._capacity*2)

        # find location of key
        hash = self._hash_function(key)
        index = hash % self._capacity
        index_lst = self._buckets[index]
        node = index_lst.contains(key)

        # map does not contain key
        if node is None:
            index_lst.insert(key, value)
            self._size += 1

        # map contains key
        else:
            node.value = value


    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in map
        :return: integer value of empty buckets
        """
        empty = 0

        # check length of list at each index in map
        for index in range(self._capacity):
            l_list = self._buckets[index]
            if l_list.length() == 0:
                empty += 1

        return empty

    def table_load(self) -> float:
        """
        Returns the hash table load factor.
        :return: float representing load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Empties buckets while maintaining capacity.
        :return: none
        """
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes map to new capacity or closest prime number if
        not prime.
        :param new_capacity: integer representing new capacity
        :return: none
        """
        if new_capacity < 1:
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
            self._buckets.append(LinkedList())

        # add values to new map
        length = values.length()
        for index in range(length):
            key, value = values[index]
            self.put(key, value)

    def get(self, key: str):
        """
        Returns the value corresponding to the given key
        :param key: string representing key
        :return: value if key found, none if not found
        """
        # find location of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        l_list = self._buckets[index]
        node = l_list.contains(key)

        # key found
        if node:
            return node.value

        # key not found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if key is found in map.
        :param key: string representing key to be found
        :return: true if map contains key, false if not
        """
        # find location of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        l_list = self._buckets[index]

        # does not contain key
        if l_list.contains(key) is None:
            return False

        # contains key
        return True

    def remove(self, key: str) -> None:
        """
        Removes node corresponding to key from map.
        :param key: key corresponding to node to be removed
        :return: none
        """
        # find location of node
        hash = self._hash_function(key)
        index = hash % self._capacity

        l_list = self._buckets[index]

        # remove node if present
        if l_list.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns Dynamic Array containing all key/value pairs in map
        :return: Dynamic Array containing tuples
        """
        key_arr = DynamicArray()

        # iterate through each list in map and add value to array
        for index in range(0, self._capacity, 1):
            l_list = self._buckets[index]
            for node in l_list:
                key_arr.append((node.key, node.value))

        return key_arr

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the mode value(s) of unsorted Dynamic Array.
    :param da: Dynamic Array
    :return: tuple containing Dynamic Array of value(s) and frequency
    """
    map = HashMap()
    mode_values = DynamicArray()
    mode_frequency = 0

    for index in range(da.length()):
        key = da[index]

        # value has not yet been added to map
        if not map.contains_key(key):
            # add to map
            map.put(key, 1)

            # first value added to map
            if mode_frequency == 0:
                mode_values.append(key)
                mode_frequency += 1

            # frequency = mode frequency
            elif mode_frequency == 1:
                mode_values.append(key)

        # value has been added to map
        else:
            # update frequency of value
            frequency = map.get(key) + 1
            map.put(key, frequency)

            # frequency greater than current mode frequency
            if frequency > mode_frequency:
                mode_values = DynamicArray()
                mode_values.append(key)
                mode_frequency = frequency

            # frequency same as current mode frequency
            elif frequency == mode_frequency:
                mode_values.append(key)

    return mode_values, mode_frequency


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
