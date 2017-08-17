import hashlib
from random import choice
import copy

LEGAL_KEYS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

class RainbowTable:

    def __init__(self, num_rows, chainlength, keylength):

        self.num_rows = num_rows
        self.num_links = chainlength
        self.keylength = keylength
        self.hasher = hashlib.sha1()
        self.key_list = None
        self.rainbow_table = None

    def hash_a_key(self, key):
        """ Generate a 40-digit hash from a key of
            some length. (restrictions?)
        """
        temp = key.encode('utf-8')
        self.hasher.update(temp)
        return self.hasher.hexdigest()

    def reduce_a_hash(self, a_hash, salt):
        """ Take a hash and a salt (integer), generate a key.
            The hash must be divided into self.keylength equal chunks:
            each chunk is reduced to one letter of the resulting key.

            Example:

            ahash = 2c6088d51a7e17115869fd3c1e360a835be46ddc
            keylength = 9
            temp_chunk_length = 4
            extra = 4

            chunk1: 2c60
            chunk2: 88d5
            chunk3: 1a7e
            chunk4: 1711
            chunk5: 5869
            chunk6: fd3c
            chunk7: 1e36
            chunk8: 0a83
            chunk9: 5be4
            extra: 6ddc       => add 6 to chunk1, d to chunk 2, etc.

            Then convert to int.  Then add salt.  Then convert to letter.
        """

        temp_reduced_string = ""
        temp_chunk_length = int(float(len(a_hash)) / self.keylength)
        temp_extra = len(a_hash) % self.keylength

        for letter_index in range(self.keylength):
            start_index = letter_index * temp_chunk_length
            one_chunk = a_hash[start_index : start_index + temp_chunk_length - 1]

            if temp_extra > 0:
                one_chunk = one_chunk + a_hash[-temp_extra]
                temp_extra -= 1

            one_chunk = int(one_chunk, 16) # convert from hex
            one_chunk += salt # add salt
            temp_reduced_string += LEGAL_KEYS[one_chunk % len(LEGAL_KEYS)]

        print(temp_reduced_string)
        return temp_reduced_string


    def generate_a_key(self):
        """ Generates a key... but why do I think it's unique?
            Fix this to make sure it's unique?
        """
        temp_string = ""
        for _ in range(self.keylength):
            temp_string += choice(LEGAL_KEYS)
        return temp_string

    def generate_all_keys(self, num_rows, keylength):
        temp_list = []
        for _ in range(num_rows):
            temp_string = self.generate_a_key()
            while temp_string in temp_list:
                temp_string = self.generate_a_key()
            temp_list.append(temp_string)
        self.key_list = copy.deepcopy(temp_list)

    def generate_chain(self, key):
        temp_hash = None
        temp_key = key
        for i in range(self.num_links):
            temp_hash = self.hash_a_key(temp_key)
            temp_key = self.reduce_a_hash(temp_hash, i)

        return temp_hash

    def make_rainbow_table(self):
        temp_dict = {}
        self.generate_all_keys(self.num_rows, self.keylength)
        for key in self.key_list:
            end_hash = self.generate_chain(key)
            temp_dict[end_hash] = key

        self.rainbow_table = copy.deepcopy(temp_dict)

    def run_searches(self):
        temp_hash = input("Enter a hash to search for: ")
        self.search_table(temp_hash)
        self.run_searches()

    def search_table(self, a_hash):

        self.hash_to_crack = a_hash

        if self.check_hashes(self.hash_to_crack):
            return 1
        else:
            for i in range(self.num_links-1, -1, -1):
                temp_hash = self.hash_to_crack
                temp_key = None
                for j in range(i, self.num_links):
                    temp_key = self.reduce_a_hash(temp_hash, j)
                    temp_hash = self.hash_a_key(temp_key)
                    if self.check_hashes(temp_hash):
                        return 1

    def check_hashes(self, a_hash):
        if a_hash in self.rainbow_table:
            print("Matched a hash!")
            return self.regenerate_key(self.rainbow_table[a_hash])

    def regenerate_key(self, key):
        temp_key = key
        for i in range(self.num_links):
            print("Did it " + str(i) + " times.")
            temp_hash = self.hash_a_key(temp_key)
            if temp_hash == self.hash_to_crack:
                print("Your key was: " + str(temp_key))
                return True
            else:
                temp_key = self.reduce_a_hash(temp_hash, i)
        print("Key not found.")

#-------------------------------------

x = RainbowTable(15000, 10, 3)
x.make_rainbow_table()
x.hash_to_crack = "975f041c151aeba305ba96194d39fddc535e76b5"
x.regenerate_key("tru")

for i in range(10):
    temp = x.hash_a_key(x.generate_a_key())
    print(temp)
x.run_searches()
"""
# 70000 rows takes 57 seconds (10 chainlength)
# 10000 takes 1.7 seconds (10 chainlength)
# but from chainlength 10 to 100, only 7.02 seconds (10000 rows)
# chainlength 1000 = 66 seconds (10000 rows)
"""
