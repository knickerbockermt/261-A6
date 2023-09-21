# 261-A6

This project consists of two implementations of a hash map, one using open addressing and one using chaining, both using dynamic arrays.  Initial methods were provided by the instructors.

Chaining:
This implementation uses a dynamic array to store singly linked lists (buckets). Each list contains nodes with keys of the same value after the hash function is applied.

The following methods were implemented for both the chaining and open addressing Hash Map classes. The average time complexity of all methods is O(1):

1. put: adds a key/value pair to the table. If the key already exists,, the value is updated. If the current load factor of the table is greater or equal to 1.0, resize_array is called to resize the table to double its capacity before the key/value pair is added.
2. empty_buckets: returns the number of empty buckets in the hash table.
3. table_load: returns the current hash table load factor, calculated as the size/capacity.
4. clear: empties all buckets in the hash map without altering the capacity.
5. resize_table: if the new capacity is not less than 1, this method resizes the hash table to the new capacity. If the new capacity is not a prime number, the method will use the next highest prime. The method calls get_keys_and_values to store the key/value pairs and then rehashes the pairs to a new hash map with the new capacity.
6. get: recieves a key and returns the corresponding value. Returns None if there is no matching key.
7. contains_key: takes a given key and returns True if it is in the hash table, and Returns false if not.
8. remove: removes a key/value pair from the hash table. Does nothing if the key is not in the map.
9. get_keys_and_values: returns a dynamic array for which each index is a key/value pair stored as a tuple.

For the chaining hash map, there is an additional stand-alone function, find_mode. This function takes an unsorted dynamic array and uses a hash map to find the mode value(s) in the array. The function stores all of the mode values in an array and returns a tuple containing this array and the frequency at which the mode value(s) occur. This function has a time complexity of O(n)

The open addressing hash map contains two additional methods within the HashMap class: __iter__ and __next__. These methods allow for iteration through the hash map.


