from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import os
import math
import sys
import time

inverted_index = {}
non_inverted_index = {}
queries = {}
inv_doc_frequency = {}
nr_of_documents = 0
doc_norm = {}

english_stopwords = stopwords.words('english')
porter = PorterStemmer()


def tokenize(doc):
    return doc.split()


def index_documents(doc_names, doc_dir):
    for doc_name in doc_names:
        index_doc(doc_name, doc_dir)


def current_milli_time():
    return round(time.time() * 1000)


def stem(token):
    return porter.stem(token)


def is_stopword(token):
    return token in english_stopwords


def index_doc(doc_name, path):
    filename = path + doc_name
    print(f'Indexing document {filename} ...')
    with open(filename, "r") as doc_handle:
        doc = doc_handle.read()
        tokens = tokenize(doc)
        non_inverted_index[doc_name] = {}
        for raw_token in tokens:
            stemmed_token = stem(raw_token)
            if is_stopword(stemmed_token):
                continue

            if stemmed_token not in inverted_index:
                inverted_index[stemmed_token] = {}

            if doc_name in inverted_index[stemmed_token]:
                inverted_index[stemmed_token][doc_name] += 1
            else:
                inverted_index[stemmed_token][doc_name] = 1

            if stemmed_token in non_inverted_index[doc_name]:
                non_inverted_index[doc_name][stemmed_token] += 1
            else:
                non_inverted_index[doc_name][stemmed_token] = 1


def index_queries(query_names, query_dir):
    for query_name in query_names:
        index_query(query_name, query_dir)


def index_query(query_name, path):
    filename = path + query_name
    print(f'Indexing query {filename} ...')
    with open(filename, "r") as query_handle:
        query = query_handle.read()
        tokens = tokenize(query)
        queries[query_name] = {}
        for raw_token in tokens:
            stemmed_token = stem(raw_token)
            if is_stopword(stemmed_token):
                continue

            if stemmed_token in queries[query_name]:
                queries[query_name][stemmed_token] += 1
            else:
                queries[query_name][stemmed_token] = 1


def calculate_inv_doc_frequencies():
    for word, word_stats in inverted_index.items():
        inv_doc_frequency[word] = math.log10((1 + nr_of_documents) / (1 + len(word_stats)))


def calculate_doc_norms():
    for doc_name, doc_frequency in non_inverted_index.items():
        doc_norm_sum = 0
        for word, frequency in doc_frequency.items():
            doc_norm_sum += (inv_doc_frequency[word] * frequency) ** 2
        doc_norm[doc_name] = math.sqrt(doc_norm_sum)


def process_queries(length, label):
    if not os.path.exists('results'):
        os.makedirs('results')

    ctm = current_milli_time()
    filename = f'results/results_{label}_{ctm}.txt'

    with open(filename, 'x') as file:
        query_names = sorted(queries.keys(), key=int)
        for query_name in query_names:
            query_index = queries[query_name]
            query_norm_sum = 0
            accumulator_sums = {}
            for word, query_frequency in query_index.items():
                if word not in inv_doc_frequency:
                    inv_doc_frequency[word] = math.log10(1 + nr_of_documents)

                b = query_frequency * inv_doc_frequency[word]
                query_norm_sum = b ** 2

                if word in inverted_index:
                    for doc_name, term_frequency in inverted_index[word].items():
                        if doc_name not in accumulator_sums:
                            accumulator_sums[doc_name] = 0

                        a = term_frequency * inv_doc_frequency[word]
                        accumulator_sums[doc_name] += a * b

            query_norm = math.sqrt(query_norm_sum)
            accumulator = []
            for doc_name, value in accumulator_sums.items():
                accumulator_item = {
                    'doc_name': doc_name,
                    'value': (value / (query_norm * doc_norm[doc_name]))
                }
                accumulator.append(accumulator_item)

            results = sorted(accumulator, key=lambda x: x['value'], reverse=True)[:length]

            for result_index, result in enumerate(results):
                line = "{} Q0 {} {} {} {}".format(query_name, result['doc_name'], result_index + 1, result['value'], 'lit')
                file.write(line + '\n')

    with open(filename) as file:
        print(file.read(-1))


if __name__ == "__main__":
    language = sys.argv[1]
    length = sys.argv[2]

    doc_dir = "./documents/"
    query_dir = f"./queries/{language}/"

    print(f'Retrieving queries from {query_dir}')

    doc_names = os.listdir(doc_dir)
    nr_of_documents = len(doc_names)
    index_documents(doc_names, doc_dir)

    query_names = os.listdir(query_dir)
    index_queries(query_names, query_dir)

    calculate_inv_doc_frequencies()
    calculate_doc_norms()
    process_queries(int(length), language)
