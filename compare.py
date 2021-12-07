import sys


def main(argv):
    file1 = 'results/results_original_1638711993787.txt'
    file2 = argv[1]
    language = file2.split('_')[1]

    result_original = file_parser(file1)
    result_translated = file_parser(file2)

    information_coverage = determine_information_coverage(result_original, result_translated, 100)
    print(f'{information_coverage * 100}%')

    # compare_first_rank(result_original, result_translated)
    # compare_first_100_ranks(result_original, result_translated, 1000, language)
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


def determine_information_coverage(original, translated, top_n):
    queries = original.keys()
    coverage_sum = 0
    for query in queries:
        coverage_sum += determine_information_coverage_for_query(original, translated, top_n, query)

    return coverage_sum / len(queries)


def determine_information_coverage_for_query(original, translated, top_n, query):
    rank_original = original[query]
    rank_translated = translated[query]

    size_original = min(top_n, len(rank_original))
    size_translated = min(top_n, len(rank_translated))

    matches = 0

    for ro in range(1, size_original + 1):
        for rt in range(1, size_translated + 1):
            if rank_original[ro] == rank_translated[rt]:
                matches += 1
                break

    return matches / size_original


def compare_first_rank(original, translated):
    counter_first = 0
    queries = original.keys()
    for query in queries:
        if original[query][1] == translated[query][1]:
            counter_first += 1
    percentage = (counter_first / len(queries)) * 100

    print(f'{counter_first} of the {len(queries)} queries (={percentage}%) have the same top result')
    return counter_first


def compare_first_100_ranks(original, translated, length, language):
    upper_interest_bound = 95
    lower_interest_bound = 40
    counter_not_exact_match = 0
    counter_exact_match = 0

    queries = original.keys()
    for query in queries:
        counter = 0
        min_original = min(length, len(original[query]))
        min_translated = min(length, len(translated[query]))

        for rank_original in range(1, min_original + 1):
            for rank_translated in range(1, min_translated + 1):
                if original[query][rank_original] == translated[query][rank_translated]:
                    counter += 1
                    break

        if counter == min_original or counter == min_translated:
            with open(f'queries/original/{query}') as query_original:
                with open(f'queries/{language}/{query}') as query_translated:
                    content_original = query_original.read(-1)
                    content_translated = query_translated.read(-1)
                    if content_translated != content_original:
                        counter_not_exact_match +=1
                        print(f'the query {query} is not an exact match in english & {language}')
                    else:
                        counter_exact_match += 1

        elif counter <= lower_interest_bound or counter >= upper_interest_bound:
            print(f'For Query {query} there are {counter} same retrieval results')

    total_100er_matches = counter_exact_match + counter_not_exact_match
    print(f'\nOut of {total_100er_matches}  {counter_exact_match} were exact matches to the Original Query and {counter_not_exact_match} were not exact matches but found the same {length} results')


if __name__ == '__main__':
    main(sys.argv)
