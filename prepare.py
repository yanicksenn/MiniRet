import sys
import xml.etree.ElementTree as et
import os
import glob


def prepare_trec(trec_filename, prepare_path):
    if not os.path.exists(prepare_path):
        os.makedirs(prepare_path)
        print(f'Prepare path {prepare_path}')

    documents = glob.glob(f'{prepare_path}/*')
    for document in documents:
        os.remove(document)
        print(f'Prune query {document}')

    tree = et.parse(trec_filename)
    trec = tree.getroot()
    for doc in trec:
        record_id = doc.find('recordId').text
        text = doc.find('text').text

        with open(f'{prepare_path}/{record_id}', 'w') as file:
            file.write(text)
            print(f'Done writing doc {record_id}')


def main(argv):
    label = argv[1]
    trec_filename = f'raw/ie1_queries_{label}.trec'
    prepare_path = f'queries/{label}'
    prepare_trec(trec_filename, prepare_path)


if __name__ == '__main__':
    main(sys.argv)
