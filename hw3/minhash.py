from sklearn.utils import murmurhash3_32 as mhash_raw
import random, argparse, string, sys


def k_gram(my_str, k):
    return [my_str[i:i+k] for i in range(len(my_str) - k + 1)]


def hfunc_gen(R=1e12):
    seed = random.randint(0, 2 ** 20)
    return lambda hkey: (mhash_raw(hkey, seed=seed) % R)


def minhash_gen(m, k, R=1e12):
    hfuncs = [hfunc_gen(R=R) for _ in range(m)]
    
    def min_hash(str):
        str_k_gram = k_gram(str, k)
        return [min([hfunc(g) for g in str_k_gram]) for hfunc in hfuncs]
    
    return min_hash


def jaccard_sim(str1, str2, k):
    k_gram1 = set(k_gram(str1, k))
    k_gram2 = set(k_gram(str2, k))
    return len(k_gram1.intersection(k_gram2)) * 1. / len(k_gram1.union(k_gram2))


class SingleTable:
    
    def __init__(self, K, B, R):
        self.bucket_hash = hfunc_gen(R=B)
        self.table = [[] for _ in range(B)]
        self.minhash_func = minhash_gen(m, 3, )
        pass
    
    def insert(self, hashcode, id):
        pass
    
    def lookup(self, hashcode):
        pass


class HashTable:
    
    def __init__(self, K, L, B, R):
        '''
        K: Number of Hash Functions.
        L: Number of Hash Tables.
        B: Size of Hash Tables.
        R: Range of Hash Functions
        '''
        self.s_tables = [SingleTable(K, B, R) for _ in range(L)]
    
    def insert(self, hashcode, id):
        for s_table in self.s_tables:
            s_table.insert(hashcode, id)
    
    def lookup(self, hashcode):
        lookup_result = set([])
        for s_table in self.s_tables:
            lookup_result = lookup_result.union(s_table.lookup(hashcode))
        return lookup_result
        


if __name__ == '__main__':
    random.seed(3407)
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, default='none', choices=['warmup', 'extended', 'both', 'none'])
    args = parser.parse_args()
    
    if args.mode in ['warmup', 'both']:
        with open('warmup_str.txt') as wfile:
            str1 = wfile.readline()[:-1]
            str2 = wfile.readline()[:-1]
        minhash_func = minhash_gen(100, 3)
        hashcode1 = minhash_func(str1)
        hashcode2 = minhash_func(str2)
        hash_similarity = sum([int(h1 == h2) for h1, h2 in 
                               zip(hashcode1, hashcode2)]) / 100.
        jaccard_similarity = jaccard_sim(str1, str2, 3)
        print(f'The Jaccard Similarity is {jaccard_similarity:.3f}.')
        print(f'The Minhash Similarity is {hash_similarity:.3f}.')
    
    if args.mode in ['extended', 'both']:
        pass
    
