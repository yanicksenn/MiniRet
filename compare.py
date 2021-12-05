import sys


def main(argv):
    file1 = 'results/results_original_1638711993787.txt'
    file2 = argv[1]

    compare_top_n = 100
    result_original = file_parser(file1)
    result_translated = file_parser(file2)
    compare_first_rank(result_original, result_translated)
    compare_first_100_ranks(result_original, result_translated)
    # Relevant information
    # Query id, Document id, rank



def file_parser(filename):
    result = {}

    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            split_line = line.split()
            query_id = split_line[0]
            document_id = split_line[2]
            rank = int(split_line[3])

            if query_id not in result:
                result[query_id] = {}

            result[query_id][rank] = document_id

    return result

def compare_first_rank(original, translated):
    counter_first = 0
    queries = original.keys()
    for query in queries:
        if original[query][1] == translated[query][1]:
            counter_first += 1
    percentage = (counter_first / len(queries)) * 100

    print(f'{counter_first} of the {len(queries)} queries (={percentage}%) have the same top result')
    return counter_first


def compare_first_100_ranks(original, translated):
    upper_interest_bound = 95
    lower_interest_bound = 40
    queries = original.keys()
    for query in queries:
        counter = 0
        for rank_original in range(1, 101):
            for rank_translated in range(1, 101):
                if original[query][rank_original] == translated[query][rank_translated]:
                    counter += 1
                    continue
        if counter <= lower_interest_bound or counter >= upper_interest_bound:
            print(f'For Query {query} there are {counter} same retrieval results')


if __name__ == '__main__':
    main(sys.argv)
