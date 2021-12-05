from prepare import prepare_trec


def main():
    prepare_trec('raw/ie1_queries_original.trec', 'queries/original')
    prepare_trec('raw/ie1_queries_french.trec', 'queries/french')
    prepare_trec('raw/ie1_queries_german.trec', 'queries/german')
    prepare_trec('raw/ie1_queries_irish.trec', 'queries/irish')
    prepare_trec('raw/ie1_queries_latin.trec', 'queries/latin')
    prepare_trec('raw/ie1_queries_norwegian.trec', 'queries/norwegian')
    prepare_trec('raw/ie1_queries_spanish.trec', 'queries/spanish')


if __name__ == '__main__':
    main()
