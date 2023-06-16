
# Citation: Lysecky & Vahid, 2018, Section 7.8.2

class HashTable:

    def __init__(self, size=20):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Calculates the hash value for the input key
    def compute_hash(self, key):
        return key % self.size

    # Inserts a key-value pair into the hash table
    def insert(self, key, value):
        hash_key = self.compute_hash(key)
        bucket = self.table[hash_key]  # Gets bucket associated with the hash key
        for i in bucket:
            if i[0] == key:
                i[1] = value
                break
        else:
            bucket.append([key, value])  # If no matching bucket is found, appends a new key-value pair to the bucket

    # Looks up the value based on input key in the hash table
    def lookup_value(self, key):
        hash_key = self.compute_hash(key)
        bucket = self.table[hash_key]
        for i in bucket:
            if i[0] == key:
                return i[1]
        return None
