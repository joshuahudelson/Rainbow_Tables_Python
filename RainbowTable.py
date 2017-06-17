import hashlib
from random import choice
import copy

LEGAL_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class RainbowTable:

    def __init__(self):

        self.hasher = hashlib.sha1()
        self.key_list = None
        self.rainbow_table = None

    def hash_a_key(self, key):
        temp = key.encode('utf-8')
        self.hasher.update(temp)
        return self.hasher.hexdigest()

    def reduce_a_hash(self, a_hash, keylength, salt):
        temp_reduced_string = ""
        temp_num_chunks = int(len(a_hash)/keylength)
        temp_extra = len(a_hash) % keylength

        for i in range(keylength):
            start_index = i * temp_num_chunks
            one_chunk = a_hash[start_index : start_index + temp_num_chunks]

            if temp_extra > 0:
                one_chunk = one_chunk + a_hash[-temp_extra]
                temp_extra -= 1

            one_chunk = int(one_chunk, 16) # convert from hex
            one_chunk += salt # add salt
            temp_reduced_string += LEGAL_KEYS[one_chunk % len(LEGAL_KEYS)]

        return temp_reduced_string

    def generate_unique_key(self, keylength):
        temp_string = ""
        for _ in range(keylength):
            temp_string += choice(LEGAL_KEYS)
        return temp_string

    def generate_all_keys(self, num_rows, keylength):
        temp_list = []
        for _ in range(num_rows):
            temp_string = self.generate_unique_key(keylength)
            while temp_string in temp_list:
                temp_string = self.generate_unique_key(keylength)
            temp_list.append(temp_string)
        self.key_list = copy.deepcopy(temp_list)

    def generate_chain(self, num_links, key, keylength):
        temp_hash = None
        temp_key = key
        for i in range(num_links):
            temp_hash = self.hash_a_key(temp_key)
            temp_key = self.reduce_a_hash(temp_hash, keylength, i)

        return temp_hash

    def make_rainbow_table(self, num_rows, num_links, keylength):
        temp_dict = {}
        self.generate_all_keys(num_rows, keylength)
        for key in self.key_list:
            end_hash = self.generate_chain(num_links, key, keylength)
            temp_dict[key] = end_hash

        self.rainbow_table = copy.deepcopy(temp_dict)



x = RainbowTable()
x.make_rainbow_table(10000, 1000, 5)
# 70000 rows takes 57 seconds (10 chainlength)
# 10000 takes 1.7 seconds (10 chainlength)
# but from chainlength 10 to 100, only 7.02 seconds (10000 rows)
# chainlength 1000 = 66 seconds (10000 rows)
